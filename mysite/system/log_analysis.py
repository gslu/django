#coding:utf-8
import re
import os,sys,json
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR,])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from mysite import settings

access_log = os.path.join(settings.BASE_DIR,'logs/nginx/access.log')
uv_pv_path = os.path.join(settings.BASE_DIR,'logs/nginx/uv_pv.json')

def getUvPv():
    uv = 0
    pv = 0
    uv_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} ')
    pv_pattern = re.compile(r'("GET /user/.*?"|"POST /user/.*?"|"POST /blog/.*?"|"POST /user/.*?")')

    with open(access_log,'r') as aclog:
        s = aclog.read()
        ips = uv_pattern.findall(s)
        views = pv_pattern.findall(s)
        ips = set(ips)
        uv = len(ips)
        pv = len(views)
    return uv,pv

if __name__ == '__main__':
    while(True):
        uv,pv = getUvPv()
        s={"uv":uv,"pv":pv}
        with open(uv_pv_path,'w') as f:
            json.dump(s,f)
        time.sleep(600)