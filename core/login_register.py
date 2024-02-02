#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtLoginRegistration 
@ File        : login_register.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from uis.LoginRegisterEmail import Ui_LoginRegister


class UiLoginRegisterQDialog(QDialog, Ui_LoginRegister):
    """界面逻辑"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.init_ui()

    def init_ui(self):
        """初始化"""
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)  # 去掉 QDialog 帮助问号
        self.stackedWidget.setCurrentIndex(0)  # 默认登录页
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))  # 切换登录页
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))  # 切换注册页
        self.pushButtonForget.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))  # 切换忘记密码页
