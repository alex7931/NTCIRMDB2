import pickle
from datetime import datetime

data = pickle.load(open("history_5.pkl","rb"))
print(data)
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
res=["userid,topic,pooltype,TJ1D,TF1RH,TF1H,ATBJ,NREJ\n"]
for userid in data.keys():
    temp = data[userid]
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
                if judge_time<=60*3:
                    time_list.append(judge_time)
                if not TJ1D:
                    TJ1D = judge_time
                if not TF1RH and (record["val"]=="REL" or record["val"]=="H.REL"):
                    TF1RH = judge_time
                if not TF1H and record["val"]=="H.REL":
                    TF1H = judge_time
        ATBJ = sum(time_list)*1.0/len(time_list)
        if len(topicid)==5:
            poolType = "rand"
            tid=topicid[1:]
            TJ1D_r.append(TJ1D)
            TF1RH_r.append(TF1RH)
            TF1H_r.append(TF1H)
            NREJ_r.append(NREJ)
            ATBJ_r.append(ATBJ)
        else:
            poolType = "sort"
            tid = topicid.rjust(4,"0")
            TJ1D_p.append(TJ1D)
            TF1RH_p.append(TF1RH)
            TF1H_p.append(TF1H)
            NREJ_p.append(NREJ)
            ATBJ_p.append(ATBJ)

        res.append(",".join([userid,tid,poolType,str(TJ1D),str(TF1RH),str(TF1H),"%.2f" %ATBJ,str(NREJ)])+"\n")
out=open("res3.txt","w",encoding="utf8")
out.writelines(res)
out.close()










