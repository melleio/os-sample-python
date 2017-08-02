from flask import Flask
from time import sleep
import re
import requests
import csv, os, json
import html5lib
from lxml import html
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    application.run()
