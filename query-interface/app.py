
from minio import Minio
from minio.error import S3Error
from flask import Flask, render_template, request,session
from flask import redirect, url_for
import json
import secrets
from flask_paginate import Pagination, get_page_parameter
import requests



app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


minio_client = Minio(
    "172.17.89.13:9000",  
    #access_key="33Tl7GDiUF6VBqIS",  
    access_key="uFikcvPEGXGyM8MS",  
    #secret_key="AaQ8neXo3WOto6DMX3yIsymFaiOExlRG",  
    secret_key="eKrpM0UAWvL9HbC36I4MgPOfpEiCGtPn",  
    secure=False
)

@app.route('/')
def buckets():
    buckets = minio_client.list_buckets()
    return render_template('buckets.html', buckets=buckets)

@app.route('/objects/<bucket_name>')
def objects(bucket_name):
    print("objects called")
    objects = minio_client.list_objects(bucket_name, recursive=True)
    return render_template('objects.html', objects=objects, bucket_name=bucket_name)

@app.route('/objects/<bucket_name>/<path:object_name>', endpoint='object_content')
def object_content(bucket_name, object_name):
    new_info = session.pop('new_info', None)
    #if new_info is not None:
    try:
        data = minio_client.get_object(bucket_name, object_name)
        content = data.read().decode('utf-8')
        data = json.loads(content)
    except S3Error as e:
        print(e)
        content = ''
    return render_template('object_content.html', object_name=object_name, data=data, new_info=new_info)

@app.route('/verify/<string:id>', methods=['GET', 'POST'])
def verify(id):
    if request.method == 'POST':
        data = request.form['data']
        #print("BEOFRE CONVERSION",data)
        #data_str = json.dumps(data)
        new_string = data.replace("'", "\"")
        new_string = new_string.replace(' ', '').replace('\t', '').replace('\n', '')
       # print("JSON AFTER CONVERSION",new_string)
        result = query_contract('tartucitycouncilchannel', 'tartucitycouncil', [new_string, id])
        print("ID", id)
        print("New String", new_string)
        print("Returned Result:::", result)
        previous_path = request.referrer
        session['new_info'] = 'some_value'
        print(previous_path)
        return redirect(previous_path)
        #make_primary_blockchain_call(json_data)
    else:
        return redirect(request.url)


def get_token():
  #TOKEN_ENDPOINT = config.TOKEN_ENDPOINT
  TOKEN_ENDPOINT = "http://172.17.91.150:8801/user/enroll"
  headers = {
    "Authorization": "Bearer ",
    "Content-Type": "application/json",
  }
  response = requests.post(TOKEN_ENDPOINT, headers=headers, json={"id": "admin", "secret": "adminpw"})
  data = response.json()
  return data["token"]



def query_contract(contract_name, contract_method, args):
    url = 'http://172.17.91.150:8801/query/{0}/{1}'.format(contract_name, contract_method)
    headers = {
        'Authorization': 'Bearer {0}'.format(get_token()),
        'Content-Type': 'application/json'
    }
    data = {
        'method': 'KVContract:getAndCompareHash',
        'args': args
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

contract_name = 'tartucitycouncilchannel'
contract_method = 'tartucitycouncil'
data = data = '{"temperature":12.542256603183866,"timestamp":"2023-05-08T11:28:01Z","org":"TartuCityCouncil","device":"sensorOne","id":"65c8ce38-5466-4de7-ac08-a663cc26b644","arrivalTime":"2023-05-08T11:28:02.537+03:00","departTimeFromFogNode":"2023-05-08T11:28:02.539+03:00"}'
args = [data, '65c8ce38-5466-4de7-ac08-a663cc26b644']

if __name__ == '__main__':
    app.run()


