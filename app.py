from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os, boto3

access_key_id = os.environ['AWS_ACCESS_KEY_ID']
secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/s3')
def s3():
    s3 = boto3.client(
    's3',
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key)
    response = s3.list_buckets()
    bucket_names = [i['''Name'''] for i in response['Buckets']]
    bucket_regions = {name : s3.get_bucket_location(Bucket=name)['LocationConstraint'] for name in bucket_names}
    return render_template('s3.html', objs=bucket_regions)

@app.route("/complete/<string:bucket_name>")
def bucket_content(bucket_name):
    s3 = boto3.client(
    's3',
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key)
    bucket_cont = {}
    size = 0
    for obj in s3.list_objects_v2(Bucket=bucket_name)['Contents']:
        bucket_cont[obj['Key']] = obj['Size']
        size = size + obj['Size']
    rd = {}
    rd['name'] = bucket_name
    rd['bucket_cont'] = bucket_cont
    rd['bucket_size'] = (size / 1000000)
    return render_template('bucket_info.html', rd=rd)


if __name__ == '__main__':
    app.run(debug=True)