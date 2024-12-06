#!/bin/bash

# SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
# REPO_DIR="${SCRIPT_DIR}/.."

# Main script execution
main() {
    # pytest --junit-xml "${REPO_DIR}/pytest-junit.xml"
    tox run --skip-missing-interpreters
}

# Execute the main function
main

# vim:set softtabstop=4 shiftwidth=4 tabstop=4 expandtab: