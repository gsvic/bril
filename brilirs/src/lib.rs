// The group clippy::pedantic is not used as it ends up being more annoying than useful
#![warn(clippy::all, clippy::nursery, clippy::cargo)]
#![warn(missing_docs)]
#![doc = include_str!("../README.md")]
#![allow(clippy::too_many_arguments)]

use std::error::Error;

use basic_block::BBProgram;
use bril_rs::Program;

/// The internal representation of brilirs, provided a ```TryFrom<Program>``` conversion
pub mod basic_block;
/// Provides ```check::type_check``` to validate [Program]
pub mod check;
#[doc(hidden)]
pub mod cli;
mod error;
/// Provides ```interp::execute_main``` to execute [Program] that have been converted into [BBProgram]
pub mod interp;

#[doc(hidden)]
pub fn run_input<T: std::io::Write>(
  input: Box<dyn std::io::Read>,
  out: T,
  input_args: Vec<String>,
  profiling: bool,
  check: bool,
  text: bool,
) -> Result<(), Box<dyn Error>> {
  // It's a little confusing because of the naming conventions.
  //      - bril_rs takes file.json as input
  //      - bril2json takes file.bril as input
  let prog: Program = if text {
    bril2json::parse_abstract_program_from_read(input, true).try_into()?
  } else {
    bril_rs::load_abstract_program_from_read(input).try_into()?
  };
  let bbprog: BBProgram = prog.try_into()?;
  check::type_check(&bbprog)?;

  if !check {
    interp::execute_main(&bbprog, out, &input_args, profiling)?;
  }

  Ok(())
}
