#!/bin/bash

# Exit on error
set -e

# Directory for the virtual environment
VENV_DIR=".venv"

# Which Python executable to use
PYTHON_BIN="python3.10"

# Function to check that python3.10 and venv support are available
check_python_venv() {
    if ! command -v $PYTHON_BIN >/dev/null 2>&1; then
        echo "🚫 $PYTHON_BIN not found. Please install Python 3.10."
        echo "   On Debian/Ubuntu: sudo apt-get install python3.10 python3.10-venv"
        echo "   On macOS (Homebrew): brew install python@3.10"
        exit 1
    fi

    # Check that venv module is available in python3.10
    if ! $PYTHON_BIN - <<<'import venv' 2>/dev/null; then
        echo "🚫 The venv module is not available in $PYTHON_BIN."
        echo "   On Debian/Ubuntu: sudo apt-get install python3.10-venv"
        exit 1
    fi

    echo "✅ $PYTHON_BIN with venv support detected."
}

# Function to create (or recreate) the .venv
create_or_recreate_venv() {
    if [ -d "$VENV_DIR" ]; then
        echo "🔁 Removing existing virtualenv at '$VENV_DIR'"
        rm -rf "$VENV_DIR"
    fi

    echo "🐍 Creating new virtualenv with $PYTHON_BIN in '$VENV_DIR'"
    $PYTHON_BIN -m venv "$VENV_DIR"
    echo "✅ Virtualenv created."
}

# Function to activate venv and install requirements
install_requirements() {
    # Activate the venv
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"

    echo "📦 Upgrading pip in the virtualenv..."
    pip install --upgrade pip

    if [ -f "requirements.txt" ]; then
        echo "📥 Installing requirements from requirements.txt..."
        pip install -r requirements.txt
        echo "✅ Requirements installed."
    else
        echo "⚠️  No requirements.txt found. Skipping installation."
    fi

    # Deactivate after install
    deactivate
}

# Main
check_python_venv
create_or_recreate_venv
install_requirements

echo "🎉 Installation complete! To start using the environment, run:"
echo "    source $VENV_DIR/bin/activate"