import os
import json
import pymysql
from dao.db import getConnection

def getConnection():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
                           )

def getSungjuk():
    conn = getConnection()
    cur = conn.cursor()
    cur.callproc("student_select")
    if (cur.rowcount):
        result = cur.fetchall()
        result_rowcount = cur.rowcount
        print("rowcount = ", result_rowcount)
    else:
        result = []
        print("rowcount = ", cur.rowcount)
    cur.close()
    conn.close()
    return result

def setSungjuk(sungData):
    conn = getConnection()
    cur = conn.cursor()
    args = (sungData['name'], sungData['kor'], sungData['mat'], sungData['eng'],
            sungData['schoolcode'], 0)
    cur.callproc("student_insert", args)
    result = cur.rowcount
    print(result)
    cur.close()
    conn.close()
    return result

def getBunhoSungjuk(bunho):
    conn = getConnection()
    cur = conn.cursor()
    args = [(bunho)]
    cur.callproc("select_with_bunho", args)
    if (cur.rowcount):
        result = cur.fetchall()
        print(result) # debugging
    else:
        result = []
    cur.close()
    conn.close()
    return result

def update_Bunho_Name(bunho, name):
    conn = getConnection()
    cur = conn.cursor()
    try:
        args = (bunho, name, 0)
        cur.callproc("sungjuk_with_bunho", args)
        cur.execute("SELECT @_sungjuk_with_bunho_2")
        result = cur.fetchone()[0]
        conn.commit()
        return result
    finally:
        cur.close()
        conn.close()
        
def delete_Bunho_Sungjuk(bunho):
    conn = getConnection()
    cur = conn.cursor()
    try:
        args = (bunho, 0)
        cur.callproc("delete_with_bunho", args)
        cur.execute("SELECT @_delete_with_bunho_1")
        result = cur.fetchone()[0]
        conn.commit()
        return result
    finally:
        cur.close()
        conn.close()