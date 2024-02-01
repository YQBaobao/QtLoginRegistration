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
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButtonLogin.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.page_register)
        self.pushButtonRegister.clicked.connect(self.register)
        self.pushButtonForget.clicked.connect(self.page_forget_password)

    def login(self):
        """登录动作"""
        pass

    def register(self):
        """注册动作"""
        pass

    def page_register(self):
        """注册页"""
        self.stackedWidget.setCurrentIndex(1)

    def page_forget_password(self):
        """忘记密码"""
        self.stackedWidget.setCurrentIndex(2)
