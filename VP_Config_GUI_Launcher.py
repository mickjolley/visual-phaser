#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VP_Config_GUI_Launcher.py - Launcher for Visual Phaser Configuration GUI

This script provides a standalone entry point for the VP Config GUI application.
Run this script to launch the configuration editor.

Usage:
    python VP_Config_GUI_Launcher.py [config_file_path]

Optional arguments:
    config_file_path - Path to VP_configV1.py file to load on startup
                      (defaults to VP_configV1.py in same directory)
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    import wx
except ImportError:
    print("ERROR: wxPython is not installed.")
    print("Install it with: pip install wxPython")
    sys.exit(1)

# Import the Boa-managed GUI module
from VP_Config_GUI_Boa import VPConfigBoaApp


def main():
    """Launch the VP Config GUI application"""
    app = VPConfigBoaApp(False)

    # If config file path provided as argument, pass it to the frame
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        if os.path.exists(config_path):
            app.frame.config_path = config_path
            app.frame.LoadConfig()

    app.MainLoop()


if __name__ == '__main__':
    main()
