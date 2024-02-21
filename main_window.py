#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtLoginRegistration 
@ File        : main_window.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QWidget, QDialog

from core.login_register import UiLoginRegisterQDialog
from uis.MianWindow import Ui_MainWindow


class MainWindow(QWidget, Ui_MainWindow):
    """界面逻辑"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.logout)

    def logout(self):
        """退出"""
        self.hide()
        login_register_ui = UiLoginRegisterQDialog()  # 设置登录

        qss = QFile(':/QSS/qss/login_register.qss')  # 资源使用 QFile 打开
        if qss.open(QFile.ReadOnly | QFile.Text):
            style_bytearray = qss.readAll()  # 类型为 QByteArray
            style = str(style_bytearray, encoding='UTF-8')
            login_register_ui.setStyleSheet(style)
        qss.close()
        if login_register_ui.exec() == QDialog.Accepted:
            login_register_ui.close()
            self.show()
