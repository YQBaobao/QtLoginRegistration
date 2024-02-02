#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtLoginRegistration 
@ File        : main.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import sys

from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QApplication, QDialog

from core.login_register import UiLoginRegisterQDialog
from main_window import MainWindow
from static.resources_rc import qInitResources

qInitResources()  # 加载资源


def read_qss_file(qss_file_name):
    """读取qss"""
    with open(qss_file_name, 'r', encoding='UTF-8') as file:
        return file.read()


class StartupMainWindow(object):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)

        self.login_register_ui = UiLoginRegisterQDialog()  # 设置登录
        self.window = MainWindow()  # 系统主窗口

        self.login_ui()
        if self.login_register_ui.exec() == QDialog.Accepted:  # 登录校验是否通过
            self.main_ui()

    def login_ui(self):
        """登录"""
        qss = QFile(':/QSS/qss/login_register.qss')  # 资源使用 QFile 打开
        if qss.open(QFile.ReadOnly | QFile.Text):
            style_bytearray = qss.readAll()  # 类型为 QByteArray
            style = str(style_bytearray, encoding='UTF-8')
            self.login_register_ui.setStyleSheet(style)  # 设置样式
        qss.close()

    def main_ui(self):
        """主窗口"""
        self.window.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    StartupMainWindow()
