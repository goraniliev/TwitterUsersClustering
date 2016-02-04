# -*- coding: utf-8 -*-
from db.connection import get_connection

__author__ = 'goran'

def is_inserted(id_user):
    db = get_connection()
    cursor = db.cursor()
    sql = """select count(*) cnt from user where iduser=%s"""
    cursor.execute(sql, (id_user))

    count = 0

    for cnt in cursor:
        count = cnt[0]

    cursor.close()
    db.close()

    return count == 1