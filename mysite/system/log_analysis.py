#coding:utf-8
import re
import os,sys,json
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR,])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from mysite import settings

access_log = os.path.join(settings.BASE_DIR,'logs/nginx/access.log')

def getVisits():

    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .*?("GET /(user)/(\d+)/.*?"|"GET /(blog)/\d{4}/\d{2}/\d{2}/.*?/(\d+)/.*?")')
    with open(access_log,'r') as aclog:
        s = aclog.read()
        visits = pattern.findall(s)
    blog_pages = [(i[0],i[4],i[5]) for i in visits if i[4]<>'']

    return blog_pages

if __name__ == '__main__':
    pass