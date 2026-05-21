#!/bin/bash
set -e

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "Building ExarotonRemote.app ..."
python3 -m PyInstaller \
    --windowed \
    --name "ExarotonRemote" \
    --collect-all customtkinter \
    --collect-all pystray \
    --hidden-import PIL \
    --hidden-import PIL._imagingtk \
    app.py

echo ""
echo "Done! Find ExarotonRemote.app in the dist/ folder."
echo "Drag it to your Applications folder to install, or double-click to run."
