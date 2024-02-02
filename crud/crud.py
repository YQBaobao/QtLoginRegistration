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

from db import models


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
        return db.query(models.User).filter(and_(models.User.email == email, models.User.deleted == '0')).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Union[models.User, None]:
        """根据username查询用户"""
        return db.query(models.User).filter(and_(models.User.username == username, models.User.deleted == '0')).first()
