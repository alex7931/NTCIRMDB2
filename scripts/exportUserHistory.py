import pymongo
import pickle
from datetime import datetime
import pandas as pd

# create a dict, users = {userid: [topicid]}
users1 = pd.read_csv('../data/users1.csv')
users2 = pd.read_csv('../data/users2.csv')
users3 = pd.read_csv('../data/users3.csv')
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
                temp_topics[idx] = int('1' + topic_id[idx])
            else:
                temp_topics[idx] = int(topic_id[idx])
        users[user_id] = temp_topics

# connect to database
con = pymongo.MongoClient("mongodb://localhost:27017/")
db = con.ntcir
usrlog = db.usrlog

user_history = {}
for userid, topics in users.items():
    user_logs = {}
    for topicid in topics:
        user_logs[topicid]=[item for item in usrlog.find({"usrid": userid, "topicid": str(topicid)}).sort([("docid", 1),("_id" ,pymongo.ASCENDING)])]
    user_history[userid] = user_logs


#Time to judge the first document;
TJ1D_r = []
TJ1D_p = []
#Time to find the first Relevant or Highly relevant document;
TF1RH_r = []
TF1RH_p = []
#Time to find the first Highly relevant document;
TF1H_r = []
TF1H_p = []
#Average time between judging two documents;
ATBJ_r = []
ATBJ_p = []
# Number of times the label of a judged document is corrected to another label.
NREJ_r = []
NREJ_p = []
res=["topicid,userid,TJ1D,TF1RH,TF1H,ATBJ,NREJ\n"]
for userid in user_history.keys():
    temp = user_history[userid]
    for topicid in temp.keys():
        labeled_doc = set()
        history = temp[topicid]
        previousTime = None
        TJ1D = None
        TF1RH = None
        TF1H = None
        NREJ = 0
        time_list =[]
        post_pool={}
        for idx in range(len(history)):
            record = history[idx]
            if record["val"] == "post":
                post_pool[record["docid"]]= datetime.strptime(record["time"],"%Y-%m-%d %H:%M:%S")
            else:
                if record["docid"] not in labeled_doc:
                    labeled_doc.add(record["docid"])
                else:
                    NREJ += 1

                if post_pool.__contains__(record["docid"]):
                    judge_time=int((datetime.strptime(record["time"],"%Y-%m-%d %H:%M:%S")-post_pool[record["docid"]]).total_seconds())
                elif idx+1 < len(history) and history[idx+1]["docid"] == record["docid"]:
                    judge_time=int((datetime.strptime(history[idx+1]["time"],"%Y-%m-%d %H:%M:%S")-datetime.strptime(record["time"],"%Y-%m-%d %H:%M:%S")).total_seconds())
                else:
                    judge_time=0

                # if judge time is longer than 3 min (180s)
                # then the time is not included and set to "NA"
                threshold = 180
                if judge_time <= threshold:
                    time_list.append(judge_time)
                if not TJ1D:
                    if judge_time <= threshold:
                        TJ1D = judge_time
                    else:
                        TJ1D = "NA"
                if not TF1RH and (record["val"]=="REL" or record["val"]=="H.REL"):
                    if judge_time <= threshold:
                        TF1RH = judge_time
                    else:
                        TF1RH = "NA"
                if not TF1H and record["val"]=="H.REL":
                    if judge_time <= threshold:
                        TF1H = judge_time
                    else:
                        TF1H = "NA"
        ATBJ = sum(time_list)*1.0/len(time_list)
        if len(str(topicid))==5:
            poolType = "sort"
            tid=str(topicid)[1:]
            TJ1D_r.append(TJ1D)
            TF1RH_r.append(TF1RH)
            TF1H_r.append(TF1H)
            NREJ_r.append(NREJ)
            ATBJ_r.append(ATBJ)
        else:
            poolType = "rand"
            tid = str(topicid).rjust(4,"0")
            TJ1D_p.append(TJ1D)
            TF1RH_p.append(TF1RH)
            TF1H_p.append(TF1H)
            NREJ_p.append(NREJ)
            ATBJ_p.append(ATBJ)

        res.append(",".join([tid,userid,poolType,str(TJ1D),str(TF1RH),str(TF1H),"%.2f" %ATBJ,str(NREJ)])+"\n")
out=open("user_history_results.txt","w",encoding="utf8")
out.writelines(res)
out.close()
