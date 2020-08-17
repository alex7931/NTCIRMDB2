import pandas as pd
import pymongo

con = pymongo.MongoClient("mongodb://localhost:27017/")
db = con.ntcir
usr = db.usr
ntcir = db.ntcir
resDict = {}
res=["<topicID>,<docID>"]
labelDict = {"NONREL":"0","ERROR":"-1","REL":"1","H.REL":"2","NOT ASSIGNED":"NA"}

for i in range(1, 25):
    label = "<Label_" + str(i) + ">"
    res[0] += label
res[0] += "\n"
print("header:", res[0])

# from user01~user24
for i in range(1,25):
    # 1 -> "user01"
    userid = "user"+str(i).rjust(2,"0")
    print(userid)
    for item in usr.find({"usrid":userid}):
        if len(item["topicid"])!=5:
            key = item["topicid"].rjust(4,"0")+' '+item["docid"]
        else:
            key = item["topicid"][1:] + ' ' + item["docid"]
        if not resDict.__contains__(key):
            resDict[key] = ["NA"] * 24
            resDict.get(key)[i-1] = labelDict[item["val"]]
        else:
            resDict.get(key)[i-1] = labelDict[item["val"]]
for k in resDict.keys():
    topicid=k.split(" ")[0]
    docid = k.split(" ")[1]
    lineList = resDict.get(k)
    # get document title
    lineList.insert(0,ntcir.find_one({"title_id":docid,"topic_id":"1"+topicid}).get("title"))
    lineList.insert(0, topicid)
    # lineList = ['0110', 'clueweb12-1209wb-18-02193', '1', '0', '0', ...]
    if len(lineList) != 26:
        print(lineList)
    res.append(",".join(lineList)+"\n")
print(len(res)-1)

with open("ntcir-15-www3.txt","w",encoding="utf8") as f:
    f.writelines(res)
