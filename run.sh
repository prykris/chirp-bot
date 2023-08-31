#!/bin/bash

# Detect the operating system
OS="$(uname)"

# Activate virtual environment
if [[ "$OS" == "Linux" ]] || [[ "$OS" == "Darwin" ]]; then
    source venv/bin/activate
elif [[ "$OS" == MINGW64_NT-10.0* ]] || [[ "$OS" == CYGWIN_NT-10.0* ]] || [[ "$OS" == MSYS_NT-10.0* ]]; then
    source venv/Scripts/activate
else
    echo "OS not recognized: $OS"
    exit 1
fi

if ! python -c "import selenium" &> /dev/null; then
    pip install -r requirements.txt
fi

# Navigate to src directory and run main Python script
cd src || exit 1

echo "Running main.py"

python main.py
