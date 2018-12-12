#!/bin/bash

cd;
cd Desktop/env;
source myenv/bin/activate;
cd;
cd Desktop/DRF-API-Model-Example-master/waitingblock;
python manage.py runserver;
gulp;
