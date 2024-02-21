#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtLoginRegistration 
@ File        : __init__.py.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from setting import CONFIG

# 创建连接
engine = create_engine(
    url=CONFIG.SQLALCHEMY_DATABASE_URI,
    pool_size=CONFIG.SQLALCHEMY_POOL_SIZE,
    max_overflow=CONFIG.SQLALCHEMY_MAX_OVERFLOW,
    pool_recycle=CONFIG.SQLALCHEMY_POOL_RECYCLE,
    pool_timeout=CONFIG.SQLALCHEMY_POOL_TIMEOUT,
    pool_pre_ping=CONFIG.SQLALCHEMY_POOL_PRE_PING,
    echo=CONFIG.SQLALCHEMY_ECHO,
    echo_pool=CONFIG.SQLALCHEMY_ECHO_POOL
)

# 连接会话
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


# 上下文管理，管理会话
@contextmanager
def session_factory():
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
