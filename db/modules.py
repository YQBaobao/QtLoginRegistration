#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtLoginRegistration 
@ File        : modules.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column, Integer, String, DateTime

from db import Base


class User(Base):
    """用户表"""
    __tablename__ = 'user'  # 指定表名
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=True, comment='用户名称')
    username = Column(String(20), nullable=False, comment='用户账号')
    password = Column(String(255), nullable=False, comment='密码')
    email = Column(String(255), nullable=False, comment='邮箱')
    sex = Column(String(1), nullable=True, server_default='1', comment='性别:男1,女0')
    disabled = Column(String(1), nullable=False, server_default='1', comment='禁用用户:启动1,禁用0')

    createTime: str = Column(DateTime, nullable=False, comment='创建时间')
    deleted = Column(String(1), nullable=False, server_default='0', comment='删除标志')

    UniqueConstraint(username, name='usernameUnique')  # 账号唯一
    UniqueConstraint(email, name='emailUnique')  # 邮箱唯一

    def __repr__(self):
        return '<user %r,%r>' % (self.id, self.username)


if __name__ == '__main__':
    from db import engine

    Base.metadata.drop_all(bind=engine)  # 删除所有表
    Base.metadata.create_all(bind=engine)  # 创建所有表
