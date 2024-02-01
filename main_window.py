#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtLoginRegistration 
@ File        : main_window.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtWidgets import QWidget

from uis.MianWindow import Ui_MainWindow


class MainWindow(QWidget, Ui_MainWindow):
    """界面逻辑"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
