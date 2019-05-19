#!/usr/bin/python3
#coding=utf-8
import json
import argparse
import pymysql
from collections import defaultdict
from contextlib import contextmanager

@contextmanager
def get_conn(**kwargs):
    db=pymysql.connect(**kwargs)
    try:
        yield db
    finally:
        db.close()

def _argparse(des):
    parser=argparse.ArgumentParser(description=des)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list",action='store_true',help='List active servers')
    group.add_argument("--host",action='store',dest='server',help='List detail about the specific host')
    return parser.parse_args()

def to_json(in_dict):
    return json.dumps(in_dict,sort_keys=True,indent=2)

def get_host_information(db,server):
    detail={}
    with db.cursor() as cur:
        cur.execute('select * from hosts where host={0}'.format("'"+server+"'"))
        rows=cur.fetchall()
        if rows:
            no,host,group,user,port=rows[0]
            detail.update(ansible_user=user,ansible_port=port)
        return detail
    
def list_all_hosts(db):
    hosts=defaultdict(list)
    with db.cursor() as cur:
        cur.execute("select * from hosts")
        rows=cur.fetchall()
        for row in rows:
            no,host,group,user,port=row
            hosts[group].append(host)
        return hosts

def main():
    parser=_argparse("this is ansible file")
    with get_conn(host="127.0.0.1",user="root",passwd="!QAZxsw2",db="ansible") as db:
        if parser.list:
            hosts=list_all_hosts(db)
            print(to_json(hosts))
        else:
            detail=get_host_information(db,parser.server)
            print(to_json(detail))

if __name__=="__main__":
    main()
