
from minio import Minio
from minio.error import S3Error
from flask import Flask, render_template, request
from flask import redirect, url_for
import json
from flask_paginate import Pagination, get_page_parameter



app = Flask(__name__)

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
    try:
        data = minio_client.get_object(bucket_name, object_name)
        content = data.read().decode('utf-8')
        data = json.loads(content)
    except S3Error as e:
        print(e)
        content = ''
    return render_template('object_content.html', object_name=object_name, data=data)

@app.route('/verify/<string:id>', methods=['GET', 'POST'])
def verify(id):
    if request.method == 'POST':
        data = request.form['data']
        json_data = json.loads(data.replace("'", "\""))
        return " "
        #make_primary_blockchain_call(json_data)
    else:
        pass


if __name__ == '__main__':
    app.run()


