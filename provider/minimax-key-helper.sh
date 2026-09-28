#!/bin/sh
set -eu
# BACKS managed MiniMax credential helper; uses the same bound project and Python.
# Credentials are resolved in memory from the existing BACKS environment only.
exec "$HOME/.local/bin/backs-provider" __minimax_key
