import os 
import boto3

basedir = os.path.abspath(os.path.dirname(__file__))

path = '/project-fault/prod/'

def get_parameter(client, parameter_name, use_decryption):
    return client.get_parameter(Name=f'{path}{parameter_name}', WithDecryption=use_decryption)['Parameter']['Value']

class Config:
    client = boto3.client('ssm', region_name='us-east-1')

    SECRET_KEY = get_parameter(client, 'SECRET_KEY', True)
    SQLALCHEMY_DATABASE_URI = get_parameter(client, 'SQLALCHEMY_DATABASE_URI', False)

    UPLOAD_FOLDER = basedir + '/static/audio/audio-files'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav'}
