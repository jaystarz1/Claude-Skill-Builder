#!/bin/bash
# Quick launcher for Skills Builder CLI

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

python3 -m code.cli "$@"
