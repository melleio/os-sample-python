from flask import Flask
from time import sleep
import re
import requests
import csv, os, json
import html5lib
from lxml import html
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

def read_zipfile(path):
    with open(os.path.join(os.path.dirname(__file__),path)) as f:
        return BeautifulSoup(f.read(),  "html5lib")

def save_htmlfile(url, filename_):
    ''' USE this to get an html file saved to your disk
    you need to provide the link & what you would like to name yourfile
    '''
    #url = "https://angel.co/sahbayahia-yahoo-com"
    
    filename  = open(os.path.join(os.path.dirname(__file__),filename_), "w")
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    response = requests.get(url, headers=headers)
    formatted_response = response.content.replace('<!--', '').replace('-->', '')
    soup=BeautifulSoup(formatted_response).prettify().encode('utf-8').strip()#[18700:30500]
    filename.write(soup)
    filename.close()
    return soup

def get_title_info(soup):
    #print "PROFILE INTRO:"
    get_profile  = []
    get_profile_ = {}
    get_profile_["get_title"] = soup.title.getText().strip()
    #for i in range(len(soup.find_all("div", class_ = " dm77 fud43 _a _jm"))):
    get_profile_["profile_description"]=soup.find_all("div", class_ = " dm77 fud43 _a _jm")[0].getText().strip()
    #return get_title, get_profile
    return get_profile_

def get_profile(soup):
    get_profile_ = {}
    get_profile_["profile_pic_link"] = soup.find_all('div', { "class":"profile-picture"})[0].find('a').get('href')
    get_profile_["profile_title"] =  get_title_info(soup)
    return  soup.find_all('div', { "class":"profile-picture"})[0].find('a').get('href')


def experience(soup):
    ## EXPERIENCE
    #print "EXPERIENCE"
    current_position = soup.find_all("li",class_ = 'position')
    #print len(current_position)
    experiences = soup.find_all("ul", class_= 'positions')
    #print len(experiences)
    EXP_ =[]
    for index in range(len(current_position)):
        experience_ =  {}
        experience_["company_name"] = experiences[0].find_all("h5", class_="item-subtitle")[index].getText().strip()
        experience_["title_in_company"] = experiences[0].find_all("h4", class_="item-title")[index].getText().strip()
        experience_["from_till"] = experiences[0].find_all("span", class_="date-range")[index].getText().strip()
        EXP_.append(experience_)
    for index in range(len(experiences)):
        experience_ =  {}
        experience_["company_name"] = experiences[0].find_all("h5", class_="item-subtitle")[index].getText().strip()
        experience_["title_in_company"]  = experiences[0].find_all("h4", class_="item-title")[index].getText().strip()
        experience_["from_till"]= experiences[0].find_all("span", class_="date-range")[index].getText().strip()
        EXP_.append(experience_)

    return EXP_

def skills(soup):
    skills = soup.find_all('ul', class_='pills')
    skills_ = {}
    for index, skill in enumerate(skills):
        skills_["skills"] = [skl.getText().strip() for skl in skill.find_all('li', class_='skill')]
    return skills_
def education(soup):
    schools  =  soup.find_all('ul', class_ = 'schools')
    edu = schools[0].find_all('li', class_ = "school")

    education_ = []
    for index in range(len(edu)):
        edu_ = {}
        edu_['school_name'] = edu[index].find_all("h5", class_="item-subtitle")[0].getText().strip()
        edu_["school_title"] = edu[index].find_all("h4", class_="item-title")[0].getText().strip()
        edu_["from_till"] = edu[index].find_all("div", class_="meta")[0].getText().strip()

        education_.append(edu_)

    return  education_

application = Flask(__name__)
@application.route("/")
def start_linkedIN():
    u = request.args.get('url', '')
    filename = request.args.get('filename','')
    url = "https://www.linkedin.com/in/" + u
    return "Hello World!"

if __name__ == "__main__":
    application.run()
