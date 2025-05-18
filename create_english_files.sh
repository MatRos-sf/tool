#!/bin/bash

SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Path to english script
VENV_PATH="$SCRIPT_DIR/venv"
PYTHON_SCRIPT="$SCRIPT_DIR/create_english_files.py"


# Check if venv folder exists
if [ -d "$VENV_PATH" ]; then
    # Aktywacja venv
    if [ -f "$VENV_PATH/bin/activate" ]; then
        source "$VENV_PATH/bin/activate"
    elif [ -f "$VENV_PATH/Scripts/activate" ]; then
        source "$VENV_PATH/Scripts/activate"
    else
        echo "File 'activate' not found in venv folder."
        exit 1
    fi


    RAW_PATH="$1"

    # Run python script
    python "$PYTHON_SCRIPT" "$@"

    # Deaktywacja venv
    deactivate

else
    echo "venv ('$VENV_PATH')does not exist."
    exit 1
fi

exit 0