#!/bin/bash
set -eu

# start PLY 
screen python2 manage.py runserver 0.0.0.0:8000
