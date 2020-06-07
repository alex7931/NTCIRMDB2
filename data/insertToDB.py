import pymongo
import pandas as pd

con = pymongo.MongoClient("mongodb://localhost:27017/")
# make a connection instance firstly
db = con.ntcir


# data simples for each table.
ntcir = db.ntcir
#{ "_id" : ObjectId("5a362a87a824642d076e3057"), "title" : "clueweb12-0814wb-34-25099", "url" : "clueweb12-0814wb-34-25099.html", "topic_id" : "53", "title_id" : "173", "topic" : "absolute neutrophils" }
table = db.table
#{ "_id" : ObjectId("5a362d0aa824642daf40d8fa"), "table" : "migrate abroad#", "table_id" : "116" }
# user=db.user
# #{ "_id" : ObjectId("5a3b5ef9a8246430d0d26e05"), "username" : "user18", "password" : "19970127ss", "email" : "sandy2142@qq.com", "sex" : "male", "name" : "Chen Yuxuan", "age" : 21, "user_groups" : [ "normal_user" ], "signup_time" : ISODate("2017-12-21T16:12:57.836Z"), "last_login" : ISODate("2018-01-01T20:05:52.783Z"), "login_num" : 7 }
# usr=db.usr
# #{ "_id" : ObjectId("597592fba82464466b276b93"), "topicid" : "18", "docid" : "21", "usrid" : "user09", "val" : "REL", "color" : "Green" }
usrlist=db.usrlist
#{ "_id" : ObjectId("5a38f230a8246430d0d26df3"), "usrid" : "user17", "usrl" : "102,112,122,132,142,152,162,172,182,192" }
# usrlog=db.usrlog
# #{ "_id" : ObjectId("5975a451a82464466b276d03"), "topicid" : "18", "docid" : "125", "usrid" : "user09", "val" : "post", "time" : "2017-07-24 16:40:01" }

from bs4 import BeautifulSoup

# read query id and query content from xml file
fi = open('./www2www3topics-E.xml','rb')
bs = BeautifulSoup(fi.read())
dt={}
for i in bs.find_all('query'):
    dt[i.find('qid').text]=[i.find('content').text,i.find('description').text]


#insert *table (table name)* this table is used for menu page of ply, key "table" is description of topic, table id
#is topic id, ensure table id and table are unique. Here we keep 2 topic lists, "0001" for randompool and "10001" for sortpool
#pool
# table -> {table,table_id}
for qid in dt.keys():
    # random pool
    temp={  "table" : "T1: "+dt[qid][0] + " D: "+dt[qid][1], "table_id" : str(int(qid)) }
    table.insert(temp)
    # sort pool
    temp = {"table": "T2: " + dt[qid][0] + " D: " + dt[qid][1], "table_id": str(int('1'+qid))}
    table.insert(temp)
print("insert table done")

#inset ntcir
# ntcir-> {title: document id like "clueweb12-0814wb-34-25099.html"; url: html path;topic_id: query id (same as above table_id)
# title_id: document id in topic from 1 to n: topic: same as above key table }
f = open('./Eruns.pd15.randpool.catpool','r')
preID='0001'
c=0
for line in f.readlines():
    qid,did=line.split()
    if qid!=preID:
        c=1
        preID=qid
    else:
        c+=1
    temp={ "title" : did, "url" : did+'.html', "topic_id" : str(int(qid)), "title_id" : str(c), "topic" : "T1: "+dt[qid][0] + " D: "+dt[qid][1]}
    ntcir.insert(temp)

f = open('./Eruns.pd15.sortpool.catpool','r')
preID='0001'
c=0
for line in f.readlines():
    qid,did=line.split()
    if qid!=preID:
        c=1
        preID=qid
    else:
        c+=1
    temp={ "title" : did, "url" : did+'.html', "topic_id" : str(int('1'+qid)), "title_id" : str(c), "topic" : "T2: "+dt[qid][0] + " D: "+dt[qid][1]}
    ntcir.insert(temp)
print("insert ntcir done")

# insert users
users1 = pd.read_csv('users1.csv')
users2 = pd.read_csv('users2.csv')
users3 = pd.read_csv('users3.csv')
user_assignments = [users1, users2, users3]

users = {}
for df in user_assignments:
    topic_id = []
    for id_num in df["topicid"].tolist():
        d = 4 - len(str(id_num))
        id_str = '0' * d + str(id_num)
        topic_id.append(id_str)
    for user_id in list(df.columns[1:]):
        temp_topics = [ids for ids in topic_id]
        sort_or_random = df[user_id].tolist()
        for idx, flag in enumerate(sort_or_random):
            if flag:
                temp_topics[idx] = '1' + topic_id[idx]
        users[user_id] = temp_topics

for usr in users.keys():
    temp = { "usrid" : usr, "usrl" : ','.join([str(int(i)) for i in users[usr]]) }
    print("insert: ", temp)
    usrlist.insert(temp)
# test user
temp = {"usrid" : 'user00', "usrl" : ','.join([str(int(str(i).rjust(4,'0')) )for i in range(1,81)]+[str(int('1'+str(i).rjust(4,'0'))) for i in range(1,81)])}
usrlist.insert(temp)

