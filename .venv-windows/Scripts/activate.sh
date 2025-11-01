#!/usr/bin/env bash
VENV_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export VIRTUAL_ENV="${VENV_DIR%/Scripts}"
export PATH="$VIRTUAL_ENV/Scripts:$PATH"
export PS1="(.venv) $PS1"
