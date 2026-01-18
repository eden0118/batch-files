#!/bin/bash
# Build macOS application package for Batch Renamer

set -e

echo "=========================================="
echo "Building Batch Renamer for macOS"
echo "=========================================="

# Install dependencies if needed
echo "Installing dependencies..."
pip3 install -q flet pyinstaller

# Clean up previous builds
echo "Cleaning up previous builds..."
rm -rf build dist "Batch Renamer.app"

# Build the application using python3 -m pyinstaller
echo "Building application..."
python3 -m PyInstaller \
    --name "Batch Renamer" \
    --onedir \
    --windowed \
    --add-data "flet/main.py:." \
    --osx-bundle-identifier "com.batchrenamer.app" \
    --collect-all flet \
    flet/main.py

# Create a DMG (optional)
if command -v hdiutil &> /dev/null; then
    echo "Creating DMG installer..."
    cd dist
    hdiutil create -volname "Batch Renamer" -srcfolder . -ov -format UDZO "Batch Renamer.dmg"
    echo "DMG created: dist/Batch Renamer.dmg"
    cd ..
fi

echo "=========================================="
echo "Build complete!"
echo "Application: dist/Batch Renamer.app"
echo "=========================================="
