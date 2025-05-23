#!/bin/bash

# SoulCoreLegacy Arcade Runner Script
echo "Starting SoulCoreLegacy Arcade..."
echo "--------------------------------"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pygame is installed
python3 -c "import pygame" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Installing pygame..."
    pip3 install pygame
fi

# Run the game
cd "$(dirname "$0")"
python3 main.py

echo "Game closed."
