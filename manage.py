# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 16:32:42 2021

@author: Rob
"""
from main import app, db, User, Post, Tag, migrate

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Post = Post, Tag = Tag, migrate=migrate)