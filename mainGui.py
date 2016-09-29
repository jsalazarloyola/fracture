#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gui.mainWindow import MainApp

############################################################
# Definitions
# Colors
BACK = [1,1,1,1]
FRONT = [0,0,0,0.8]
LIGHT = [0,0,0,0.2]
CYAN = [0,0.5,0.5,0.2]
BLUE = [0,0,1,0.3]

if __name__ == "__main__":
    window = MainApp(BACK, FRONT, LIGHT)

    window.start()
