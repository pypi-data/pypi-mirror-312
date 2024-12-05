use std::hash::{Hash, Hasher};
use std::sync::Arc;
use std::time::Duration;

use moka::sync::Cache;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::pyclass::CompareOp;
use pyo3::types::PyType;

#[derive(Debug)]
struct AnyKey {
    obj: PyObject,
    hash: isize,
}

impl AnyKey {
    fn new(obj: PyObject) -> PyResult<Self> {
        let hash = Python::with_gil(|py| obj.to_object(py).into_bound(py).hash())?;
        Ok(AnyKey { obj, hash })
    }

    fn new_with_gil(obj: PyObject, py: Python) -> PyResult<Self> {
        let hash = obj.to_object(py).into_bound(py).hash()?;
        Ok(AnyKey { obj, hash })
    }
}

impl PartialEq for AnyKey {
    fn eq(&self, other: &Self) -> bool {
        Python::with_gil(|py| {
            let lhs = self.obj.to_object(py).into_bound(py);
            let rhs = other.obj.to_object(py).into_bound(py);
            match lhs.rich_compare(rhs, CompareOp::Eq) {
                Ok(v) => v.is_truthy().unwrap_or_default(),
                Err(_) => false,
            }
        })
    }
}

impl Eq for AnyKey {}
impl Hash for AnyKey {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.hash.hash(state);
    }
}

#[pyclass]
struct Moka(Arc<Cache<AnyKey, Arc<PyObject>, ahash::RandomState>>);

#[pymethods]
impl Moka {
    #[new]
    #[pyo3(signature = (capacity, ttl=None, tti=None))]
    fn new(capacity: u64, ttl: Option<f64>, tti: Option<f64>) -> PyResult<Self> {
        let mut builder = Cache::builder().max_capacity(capacity);

        if let Some(ttl) = ttl {
            let ttl_micros = (ttl * 1000_000.0) as u64;
            if ttl_micros == 0 {
                return Err(PyValueError::new_err("ttl must be positive"));
            }
            builder = builder.time_to_live(Duration::from_micros(ttl_micros));
        }

        if let Some(tti) = tti {
            let tti_micros = (tti * 1000_000.0) as u64;
            if tti_micros == 0 {
                return Err(PyValueError::new_err("tti must be positive"));
            }
            builder = builder.time_to_idle(Duration::from_micros(tti_micros));
        }

        Ok(Moka(Arc::new(
            builder.build_with_hasher(ahash::RandomState::default()),
        )))
    }

    #[classmethod]
    fn __class_getitem__<'a>(
        cls: &'a Bound<'a, PyType>,
        _v: PyObject,
    ) -> PyResult<&'a Bound<'a, PyType>> {
        Ok(cls)
    }

    fn set(&self, py: Python, key: PyObject, value: PyObject) -> PyResult<()> {
        let hashable_key = AnyKey::new_with_gil(key, py)?;
        let value = Arc::new(value.clone_ref(py));
        py.allow_threads(|| self.0.insert(hashable_key, value));
        Ok(())
    }

    fn get(&self, py: Python, key: PyObject) -> PyResult<Option<PyObject>> {
        let hashable_key = AnyKey::new_with_gil(key, py)?;
        let value = py.allow_threads(|| self.0.get(&hashable_key));
        Ok(value.map(|obj| obj.clone_ref(py)))
    }

    fn get_with(&self, py: Python, key: PyObject, initializer: PyObject) -> PyResult<PyObject> {
        let hashable_key = AnyKey::new_with_gil(key, py)?;
        py.allow_threads(|| {
            self.0.try_get_with(hashable_key, || {
                Python::with_gil(|py| initializer.call0(py).map(Arc::new))
            })
        })
        .map(|v| v.clone_ref(py))
        .map_err(|e| e.clone_ref(py))
    }

    fn remove(&self, py: Python, key: PyObject) -> PyResult<Option<PyObject>> {
        let hashable_key = AnyKey::new_with_gil(key, py)?;
        let removed = py.allow_threads(|| self.0.remove(&hashable_key));
        Ok(removed.map(|obj| obj.clone_ref(py)))
    }

    fn clear(&self, py: Python) {
        py.allow_threads(|| self.0.invalidate_all());
    }

    fn count(&self, py: Python) -> u64 {
        py.allow_threads(|| self.0.entry_count())
    }
}

#[pymodule]
fn moka_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Moka>()?;
    Ok(())
}
