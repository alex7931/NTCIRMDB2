import pymongo

con = pymongo.MongoClient("mongodb://localhost:27017/")

db = con.ntcir
table = db.table
ntcir = db.ntcir
usrlist=db.usrlist
usr = db.usr
dc ={}
##step1 get total document number for each topic
# for www2 we have 80 topics
for i in range(1,81):
    qid = str(i).rjust(4,"0")
    dc[str(i)]=len([k for k in ntcir.find({"topic_id":str(i)})])
    dc["1"+qid]=len([k for k in ntcir.find({"topic_id":"1"+qid})])

# for www3 we have 80 topics
for i in range(101,181):
    qid = str(i).rjust(4,"0")
    dc[str(i)]=len([k for k in ntcir.find({"topic_id":str(i)})])
    dc["1"+qid]=len([k for k in ntcir.find({"topic_id":"1"+qid})])

# for www1 we have 100 topics
# for i in range(1,101):
    # if i!=14:
        # qid = "2"+str(i).rjust(4, "0")
        # dc[qid] = len([k for k in ntcir.find({"topic_id":qid})])

# we defined userid from user01,
for i in range(1,25):
    userid = "user" + str(i).rjust(2,"0")
    topicIds = str(usrlist.find_one({"usrid":userid})[u"usrl"]).split(",")
    totalNum=0
    for j in topicIds:
        totalNum+=dc[j]
    labelNum = len([k for k in usr.find({"usrid":userid})])
    print("userid:"+userid+" "+str(labelNum)+"/"+str(totalNum)+" "+str(labelNum*1.0/totalNum))
