#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse,render_to_response
from user_system.utils import *
from assessment.models import *
import numpy as np
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
import os
import json
import time



@require_login
def assessment(user,request):
    if user.username== 'administrator':
        user_name=list(usrlist.objects.values_list('usrid'))
        # user_name.remove('test01')
        all_multilist=[]
        for i in user_name:
            user_multilist = []
            user_multilist.append(i)
            user_complete_num=len(usr.objects.filter(usrid=str(i)))
            user_topic_list = usrlist.objects.get(usrid=str(i)).usrl
            l = []
            for g in user_topic_list.split(','):
                l.append(int(g))
            user_total_num = 0
            all_topic_num=[]
            for j in l:
                user_total_num += len(ntcir.objects.filter(topic_id=str(j)))
                topic_num = []
                topic_num.append(j)
                topic_num.append(len(usr.objects.filter(topicid=str(j)).filter(usrid=str(i))))
                topic_num.append(len(ntcir.objects.filter(topic_id=str(j))))
                all_topic_num.append(topic_num)
            user_multilist.append([user_complete_num,user_total_num])
            user_multilist.append(all_topic_num)
            all_multilist.append(user_multilist)

        return render(request, 'administrator.html', locals())
    else:
        top = table.objects.all()
        user_topic_list=usrlist.objects.get(usrid=str(user.username)).usrl
        l=[]
        for i in user_topic_list.split(','):
            l.append(int(i))

        mark = []
        cc = 1
        for a in l:
            count = len(usr.objects.filter(topicid=str(a)).filter(usrid=str(user.username)))
            total = len(ntcir.objects.filter(topic_id=str(a)))
            tablename=table.objects.get(table_id=str(a)).table
            mark.append([str(a),tablename,count,total,str(cc)])
            cc+=1

        return render(request, 'topic.html',locals())


@require_login
def jump(user,request,listnum):
    user_topic_list = usrlist.objects.get(usrid=str(user.username)).usrl
    l = []
    for i in user_topic_list.split(','):
        l.append(int(i))
    mark = []
    cc = 1
    for a in l:
        tablename=table.objects.get(table_id=str(a)).table
        mark.append([str(a),tablename,str(cc)])
        cc+=1
    fnum=1
    lnum=len(l)
    listnum=int(listnum)
    topic_id = l[listnum - 1]
    topic = table.objects.get(table_id=str(topic_id)).table
    topicid=int(topic_id)
    doc = ntcir.objects.filter(topic=str(topic))
    userdata = usr.objects.filter(topicid=str(topic_id)).filter(usrid=str(user.username))
    top = table.objects.all()


    completed = len(usr.objects.filter(topicid=str(topic_id)).filter(usrid=str(user.username)))
    totalnum = len(ntcir.objects.filter(topic_id=str(topic_id)))
    nonrelnum = len(usr.objects.filter(topicid=str(topic_id)).filter(usrid=str(user.username)).filter(val="NONREL"))
    relnum = len(usr.objects.filter(topicid=str(topic_id)).filter(usrid=str(user.username)).filter(val="REL"))
    hrelnum = len(usr.objects.filter(topicid=str(topic_id)).filter(usrid=str(user.username)).filter(val="H.REL"))
    errornum = len(usr.objects.filter(topicid=str(topic_id)).filter(usrid=str(user.username)).filter(val="ERROR"))

    doclist= []
    cou=[None]*totalnum
    for d in doc:
        doclist.append([int(d.title_id),d.title])
        doclist.sort()
    for u in userdata:
        doclist[int(u.docid)-1].extend([u.val,u.color])
        cou[int(u.docid)-1]=u.val

    count=0
    for c in cou:
        count+=1
        if c == None:
            break



    return render(request, 'assessment.html',locals())


@require_login
def id_con(user,request):
    user_topic_list = usrlist.objects.get(usrid=str(user.username)).usrl
    l = []
    for i in user_topic_list.split(','):
        l.append(int(i))

    doc_id = request.GET.get("docid",None)
    listnum = request.GET.get("topicid",None)
    topic_id = str(l[int(listnum) - 1])
    topic = table.objects.get(table_id=str(topic_id)).table
    a = ntcir.objects.get(topic=str(topic),title_id=str(doc_id)).url
    log = usrlog(
        time=str(time.strftime("%Y-%m-%d %H:%M:%S")),
        topicid=topic_id,
        docid=doc_id,
        usrid=user.username,
        val="post"
    )
    log.save()
    return HttpResponse(json.dumps({"asd":a}))

@require_login
def sv(user,request):
    user_topic_list = usrlist.objects.get(usrid=str(user.username)).usrl
    l = []
    for i in user_topic_list.split(','):
        l.append(int(i))
   # print(user.username)
    docid = request.GET.get("docid", None)
    listnum = request.GET.get("topicid", None)
    topicid = str(l[int(listnum) - 1])
   # topic = table.objects.get(table_id=str(topicid)).table
   # doc = ntcir.objects.get(topic=str(topic),title_id=str(docid)).title
   # usrid = request.GET.get("usrid", None)
   # usrid = user
    val = request.GET.get("val", None)
    color = request.GET.get("color", None)
    u = usr.objects.filter(topicid=str(topicid)).filter(docid=str(docid)).filter(usrid=str(user.username))
    u.delete()
    userdata = usr(
          topicid = topicid,
          docid = docid,
          usrid = user.username,
          val = val,
          color = color
    )
    userdata.save()
    completed = len(usr.objects.filter(topicid=str(topicid)).filter(usrid=str(user.username)))
    totalnum = len(ntcir.objects.filter(topic_id=str(topicid)))
    nonrelnum = len(usr.objects.filter(topicid=str(topicid)).filter(usrid=str(user.username)).filter(val="NONREL"))
    relnum = len(usr.objects.filter(topicid=str(topicid)).filter(usrid=str(user.username)).filter(val="REL"))
    hrelnum = len(usr.objects.filter(topicid=str(topicid)).filter(usrid=str(user.username)).filter(val="H.REL"))
    errornum = len(usr.objects.filter(topicid=str(topicid)).filter(usrid=str(user.username)).filter(val="ERROR"))
    log = usrlog(
        time=str(time.strftime("%Y-%m-%d %H:%M:%S")),
        topicid=topicid,
        docid=docid,
        usrid=user.username,
        val=val
    )
    log.save()

    # user_complete_num = len(usr.objects.filter(usrid=str(user.username)))
    # user_total_num = 0
    # for j in l:
    #     user_total_num += len(ntcir.objects.filter(topic_id=str(j)))
    # all_topic_num=usrprocess(
    #     usrid=str(user.username),
    #     alltopicnum='all'+' '+'topics:'+' '+str(user_complete_num)+'/'+str(user_total_num),
    #     topicnum=
    # )
    # all_topic_num.save()
    return HttpResponse(json.dumps({"completed":completed, "totalnum":totalnum,"nonrelnum":nonrelnum,"relnum":relnum,"hrelnum":hrelnum,"errornum":errornum}))

def show(request,url):
    a=url[10:12]
    return render(request, a+"/"+url)


def st(request):
    uname=request.GET.get('uname',None)
    ulist=request.GET.get('ulist',None)
    u=usrlist.objects.filter(usrid=uname)
    u.delete()
    userlistdata=usrlist(
        usrid=uname,
        usrl=ulist
    )
    userlistdata.save()
    return HttpResponse()

def download_data(request):
    import pymongo

    con = pymongo.Connection('localhost', 27017)

    ntcir = con.ntcir
    topic = ntcir.ntcir
    topiclist = ntcir.table
    usr = ntcir.usr

    matrix = [[0 for i in range(201)] for i in range(400)]
    d1 = open('/home/fanyimeng/exdocument.txt')
    for line in d1:
        a = line.strip('\n').split(' ')
        matrix[int(a[2])][int(a[0])] = a[1]
    d1.close()

    f = open('/home/fanyimeng/assessment_result.csv', 'w')
    for line in usr.find():
        if line['usrid']!='test01':
            usrid = line['usrid']
            docid = line['docid']
            topicid = line['topicid']
            val = line['val']
            docname = matrix[int(docid)][int(topicid)]
            s = usrid + ',' + topicid + ',' + docname + ',' + val + '\n'
            f.write(s)

    f.close()

    def readfile(fn,buf_size=262144):
        f=open(fn,'rb')
        while True:
            c=f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    the_file_name='assessment_result.csv'
    response=HttpResponse(readfile('/home/fanyimeng/assessment_result.csv'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

    return response











