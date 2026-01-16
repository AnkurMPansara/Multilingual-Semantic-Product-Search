#!/bin/bash

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating..."
    python -m venv .venv

    echo "Installing requirements..."
    source .venv/bin/activate
    pip install -r requirements.txt
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Load variables from .env file
if [ -f ".env" ]; then
    echo "Loading environment variables from .env..."
    export $(grep -v '^#' .env | xargs)
else
    echo "No .env file found, skipping..."
fi

# Run the application
echo "Running main.py..."
python main.py

# Pause equivalent (wait for user to press Enter)
read -p "Press [Enter] to continue..."
