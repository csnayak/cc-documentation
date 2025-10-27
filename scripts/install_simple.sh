#!/bin/bash

# Ultra-Simple Python 3.13 and Cloud Custodian Installation
# Completely avoids system pip conflicts

echo "=== Ultra-Simple Installation ==="
echo "Installing Python 3.13 and Cloud Custodian..."

# Update and install Python 3.13
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.13 python3.13-venv

# Create virtual environment (this will bootstrap pip automatically)
echo "Creating virtual environment..."
python3.13 -m venv ~/cloud-custodian-env

# Activate and install Cloud Custodian
echo "Installing Cloud Custodian in virtual environment..."
source ~/cloud-custodian-env/bin/activate

# The virtual environment should have its own pip
pip install c7n==0.9.47.0 

echo "Verifying installation..."
custodian version

deactivate

# Add alias to .bashrc
echo 'alias activate-custodian="source ~/cloud-custodian-env/bin/activate"' >> ~/.bashrc

echo ""
echo "✅ Installation complete!"
echo ""
echo "To use:"
echo "1. source ~/.bashrc"
echo "2. activate-custodian"
echo "3. custodian --help"
