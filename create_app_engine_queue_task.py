
from __future__ import print_function
#import datetime
import logging
import os
from flask import Flask, render_template, request, Response
import sqlalchemy
from sqlalchemy import text
from flask import Flask
from sqlalchemy import create_engine
import requests
import os  
import time
import requests
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import json
from io import BytesIO
import io    
import base64
from pandas.io.json import json_normalize
import datetime
from datetime import datetime, timedelta
#import datetime
import argparse
import os



#and the access its now method simpler
d1 = datetime.now()

#
#from datetime import datetime, timedelta
#futuredate = datetime.now() + timedelta(days=10)
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"F:\\My_Data_personal\\new_secpod_api\\tasks\\GOOGLE_APPLICATION_CREDENTIALS.json"

# Remember - storing secrets in plaintext is potentially unsafe. Consider using
# something like https://cloud.google.com/kms/ to help keep secrets secret.
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

app = Flask(__name__)

logger = logging.getLogger()

# [START cloud_sql_mysql_sqlalchemy_create]
# The SQLAlchemy engine will help manage interactions, including automatically
# managing a pool of connections to your database
db = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_pass,
        database=db_name,
        query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)},
    ),
    # ... Specify additional properties here.
    # [START_EXCLUDE]
    # [START cloud_sql_mysql_sqlalchemy_limit]
    # Pool size is the maximum number of permanent connections to keep.
 # Pool size is the maximum number of permanent connections to keep.
    pool_size=10,
    # Temporarily exceeds the set pool_size if no connections are available.
    max_overflow=5,

    pool_timeout=30000,  # 30 seconds
    # [END cloud_sql_mysql_sqlalchemy_timeout]
    # [START cloud_sql_mysql_sqlalchemy_lifetime]
 
    pool_recycle=1000000,  # 30 minutes
    # [END cloud_sql_mysql_sqlalchemy_lifetime]
    # [END_EXCLUDE]
)
    
url = "https://saner.secpod.com/AncorWebSer223vice/perform213"
#admin_key ="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"
headers_req = {
   'Content-Type': "application/x-www-form-urlencoded",
 
    'Authorization': "",
    'Host': "",
    'User-Agent': "",
    'Connection': "",
}


t = text("SELECT * FROM account_id")

with db.connect() as conn:
        data=conn.execute(t).fetchall()



row_acc=[]
for i,row in enumerate(data):
        row_acc.append(row[0])
        print(row[0])


@app.route('/create_task_vul_host', methods=['POST'])
def create_task():
    # [START cloud_tasks_appengine_create_task]
    """Create a task for a given queue with an arbitrary payload."""

    from google.cloud import tasks_v2
    from google.protobuf import timestamp_pb2

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    project = ''
    queue = 'my-appengine-queue'
    location = 'us-central1'
#    payload = 'ankita'
    in_seconds= 300
	
    
    

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)
    
    for acc in row_acc:
        payload = str(acc)

        # Construct the request body.
        task = {
                'app_engine_http_request': {  # Specify the type of request.
                    'http_method': 'POST',
                    'relative_uri': '/secpod_vul_hosts'
                }
        }
        if payload is not None:
            # The API expects a payload of type bytes.
            converted_payload = payload.encode()
    
            # Add the payload to the request.
            task['app_engine_http_request']['body'] = converted_payload
    
        if in_seconds is not None:
            # Convert "seconds from now" into an rfc3339 datetime string.
            d = datetime.utcnow() + timedelta(seconds=in_seconds)
    
            # Create Timestamp protobuf.
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(d)
    
            # Add the timestamp to the tasks.
            task['schedule_time'] = timestamp
    
        # Use the client to build and send the task.
        response = client.create_task(parent, task)
    
        print('Created task {}'.format(response.name))
    return response
    # [END cloud_tasks_appengine_create_task]
    
row_vul_host=[]
@app.route('/secpod_vul_hosts', methods=['POST','GET'])
def example_task_handler():
    """Log the request payload."""
    payload = request.get_data(as_text=True) or '(empty payload)'
    print('Received task with payload: {}'.format(payload))
#    return 'Printed task payload: {}'.format(payload)

    data = """data={"request": {"method": "getreportapidata","parameters": {"parameterset": [{"parameter": [{"key": "accountid","value": """+'"'+str(payload)+'"'+"""},{"key": "reportapi","value": "Vulnerable Hosts"}]}]}}}"""   # here they're returning a 404
    r = requests.post(url,data=data,headers=headers_req)
    
#        time.sleep(5)
#    return str(r.status_code)
#    print('getvulnerablehost:', r.status_code)
    encoded_string = base64.b64encode(r.content)
    encoded_string=str(encoded_string)
    
    
    encoded_string=encoded_string.strip("b")
    encoded_string=encoded_string.strip("'")
    
    
    #print(encoded_string)
    url_send = "https://26-01-dot-omnistruct-web-app.appspot.com/saveSecpodReport"
    
    payload_send = """{"filecontent":"""+'"'+str(encoded_string)+'"'+""","apiname":"vulnerabilityedits","accountid":"sp15r0d3rxpzzba","mimetype":"application/zip,multipart/x-zip","filename":"responsevulhosts.zip"}"""
    headers_send = {
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url_send, headers=headers_send, data = payload_send)
#        time.sleep(5)
    print(response.text.encode('utf8'))
    
    
    u12="https://compliance.omnistruct.com/getartifactfile?fileurl=responsevulhosts.zip&mimetype=application/zip,multipart/x-zip1"
    resp = urlopen(u12)
    zipfile = ZipFile(BytesIO(resp.read()))
    zipfile.namelist()
#        time.sleep(5)
    data_output = zipfile.read('response.json')
    #print(data_output)
    
        
    bytes_io = io.BytesIO(data_output)
    
    dict_train = json.load(bytes_io)
    
    
#        vul_stat_df=json_normalize(dict_train['severity'])
    
    get_all_data=[]
    
    for i in dict_train['device']:
             get_all_data.append(i.copy())
             
             
     
    final_d=[]
 
    for dicts in get_all_data: 
        for keys in dicts: 
            dicts[keys] = str(dicts[keys]) 
        final_d.append(dicts)
            
        date = str(datetime.now()).split()[0]  #date in yyyy-02-12
    
        # Adding a new key value pair
        for id1 in final_d:
            id1.update( {'Date' : date} )
            id1.update({'account_id' : payload})
            
        for id2 in final_d:
            if 'profileId' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'profileId' : ''} )
            
        for id2 in final_d:
            if 'IPAddress' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'IPAddress' : ''} )
                
        for id2 in final_d:
            if 'critical' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'critical' : ''} )
                
        for id2 in final_d:
            if 'family' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'family' : ''} )
                
        for id2 in final_d:
            if 'groupId' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'groupId' : ''} )
                
        for id2 in final_d:
            if 'high' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'high' : ''} )
                
        for id2 in final_d:
            if 'low' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'low' : ''} )
                
        for id2 in final_d:
            if 'medium' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'medium' : ''} )
                
        for id2 in final_d:
            if 'name' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'name' : ''} )
                
        for id2 in final_d:
            if 'totalThreatIndicators' in id2:
#                value=id2['profileId']
                print("yes")
            else:
#                print("nooooo")
                id2.update( {'totalThreatIndicators' : ''} )
                
        for id2 in final_d:
            if 'totalVulnerabilities' in id2:
#                value=id2['profileId']
                print("yes")
                
            else:
#                print("nooooo")
                id2.update( {'totalVulnerabilities' : ''} )
            
         

        
        sql = """INSERT INTO vulnerable_hosts (account_id,date,ipaddress,critical,family,groupId,high,low,medium,name,profileId,
    totalThreatIndicators,totalVulnerabilities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
   
              
        for id1 in final_d:   

            values = (id1['account_id'],id1['Date'],id1['IPAddress'],id1['medium'],id1['low'],id1['high'],id1['critical'],id1['family'],id1['groupId'],id1['name'],id1['profileId'],id1['totalThreatIndicators'],id1['totalVulnerabilities'])
    
            with db.connect() as conn:
                conn.execute(sql, values)
            

   
        
        
        
    row_vul_host.append(final_d)

    print(final_d)


    return str(row_vul_host)	





@app.route('/create_task_high_fidelity_attack', methods=['POST'])
def create_task_high_fidelity_attack():
    # [START cloud_tasks_appengine_create_task]
    """Create a task for a given queue with an arbitrary payload."""

    from google.cloud import tasks_v2
    from google.protobuf import timestamp_pb2

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    project = ''
    queue = 'my-appengine-queue'
    location = 'us-central1'
#    payload = 'ankita'
    in_seconds= 300
	
    
    

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)
    
    for acc in row_acc:
        payload = str(acc)

        # Construct the request body.
        task = {
                'app_engine_http_request': {  # Specify the type of request.
                    'http_method': 'POST',
                    'relative_uri': '/secpod_high_fidelity_attacks'
                }
        }
        if payload is not None:
            # The API expects a payload of type bytes.
            converted_payload = payload.encode()
    
            # Add the payload to the request.
            task['app_engine_http_request']['body'] = converted_payload
    
        if in_seconds is not None:
            # Convert "seconds from now" into an rfc3339 datetime string.
            d = datetime.utcnow() + timedelta(seconds=in_seconds)
    
            # Create Timestamp protobuf.
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(d)
    
            # Add the timestamp to the tasks.
            task['schedule_time'] = timestamp
    
        # Use the client to build and send the task.
        response = client.create_task(parent, task)
    
        print('Created task {}'.format(response.name))
    return response
    # [END cloud_tasks_appengine_create_task]


row_high_fidelity_attacks=[]
@app.route('/secpod_high_fidelity_attacks', methods=['POST','GET'])
def home_high_fidelity_attacks():
    """Log the request payload."""
    payload = request.get_data(as_text=True) or '(empty payload)'
    print('Received task with payload: {}'.format(payload))
#    return 'Printed task payload: {}'.format(payload)
    data = """data={"request": {"method": "getreportapidata","parameters": {"parameterset": [{"parameter": [{"key": "accountid","value": """+'"'+str(payload)+'"'+"""},{"key": "reportapi","value": "High Fidelity Attacks"}]}]}}}"""   # here they're returning a 404
    r = requests.post(url,data=data,headers=headers_req)
    
#        time.sleep(5)
#    return str(r.status_code)
#    print('getvulnerablehost:', r.status_code)
    encoded_string = base64.b64encode(r.content)
    encoded_string=str(encoded_string)
    
    
    encoded_string=encoded_string.strip("b")
    encoded_string=encoded_string.strip("'")
    
    
    #print(encoded_string)
    url_send = "https://26-01-dot-omnistruct-web-app.appspot.com/saveSecpodReport"
    
    payload_send = """{"filecontent":"""+'"'+str(encoded_string)+'"'+""","apiname":"vulnerabilityedits","accountid":"sp15r0d3rxpzzba","mimetype":"application/zip,multipart/x-zip","filename":"responsehighfidelity.zip"}"""
    headers_send = {
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url_send, headers=headers_send, data = payload_send)
#        time.sleep(5)
    print(response.text.encode('utf8'))
    
    
    u12="https://compliance.omnistruct.com/getartifactfile?fileurl=responsehighfidelity.zip&mimetype=application/zip,multipart/x-zip"
    resp = urlopen(u12)
    zipfile = ZipFile(BytesIO(resp.read()))
    zipfile.namelist()
#        time.sleep(5)
    data_output = zipfile.read('response.json')
    #print(data_output)
    
        
    bytes_io = io.BytesIO(data_output)
    
    dict_train = json.load(bytes_io)
    
    
#        vul_stat_df=json_normalize(dict_train['severity'])
    
    get_all_data=[]
    
    for i in dict_train['attacks']:
             get_all_data.append(i.copy())
             
             
     
    final_d=[]
#    for get_one_dict in get_all_data:
    for dicts in get_all_data: 
        for keys in dicts: 
            dicts[keys] = str(dicts[keys]) 
        final_d.append(dicts)
            
        date = str(datetime.now()).split()[0]  #date in yyyy-02-12
    
        # Adding a new key value pair
        for id1 in final_d:
            id1.update( {'Date' : date} )
            id1.update({'account_id' : payload})
            
        for id2 in final_d:
            if 'hostnames' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'hostnames' : ''} )
        
        for id2 in final_d:
            if 'reference' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'reference' : ''} )
                
        for id2 in final_d:
            if 'tags' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'tags' : ''} )
                    
         

        
        sql = """INSERT INTO high_fidelity_attacks (account_id,date,hostnames,reference,tags) VALUES (%s,%s,%s,%s,%s)"""
              
        for id1 in final_d:   

            values = (id1['account_id'],id1['Date'],id1['hostnames'],id1['reference'],id1['tags'])
    
            with db.connect() as conn:
                conn.execute(sql, values)

   
        
        
        
    row_high_fidelity_attacks.append(final_d)

    print(final_d)


    return str(row_high_fidelity_attacks)





@app.route('/create_patch_statistics', methods=['POST'])
def create_task_patch_statistics():
    # [START cloud_tasks_appengine_create_task]
    """Create a task for a given queue with an arbitrary payload."""

    from google.cloud import tasks_v2
    from google.protobuf import timestamp_pb2

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    project = 'omnistruct-secpod-api'
    queue = 'my-appengine-queue'
    location = 'us-central1'
#    payload = 'ankita'
    in_seconds= 300
	
    
    

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)
    
    for acc in row_acc:
        payload = str(acc)

        # Construct the request body.
        task = {
                'app_engine_http_request': {  # Specify the type of request.
                    'http_method': 'POST',
                    'relative_uri': '/secpod_patch_statistics'
                }
        }
        if payload is not None:
            # The API expects a payload of type bytes.
            converted_payload = payload.encode()
    
            # Add the payload to the request.
            task['app_engine_http_request']['body'] = converted_payload
    
        if in_seconds is not None:
            # Convert "seconds from now" into an rfc3339 datetime string.
            d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)
    
            # Create Timestamp protobuf.
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(d)
    
            # Add the timestamp to the tasks.
            task['schedule_time'] = timestamp
    
        # Use the client to build and send the task.
        response = client.create_task(parent, task)
    
        print('Created task {}'.format(response.name))
    return response
    # [END cloud_tasks_appengine_create_task]

    


row_patchstatistics=[] 
@app.route('/secpod_patch_statistics', methods=['POST','GET'])
def home_patch_statistics():
    """Log the request payload."""
    payload = request.get_data(as_text=True) or '(empty payload)'
    print('Received task with payload: {}'.format(payload))
    
    data = """data={"request": {"method": "getreportapidata","parameters": {"parameterset": [{"parameter": [{"key": "accountid","value": """+'"'+str(payload)+'"'+"""},{"key": "reportapi","value": "Patch Statistics"}]}]}}}"""   # here they're returning a 404
    r = requests.post(url,data=data,headers=headers_req)
    

    encoded_string = base64.b64encode(r.content)
    encoded_string=str(encoded_string)
    
    
    encoded_string=encoded_string.strip("b")
    encoded_string=encoded_string.strip("'")
    
    
    #print(encoded_string)
    url_send = "https://26-01-dot-omnistruct-web-app.appspot.com/saveSecpodReport"
    
    payload_send = """{"filecontent":"""+'"'+str(encoded_string)+'"'+""","apiname":"vulnerabilityedits","accountid":"sp15r0d3rxpzzba","mimetype":"application/zip,multipart/x-zip","filename":"responsepatchstatistics.zip"}"""
    headers_send = {
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url_send, headers=headers_send, data = payload_send)
#        time.sleep(5)
    print(response.text.encode('utf8'))
    
    
    u12="https://compliance.omnistruct.com/getartifactfile?fileurl=responsepatchstatistics.zip&mimetype=application/zip,multipart/x-zip"
    resp = urlopen(u12)
    zipfile = ZipFile(BytesIO(resp.read()))
    zipfile.namelist()
#        time.sleep(5)
    data_output = zipfile.read('response.json')
    #print(data_output)
    
        
    bytes_io = io.BytesIO(data_output)
    
    dict_train = json.load(bytes_io)
    
    
#        vul_stat_df=json_normalize(dict_train['severity'])
    
    get_all_data=[]
    
    for i in dict_train[' patches ']:
             get_all_data.append(i.copy())
             
             
     
    final_d=[]
#    for get_one_dict in get_all_data:
    for dicts in get_all_data: 
        for keys in dicts: 
            dicts[keys] = str(dicts[keys]) 
        final_d.append(dicts)
            
        date = str(datetime.now()).split()[0]  #date in yyyy-02-12
    
        # Adding a new key value pair
        for id1 in final_d:
            id1.update( {'Date' : date} )
            id1.update({'account_id' : payload})
            
        for id2 in final_d:
            if 'asset' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'asset' : ''} )
            
        for id2 in final_d:
            if 'date' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'date' : ''} )
                
        for id2 in final_d:
            if 'families' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'families' : ''} )

        for id2 in final_d:
            if 'familycount' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'familycount' : ''} )
            
        for id2 in final_d:
            if 'hosts' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'hosts' : ''} )
            
        for id2 in final_d:
            if 'patch' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'patch' : ''} )
                
        for id2 in final_d:
            if 'reboot' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'reboot' : ''} )
            
        for id2 in final_d:
            if 'severity' in id2:
#                value=id2['profileId']
                print("yes")
            else:
                print("nooooo")
                id2.update( {'severity' : ''} )
             

        
        sql = """INSERT INTO patch_statistics (account_id,date,asset,hostcount,hosts,patch,severity) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
      
        for id1 in final_d:   

            values = (id1['account_id'],id1['Date'],id1['asset'],id1['hostcount'],id1['hosts'],id1['patch'],id1['severity'])

            with db.connect() as conn:
                conn.execute(sql, values)
            

        
        
        
    row_patchstatistics.append(final_d)

    print(final_d)


    return str(row_patchstatistics)


@app.route('/pre_create_task_vul_host', methods=['GET'])
def pre_create_task():
    url_create = "https://omnistruct-secpod-api.appspot.com/create_task_vul_host"
    response = requests.request("POST", url_create)
    print(response.text.encode('utf8'))
    return "Created Vulnerable host Task Created."

   
    
@app.route('/pre_create_task_high_fidelity_attacks', methods=['GET'])
def pre_create_task_high_fidelity_attacks():
    url_create = "https://omnistruct-secpod-api.appspot.com/create_task_high_fidelity_attack"
    response = requests.request("POST", url_create)
    print(response.text.encode('utf8'))
    return "Create high fedility Task Created."



@app.route('/pre_create_patch_statistics', methods=['GET'])
def pre_create_task_patch_statistics():
    url_create = "https://omnistruct-secpod-api.appspot.com/create_patch_statistics"
    response = requests.request("POST", url_create)
    print(response.text.encode('utf8'))
    return "Create patch statistics Task Created."



    

if __name__ == '__main__':
   
    app.run(host='127.0.0.1', port=8080, debug=True)
#    create_task()
