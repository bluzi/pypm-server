import boto3
import json
from utils import config

s3 = boto3.client(
    's3',
    aws_access_key_id=config.aws_access_key,
    aws_secret_access_key=config.aws_access_secret
)


def get(package_name, version): 
    s3object = s3.get_object(Bucket=config.aws_bucket, Key='{}/{}'.format(package_name, version))
    return json.loads(s3object['Body'].read())


def publish(package_name, version, files):
    try: 
        get(package_name, version)
        version_exists = True
    except ValueError:
        version_exists = False

    if version_exists:
        raise ValueError('version {} already exists for package {}'.format(version, package_name))

    body = json.dumps({
        'files': files
    })

    s3.put_object(Bucket=config.aws_bucket, Key='{}/{}'.format(package_name, version), Body=body)


def list_versions(package_name):
    s3objects = s3.list_objects(Bucket=config.aws_bucket, Prefix='{}/'.format(package_name))

    if 'Contents' not in s3objects:
        raise ValueError('Package {} does not exist'.format(package_name))

    versions = list(map(lambda s3object: s3object['Key'].split('/')[1], s3objects['Contents']))
    versions.sort()

    return versions
