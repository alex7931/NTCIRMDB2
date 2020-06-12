# Assesment tool PLY for NTCIR WWW tasks

Developed by Yimeng Fan, Lingtao Li, Peng Xiao, maintained by Sijie Tao in RSL(Real Sakai Lab) of Waseda University.

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

### Obtain assessment progress report for each assessor

```
$ cd scripts
$ python3 exportProgress.py
```

### Obtain assessment results for each document

```
$ cd scripts
$ python3 exportWWW2.py
# or
$ python3 exportWWW1Addition.py
```

### Obain reports of assessor judgement bahavior

#### Get assessor history

```
$ cd scripts
$ python3 exportUserHistory.py
```

#### Obain a report from history file

```
$ cd scripts
$ python3 dataProcess.py
```
