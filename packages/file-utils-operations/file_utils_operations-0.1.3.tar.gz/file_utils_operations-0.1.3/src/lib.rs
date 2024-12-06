use pyo3::prelude::*;

#[doc(hidden)]
pub mod utils;

pub mod with_eol;
use with_custom_delims::WithCustomDelims;
use with_eol::WithEOL;

pub mod with_custom_delims;

////
#[pymodule]
fn file_utils_operations_lib(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<WithEOL>()?;
    m.add_class::<WithCustomDelims>()?;
    Ok(())
}
