#!/usr/bin/env bash
set -e

VENV_DIR=".venv"
PYTHON_BIN="python3.10"

# 1) Ensure python3.10 is installed
if ! command -v $PYTHON_BIN >/dev/null 2>&1; then
    echo "🚫 '$PYTHON_BIN' not found. Please install Python 3.10 (with venv support)."
    echo "   • Debian/Ubuntu: sudo apt-get install python3.10 python3.10-venv"
    echo "   • macOS/Homebrew: brew install python@3.10"
    exit 1
fi

echo "✅ Found $PYTHON_BIN"

# 2) (Re)create the virtualenv
if [ -d "$VENV_DIR" ]; then
    echo "🔁 Removing existing virtualenv at '$VENV_DIR'"
    rm -rf "$VENV_DIR"
fi

echo "🐍 Creating virtualenv in '$VENV_DIR'…"

# Try stdlib venv first
if $PYTHON_BIN - <<<'import venv' 2>/dev/null; then
    echo "   • Using built-in venv"
    $PYTHON_BIN -m venv "$VENV_DIR"
else
    # Fallback to virtualenv
    echo "   • Built-in venv unavailable; falling back to virtualenv"
    echo "   • Installing virtualenv via pip"
    $PYTHON_BIN -m pip install --user virtualenv

    # Make sure ~/.local/bin is on PATH (where --user puts the script)
    export PATH="$HOME/.local/bin:$PATH"

    echo "   • Creating env with virtualenv"
    $PYTHON_BIN -m virtualenv -p "$PYTHON_BIN" "$VENV_DIR"
fi

echo "✅ Virtualenv created."

# 3) Activate & install requirements
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "📦 Upgrading pip…"
pip install --upgrade pip

if [ -f requirements.txt ]; then
    echo "📥 Installing from requirements.txt…"
    pip install -r requirements.txt
    echo "✅ Requirements installed."
else
    echo "⚠️  No requirements.txt found; skipping."
fi

deactivate

# 4) Done
echo "🎉 Done! To start using it, run:"
echo "    source $VENV_DIR/bin/activate"