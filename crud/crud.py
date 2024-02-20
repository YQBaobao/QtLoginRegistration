#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtLoginRegistration 
@ File        : crud.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from typing import Union

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db import models, schemas


class CRUD(object):
    @staticmethod
    def _commit(db: Session, db_obj):
        try:
            db.commit()
            return db_obj
        except Exception:
            db.rollback()
            return


class CRUDUser(CRUD):

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Union[models.User, None]:
        """根据email查询用户"""
        return db.query(models.User).filter(and_(models.User.email == email, models.User.deleted == 0)).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Union[models.User, None]:
        """根据username查询用户"""
        return db.query(models.User).filter(and_(models.User.username == username, models.User.deleted == 0)).first()

    def create(self, db: Session, user: schemas.UserRegister):
        """用户创建"""
        db_user = models.User(**user.model_dump())
        db.add(db_user)
        return self._commit(db, db_user)

    def update(self, db: Session, email: str, update_data: dict):
        """更新"""
        db_user = db.query(models.User).filter(
            and_(models.User.email == email, models.User.deleted == 0)).update(update_data)
        return self._commit(db, db_user)


class CRUDConfirmString(CRUD):

    @staticmethod
    def get_confirm_string_by_email(db: Session, email: str) -> Union[models.ConfirmString, None]:
        """根据email获取验证码"""
        return db.query(models.ConfirmString).filter(
            and_(models.ConfirmString.email == email, models.ConfirmString.deleted == 0)).first()

    def create(self, db: Session, confirm_string: schemas.ConfirmString):
        """创建验证码保存"""
        db_confirm_string = models.ConfirmString(**confirm_string.model_dump())
        db.add(db_confirm_string)
        return self._commit(db, db_confirm_string)

    def update(self, db: Session, email: str, update_data: dict):
        """更新"""
        db_confirm_string = db.query(models.ConfirmString).filter(
            and_(models.ConfirmString.email == email, models.ConfirmString.deleted == 0)).update(update_data)
        return self._commit(db, db_confirm_string)
