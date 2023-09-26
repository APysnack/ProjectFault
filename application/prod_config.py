import os 
import boto3

basedir = os.path.abspath(os.path.dirname(__file__))

path = '/project-fault/prod/'

def get_parameter(client, parameter_name, use_decryption):
    return client.get_parameter(Name=f'{path}{parameter_name}', WithDecryption=use_decryption)['Parameter']['Value']

class Config:
    client = boto3.client('ssm', region_name='us-east-1')

    rds_endpoint = get_parameter(client, 'RDS_ENDPOINT', False)
    rds_username = get_parameter(client, 'RDS_USER_NAME', False)
    rds_password = get_parameter(client, 'RDS_PASSWORD', True)
    rds_port = get_parameter(client, 'RDS_PORT', False)
    rds_db_name = get_parameter(client, 'RDS_DB_NAME', False)

    SQLALCHEMY_DATABASE_URI = f"postgresql://{rds_username}:{rds_password}@{rds_endpoint}:{rds_port}/{rds_db_name}"


    SECRET_KEY = get_parameter(client, 'SECRET_KEY', True)

    IMAGE_UPLOADS = 'https://project-fault-media.s3.amazonaws.com/'
    UPLOAD_FOLDER = basedir + '/static/audio/audio-files'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav'}
