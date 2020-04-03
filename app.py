import os
import flask import Flask, render_template, redirect, request, url_for
from flask_pymong import PyMongo
from bson.objectid import objectId
if os.path.exists("env.py"):
    import env

