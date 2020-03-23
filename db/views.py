from django.http import HttpResponse
from . import db
import json
import datetime
import requests


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.strftime("%d.%m.%Y")

def query_db(request):
    connection = db.Connection()
    my_query = connection.query_db("select ID, NAME, TXT, DT  from tst  where rownum <= :s", [3])
    json_output = json.dumps(my_query, default = myconverter)
    return HttpResponse(json_output)

def print_query(request):
    response = requests.get("http://127.0.0.1:8000/db_tst/get")
    rows = json.loads(response.text)
    return HttpResponse(rows[0]["NAME"] + rows[0]["DT"])

def upd(request):
    json_data = requests.get("http://127.0.0.1:8000/db_tst/get")
    print( json_data.text)
    connection = db.Connection()
    connection.merge_tbl("""
merge into tst t
using (select :ID id,
              :NAME name,
              :TXT txt,
              to_date(:DT, 'dd.mm.yyyy') dt
       from dual ) n
on (t.id = n.id+1)
when matched then
  update 
  set t.name = n.name,
      t.txt = n.txt,
      t.dt = n.dt
when not matched then 
  insert(id,name,txt, dt)       
  values(nvl(n.id+1, seq.nextval), n.name, n.txt, n.dt)    
    """, json_data.text)
    return HttpResponse('OK')