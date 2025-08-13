#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt

echo "Setup complete. You can now run 'python scripts/sync_runner.py'"
