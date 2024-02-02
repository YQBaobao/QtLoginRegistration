#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtLoginRegistration 
@ File        : login_register.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import bcrypt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from email_validator import validate_email, EmailNotValidError

from crud.crud import CRUDUser
from db import SessionLocal
from lib.basic_function import BasicFunction
from uis.LoginRegisterEmail import Ui_LoginRegister


class UiLoginRegisterQDialog(QDialog, Ui_LoginRegister):
    """界面逻辑"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.init_ui()
        self.basic_function = BasicFunction(self)
        self.user = CRUDUser()

    def init_ui(self):
        """初始化"""
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)  # 去掉 QDialog 帮助问号
        self.stackedWidget.setCurrentIndex(0)  # 默认登录页
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))  # 切换登录页
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))  # 切换注册页
        self.pushButtonForget.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))  # 切换忘记密码页

        # 登录页需要绑定的信号
        self.pushButtonLogin.clicked.connect(self.login)

    def login(self):
        """登录动作"""
        if not self.required_login():  # 必填校验未通过
            return
        try:
            info = validate_email(self.account, check_deliverability=False)
            email = info.normalized
            with SessionLocal() as db:
                user = self.user.get_user_by_email(db, email)
        except EmailNotValidError:  # 输入的是否是邮箱，不是将报错
            with SessionLocal() as db:
                user = self.user.get_user_by_username(db, self.account)

        if not user:  # 查询空，无此用户
            self.basic_function.info_message("用户名或密码错误")
            return
        if user.disabled == '0':
            self.basic_function.info_message("此用户账号已被禁用")
            return
        bytes_my_password = bytes(self.password, encoding="utf-8")
        str_my_hash_password = user.password
        bytes_my_hash_password = bytes(str_my_hash_password, encoding='utf-8')
        check = bcrypt.checkpw(bytes_my_password, bytes_my_hash_password)
        if not check:  # 校验通过，设置QDialog对象状态为允许
            self.basic_function.info_message("用户名或密码错误")
            return
        self.accept()

    def update_login_config(self, password):
        """手动登录更新配置文件"""
        if not self.checkBox.isChecked():
            crypto.delete_db(self.accounts)
            return
        crypto.delete_db(self.accounts)
        crypto.insert_db(self.accounts, self.username, password)

    def required_login(self):
        """登录必填校验"""
        self.account = self.lineEditUsername.text()
        self.password = self.lineEditPassword.text()
        if not self.account.strip():
            self.basic_function.info_message("用户账号不能为空")
            return
        if not self.password.strip():
            self.basic_function.info_message("用户密码不能为空")
            return
        return True
