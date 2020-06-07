import pymongo
import pickle


s = {
'user28':['4'+str(i).rjust(4,'0') for i in [1,11,21,31,41,51,61,71,81,91] ],
'user29':['4'+str(i).rjust(4,'0') for i in [3,13,23,33,43,53,63,73,83,93] ],
'user30':['4'+str(i).rjust(4,'0') for i in [5,15,25,35,45,55,65,75,85,95] ],
'user31':['4'+str(i).rjust(4,'0') for i in [7,17,27,37,47,57,67,77,87,97] ],
'user32':['4'+str(i).rjust(4,'0') for i in [9,19,29,39,49,59,69,79,89,99] ],
}

con = pymongo.MongoClient("mongodb://localhost:27017/")
db = con.ntcir
usrlog = db.usrlog
dct = {}
for i in s.keys():
    temp = {}
    for j in s[i]:
        temp[j]=[item for item in usrlog.find({"usrid":i,"topicid":j }).sort([("docid",1),("_id",pymongo.ASCENDING)])]
    dct[i] = temp
pickle.dump(dct,open("history_5.pkl","wb"))