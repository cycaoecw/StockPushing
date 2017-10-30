#!/usr/bin/python3
#encoding=utf-8

import pymysql

def getResults(sql):
	  # 打开数据库连接
      #db = pymysql.connect("112.74.13.22","admin","admin123","tradeplatform",charset='utf8')
      db = pymysql.connect("119.23.73.195","root","cyPython!","stockpush",charset='utf8')

    # 使用cursor()方法获取操作游标
      cursor = db.cursor()
	  # 执行SQL语句
      cursor.execute(sql)
      return  cursor

def generate_dicts(cur):
    fieldnames = [d[0].lower() for d in cur.description]
    while True:
        rows = cur.fetchmany()
        if not rows: return
        for row in rows:
            yield dict(zip(fieldnames, row))

def getResultWithAllData(sql):
    # 打开数据库连接
    #db = pymysql.connect("112.74.13.22", "admin", "admin123", "tradeplatform", charset='utf8')
    db = pymysql.connect("119.23.73.195", "root", "cyPython!", "stockpush", charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # 执行SQL语句
    cursor.execute(sql)

    return cursor.fetchall()


def executeSql(sql):
    #db = pymysql.connect("112.74.13.22", "admin", "admin123", "tradeplatform", charset='utf8')
    db = pymysql.connect("119.23.73.195", "root", "cyPython!", "stockpush", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    returnResult = False
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        returnResult = True
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()
    return  returnResult