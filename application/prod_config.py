import os 
import boto3

basedir = os.path.abspath(os.path.dirname(__file__))

path = '/project-fault/prod/'

def get_parameter(client, parameter_name):
    return client.get_parameter(Name=f'{path}{parameter_name}', WithDecryption=False)['Parameter']['Value']

class Config:
    client = boto3.client('ssm', region_name='us-east-1')

    SECRET_KEY = get_parameter(client, 'SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = get_parameter(client, 'SQLALCHEMY_DATABASE_URI')

    UPLOAD_FOLDER = basedir + '/static/audio/audio-files'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav'}
