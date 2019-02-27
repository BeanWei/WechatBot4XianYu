# coding:utf-8

from models import SQLBase, SQL_Engine

SQLBase.metadata.create_all(SQL_Engine)