#!/bin/bash

# Exit on error
set -e

# Function to check if conda is installed
check_conda_installed() {
    if command -v conda >/dev/null 2>&1; then
        echo "✅ Conda is already installed."
    else
        echo "🚫 Conda not found. Installing Miniconda..."
        install_miniconda
    fi
}

# Function to install Miniconda
install_miniconda() {
    OS_TYPE=$(uname)
    if [ "$OS_TYPE" == "Linux" ]; then
        MINICONDA_SCRIPT="Miniconda3-latest-Linux-x86_64.sh"
    elif [ "$OS_TYPE" == "Darwin" ]; then
        MINICONDA_SCRIPT="Miniconda3-latest-MacOSX-x86_64.sh"
    else
        echo "Unsupported OS: $OS_TYPE"
        exit 1
    fi

    wget https://repo.anaconda.com/miniconda/$MINICONDA_SCRIPT -O miniconda.sh
    bash miniconda.sh -b -p $HOME/miniconda
    rm miniconda.sh
    export PATH="$HOME/miniconda/bin:$PATH"
    echo 'export PATH="$HOME/miniconda/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    echo "✅ Miniconda installed."
}

# Function to install Python requirements
install_requirements() {
    ENV_NAME="senior-project-ui-evluation"

    echo "🔍 Checking if conda environment '$ENV_NAME' exists..."
    if conda info --envs | grep -q "^$ENV_NAME[[:space:]]"; then
        echo "🔁 Switching to 'base' environment before removal..."
        source "$(conda info --base)/etc/profile.d/conda.sh"
        conda activate base

        echo "🗑️ Removing existing environment: $ENV_NAME"
        conda remove --name $ENV_NAME --all -y
    fi

    echo "🐍 Creating new conda environment: $ENV_NAME"
    conda create -y -n $ENV_NAME python=3.10

    echo "✅ Environment '$ENV_NAME' created."

    echo "📦 Installing Python requirements into '$ENV_NAME'..."
    if [ -f "requirements.txt" ]; then
        # Activate env in subshell to keep it clean
        echo "🔁 Switching to '$ENV_NAME' environment before activation..."
        source "$(conda info --base)/etc/profile.d/conda.sh"
        conda activate $ENV_NAME

        conda install --yes --file requirements.txt || pip install -r requirements.txt
        echo "✅ Requirements installed in '$ENV_NAME'"
    else
        echo "⚠️  No requirements.txt found. Skipping requirements installation."
    fi
}

# Start installation process
check_conda_installed
install_requirements

echo "🎉 Installation complete!"