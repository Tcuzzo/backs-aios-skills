#!/bin/sh
set -eu
# BACKS managed credential helper.
# The launcher restores the bound project AND Python environment. Never invoke
# bare python3 here: VS Code's extension host need not activate the terminal venv.
exec "$HOME/.local/bin/backs-provider" __key
