import pymongo

con = pymongo.MongoClient("mongodb://localhost:27017/")
db = con.ntcir
usr = db.usr
ntcir = db.ntcir
resDict = {}
res=["<topicID>,<docID>,<assessment1>,<assessment2>\n"]
labelDict = {"NONREL":"0","ERROR":"-1","REL":"1","H.REL":"2"}
userList =  ["user21","user22"]
for i in range(len(userList)):
    for item in usr.find({"usrid":userList[i]}):
        key = item["topicid"]+' '+item["docid"]
        if not resDict.__contains__(key):
            resDict[key] = [labelDict[item["val"]]]
        else:
            resDict.get(key).append(labelDict[item["val"]])
for k in resDict.keys():
    topicid=k.split(" ")[0]
    docid = k.split(" ")[1]
    lineList = resDict.get(k)

    lineList.insert(0,ntcir.find_one({"title_id":docid,"topic_id":topicid}).get("title"))
    lineList.insert(0, topicid[1:])
    if len(lineList)!=4:
        print(lineList)
    res.append(",".join(lineList)+"\n")
print(len(res)-1)
f=open("www1Add.txt","w",encoding="utf8")
f.writelines(res)
f.close()

