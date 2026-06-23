import Lake
open Lake DSL

package «MarkedRootedClosure» where
  version := v!"2.4.2"

lean_lib «MarkedRootedClosure» where
  roots := #[`MarkedRootedClosure]

/-- Exact upstream proof dependency. The commit, Lean toolchain, and Mathlib
    revision are recorded again in `archive/UPSTREAM.lock`. -/
require «YangMills» from git
  "https://github.com/lluiseriksson/THE-ERIKSSON-PROGRAMME.git" @
    "4e45246aa109671d25fcd01ba1abf7bc3f8506d1"
