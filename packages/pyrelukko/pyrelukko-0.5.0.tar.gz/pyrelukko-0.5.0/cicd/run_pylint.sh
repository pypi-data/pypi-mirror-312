#!/bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
REPO_DIR="${SCRIPT_DIR}/.."

# Main script execution
main() {
    pylint --verbose \
            --rcfile "${REPO_DIR}/pyproject.toml" \
            --output-format=json:pylint.out.json,parseable:pylint.out.txt,text \
            "${REPO_DIR}"
    pylint_exit_code=$?

    pylint-json2html \
        -o "${REPO_DIR}/pylint.out.html" \
        "${REPO_DIR}/pylint.out.json"

    return ${pylint_exit_code}
}

# Execute the main function
main

# vim:set softtabstop=4 shiftwidth=4 tabstop=4 expandtab: