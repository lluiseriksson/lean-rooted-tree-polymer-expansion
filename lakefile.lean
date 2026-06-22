import Lake
open Lake DSL

package «MarkedRootedClosure» where
  version := v!"1.0.0"

lean_lib «MarkedRootedClosure» where
  roots := #[`MarkedRootedClosure]

/-- Exact upstream proof dependency.  The commit, Lean toolchain, and Mathlib
    commit are recorded again in `archive/UPSTREAM.lock`. -/
require «YangMills» from git
  "https://github.com/lluiseriksson/THE-ERIKSSON-PROGRAMME.git" @
    "83d18a113e3fa22ada23b13361fb84015a1c80ed"
