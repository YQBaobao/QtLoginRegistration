#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtLoginRegistration
@ File        : schemas.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 创建初始 Pydantic模型,用于关联ORM
"""
from datetime import datetime
from typing import Union

from pydantic import BaseModel, ConfigDict


# ConfirmString Pydantic模型
class ConfirmString(BaseModel):
    email: str
    activeCode: str
    activeValidityPeriod: datetime
    createTime: datetime
    deleted: int = 0

    model_config = ConfigDict(from_attributes=True, )


# UserRegister Pydantic模型
class UserRegister(BaseModel):
    """注册"""
    username: str
    password: str
    email: str
    name: Union[str, None] = None
    sex: Union[int, None] = 1
    disabled: int = 1
    createTime: datetime
    deleted: int = 0

    model_config = ConfigDict(from_attributes=True, )
