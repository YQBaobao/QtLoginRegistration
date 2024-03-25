#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtLoginRegistration 
@ File        : login_register.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import datetime
from threading import Thread

import bcrypt
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QDialog
from email_validator import validate_email, EmailNotValidError

from crud.crud import CRUDUser, CRUDConfirmString
from db import session_factory, models, schemas
from lib import crypto
from lib.basic_function import BasicFunction
from lib.lib import check_code
from lib.send_email import SendEmail
from uis.LoginRegisterEmail import Ui_LoginRegister


class UiLoginRegisterQDialog(QDialog, Ui_LoginRegister):
    """界面逻辑"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.init_ui()
        self.basic_function = BasicFunction(self)
        self.user = CRUDUser()
        self.confirm_string = CRUDConfirmString()
        self.send_email = SendEmail()

    def init_ui(self):
        """初始化"""
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)  # 去掉 QDialog 帮助问号
        self.stackedWidget.setCurrentIndex(0)  # 默认登录页
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))  # 切换登录页
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))  # 切换注册页
        self.pushButtonForget.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))  # 切换忘记密码页
        self.init_time()

        # 登录页需要绑定的信号
        self.pushButtonLogin.clicked.connect(self.login)

        # 注册页需要绑定的信号
        self.lineEdit_3.textEdited.connect(
            lambda: self.check_password(self.lineEdit_3, self.lineEdit_4, self.label_9, self.pushButtonRegister))
        self.lineEdit_4.textEdited.connect(
            lambda: self.check_password(self.lineEdit_3, self.lineEdit_4, self.label_9, self.pushButtonRegister))
        self.pushButtonSend.clicked.connect(lambda: self.send_captcha(self.lineEdit_2, self.pushButtonSend))
        self.pushButtonRegister.clicked.connect(self.register)

        # 忘记密码页绑定信号
        self.lineEdit_7.textEdited.connect(
            lambda: self.check_password(self.lineEdit_7, self.lineEdit_8, self.label_14, self.pushButtonForgetOk))
        self.lineEdit_8.textEdited.connect(
            lambda: self.check_password(self.lineEdit_7, self.lineEdit_8, self.label_14, self.pushButtonForgetOk))
        self.pushButtonSend2.clicked.connect(lambda: self.send_captcha(self.lineEdit_6, self.pushButtonSend2))
        self.pushButtonForgetOk.clicked.connect(self.forget_password)

        # 窗口切换信号
        self.stackedWidget.currentChanged.connect(self.update_stacked_widget)

        # 记住
        self.accounts = 'remember.db'
        self.table = 'remember'
        crypto.create_db(self.accounts, self.table)  # 创建存储库
        self.remember_init()

    def update_stacked_widget(self):
        self.lineEditUsername.clear()
        self.lineEditPassword.clear()
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.lineEdit_9.clear()

    def init_time(self):
        self.count = 60
        self.time = QTimer(self)
        self.time.setInterval(1000)

    def login(self):
        """登录动作"""
        if not self.login_required():  # 必填校验未通过
            return
        try:
            info = validate_email(self.account, check_deliverability=False)
            email = info.normalized
            with session_factory() as db:
                user = self.user.get_user_by_email(db, email)
        except EmailNotValidError:  # 输入的是否是邮箱，不是将报错
            with session_factory() as db:
                user = self.user.get_user_by_username(db, self.account)

        if not user:  # 查询空，无此用户
            self.basic_function.info_message("用户名或密码错误")
            return
        if not user.disabled:
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
        self.remember()

    def login_required(self):
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

    def register(self):
        """注册动作"""
        if (not self.register_required() or
                not self.check_email_format() or
                not self.check_email_username_unique() or
                not self.check_captcha()):  # 数据校验
            return
        bytes_my_password = bytes(self.password, encoding="utf-8")
        bytes_my_hash_password = bcrypt.hashpw(bytes_my_password, bcrypt.gensalt(rounds=13))
        str_my_hash_password = bytes.decode(bytes_my_hash_password)
        user = schemas.UserRegister(
            username=self.username, password=str_my_hash_password, email=self.email, createTime=datetime.datetime.now())
        with session_factory() as db:
            self.user.create(db, user)
        # 注册成功后，判断是否选中直接登录,若未选中，则切换会登录页
        if self.checkBox_2.isChecked():
            self.accept()
        else:
            self.stackedWidget.setCurrentIndex(0)

    def register_required(self):
        """注册必填校验"""
        self.username = self.lineEdit.text()
        self.captcha = self.lineEdit_5.text()
        self.email = self.lineEdit_2.text()
        self.password = self.lineEdit_3.text()
        if not self.username.strip():
            self.basic_function.info_message("账号不能为空")
            return False
        elif not self.email.strip():
            self.basic_function.info_message("邮箱地址不能为空")
            return False
        elif not self.password.strip():
            self.basic_function.info_message("用户密码不能为空")
            return False
        elif not self.repeat_password.strip():
            self.basic_function.info_message("重复密码不能为空")
            return False
        elif not self.captcha.strip():
            self.basic_function.info_message("邮箱验证码不能为空")
            return False
        return True

    def check_email_format(self):
        """邮箱格式校验"""
        try:
            info = validate_email(self.email, check_deliverability=False)
            self.email = info.normalized
            return True
        except EmailNotValidError:
            self.basic_function.info_message("邮箱格式不正确，请重新输入")
            return

    def check_email_username_unique(self):
        """检查邮箱与账号是否已被注册"""
        with session_factory() as db:
            get_email = self.user.get_user_by_email(db, self.email)
            get_username = self.user.get_user_by_username(db, self.username)
        if get_email:
            self.basic_function.info_message("邮箱地址已存在")
            return
        if get_username:
            self.basic_function.info_message("账号已存在")
            return
        return True

    def check_captcha(self):
        """检查验证码"""
        with session_factory() as db:
            get_active_code = self.confirm_string.get_confirm_string_by_email(db, self.email)
        if not get_active_code:
            self.basic_function.info_message("验证码已失效，请重新发送邮件获取")
            return
        time_now = datetime.datetime.now()
        time_diff = get_active_code.activeValidityPeriod - time_now
        if not time_diff.seconds <= 5 * 60 or time_diff.days < 0:
            self.basic_function.info_message("验证码已过期，请重新发送邮件获取")
            self.confirm_string.update(db, self.email, {models.ConfirmString.deleted: '1'})
            return
        if self.captcha != get_active_code.activeCode:
            self.basic_function.info_message("验证码不正确，请重新输入")
            return
        self.confirm_string.update(db, self.email, {models.ConfirmString.deleted: '1'})
        return True

    def check_password(self, password_line_edit, old_password_line_edit, label, push_button):
        """重复密码的验证"""
        self.password = password_line_edit.text()
        self.repeat_password = old_password_line_edit.text()
        if self.password != self.repeat_password:
            label.setStyleSheet("color: rgb(255, 0, 0);")
            label.setText("两次密码输入不一致，重新输入！")
            push_button.setEnabled(False)
            return
        label.setText("")
        push_button.setEnabled(True)

    def send_captcha(self, email_line_edit, captcha_push_button):
        """发送验证码"""
        if not self.send_captcha_required(email_line_edit) or not self.check_email_format():  # 数据校验
            return
        self.time.timeout.connect(lambda: self.refresh_time(captcha_push_button))
        if captcha_push_button.isEnabled():
            self.time.start()
            captcha_push_button.setEnabled(False)
        captcha = check_code()
        self.save_captcha(captcha)
        # 发送邮件是一个耗时操作，为了避免阻塞，于是定义一个线程来实现
        thread = Thread(
            target=self.send_email.send_active_email,
            args=(captcha, self.email,)
        )
        thread.start()

    def refresh_time(self, captcha_push_button):
        if self.count > 0:
            captcha_push_button.setText(str(self.count) + '秒后重发')
            self.count -= 1
        else:
            self.time.stop()
            captcha_push_button.setEnabled(True)
            captcha_push_button.setText('发送')
            self.count = 60

    def send_captcha_required(self, email_line_edit):
        self.email = email_line_edit.text()
        if not self.email.strip():
            self.basic_function.info_message("邮箱地址不能为空")
            return False
        return True

    def save_captcha(self, captcha):
        """更新数据库验证码"""
        active_valid_time = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        confirm_string = schemas.ConfirmString(
            email=self.email, activeCode=captcha, activeValidityPeriod=active_valid_time,
            createTime=datetime.datetime.now())
        with session_factory() as db:
            # 每点击一次发送，就将旧的删除
            self.confirm_string.update(db, self.email, {models.ConfirmString.deleted: 1})
            # 保存信息
            self.confirm_string.create(db, confirm_string)

    def forget_password(self):
        """忘记密码动作"""
        if (not self.forget_password_required() or
                not self.forget_password_check_email_exist() or
                not self.check_email_format() or
                not self.check_captcha()):  # 数据校验
            return
        bytes_my_password = bytes(self.password, encoding="utf-8")
        bytes_my_hash_password = bcrypt.hashpw(bytes_my_password, bcrypt.gensalt(rounds=13))
        str_my_hash_password = bytes.decode(bytes_my_hash_password)
        with session_factory() as db:
            self.user.update(db, self.email, {models.User.password: str_my_hash_password})
        # 判断是否选中找回密码后直接登录,若未选中，则切换会登录页
        if self.checkBox_3.isChecked():
            self.accept()
        else:
            self.stackedWidget.setCurrentIndex(0)

    def forget_password_check_email_exist(self):
        """检查邮箱是否注册"""
        with session_factory() as db:
            get_email = self.user.get_user_by_email(db, self.email)
        if not get_email:
            self.basic_function.info_message("邮箱地址系统中不存在")
            return
        return True

    def forget_password_required(self):
        self.email = self.lineEdit_6.text()
        self.password = self.lineEdit_7.text()
        self.captcha = self.lineEdit_9.text()
        if not self.email.strip():
            self.basic_function.info_message("邮箱地址不能为空")
            return False
        elif not self.password.strip():
            self.basic_function.info_message("用户密码不能为空")
            return False
        elif not self.repeat_password.strip():
            self.basic_function.info_message("重复密码不能为空")
            return False
        elif not self.captcha.strip():
            self.basic_function.info_message("邮箱验证码不能为空")
            return False
        return True

    def remember_init(self):
        """初始化"""
        if not self.remember_required():
            return
        self.lineEditUsername.setText(self.username)
        self.lineEditPassword.setText(self.password)
        return True

    def remember(self):
        """记住"""
        if not self.checkBox.isChecked():
            crypto.delete_db(self.accounts, self.table)
            return
        crypto.delete_db(self.accounts, self.table)
        crypto.insert_db(self.accounts, self.table, self.account, self.password)

    def remember_required(self):
        """参数校验"""
        try:
            self.username, self.password = crypto.decrypt(self.accounts, self.table)
            if not self.username.strip() or not self.password.strip():
                return False
        except IndexError:
            return False
        return True
