# Repository maintenance

Dependabot checks Python test dependencies and GitHub Actions weekly. Minor and
patch Python updates are grouped; major updates remain separate for review.
Updates arrive as pull requests and must pass the existing checks before merging.

The CI workflow installs the test requirements on Python 3.11 and 3.12, checks
installed dependency compatibility with `pip check`, and runs the pack tests.
It also checks the shell and PowerShell installers and JavaScript hooks.
Run the complete test suite on Linux: provider update tests use `fcntl`.

Before publishing a change:

1. Install `tests/requirements.txt` in a fresh virtual environment.
2. Run `python -m pip check` and `python -m pytest tests -q`.
3. Run `git diff --check`. Resolve any merge conflicts, then rerun tests on the
   resolved result.
4. For skill or play changes, update `docs/FLOWCHARTS.md`. The documentation
   test compares links with the actual source inventory, including stale links.

Enable the shipped local hooks with `git config core.hooksPath .githooks`.
CI still checks full commit history even when local hooks were not enabled.
The hygiene guard must remain enforced: historical policy violations need an
explicitly approved history repair, not a reduced scan or an unapproved exception.
Rewriting shared history changes commit IDs and requires coordination with other
contributors; routine dependency maintenance must not perform it automatically.
