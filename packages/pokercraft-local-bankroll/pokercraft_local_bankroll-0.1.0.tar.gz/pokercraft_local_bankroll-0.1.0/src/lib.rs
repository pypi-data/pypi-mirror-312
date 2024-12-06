use pyo3::prelude::*;

mod calculation;

use calculation::calculate;

/// A Python module implemented in Rust.
#[pymodule]
fn pokercraft_local_bankroll(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate, m)?)?;
    Ok(())
}
