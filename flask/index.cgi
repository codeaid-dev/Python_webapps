#! /home/wwbwb/miniconda3/envs/py39/bin/python
from wsgiref.handlers import CGIHandler
from hello import app

CGIHandler().run(app)