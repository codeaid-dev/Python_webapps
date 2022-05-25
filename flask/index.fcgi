#! /home/wwbwb/miniconda3/envs/py39/bin/python
from flup.server.fcgi import WSGIServer
from hello import app

if __name__ == '__main__':
    WSGIServer(app).run()