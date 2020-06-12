# Assesment tool PLY for NTCIR WWW tasks 

Developed by Yimeng Fan, Lingtao Li, Peng Xiao, mentained by Sijie Tao in RSL(Real Sakai Lab) of Waseda University.

## Requirements

Python 2.7.10  
Django 1.8.16  
pymongo 2.8  

## Usage

### Preparation

Obtain pool files, assessors assignment files, topic files.

### Create database

```
$ cd data
$ python3 insertToDB.py
```

### Run

```
$ python2 manage.py runserver 0.0.0.0:8000
```

### Obtain assessment progress report

```
$ cd scripts
$ python3 exportProgress.py
```
