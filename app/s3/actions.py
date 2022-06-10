import os
import boto3
from fastapi import HTTPException


def upload_file_to_bucket(file_obj, bucket, file_type, directory):
    s3_client = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                             aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
    file_as_binary = file_obj.file._file

    # Upload the file
    try:

        file_name = f'/{directory}/' + file_type
        # check files with the same type
        files_list = []
        bucket_obj = s3_client.list_objects(Bucket=bucket)
        for content in bucket_obj["Contents"]:
            key = content["Key"]
            if '_' in key and key[:key.index('_')] == file_name:
                files_list.append(key)

        file_name += f'_{len(files_list) + 1}'
        s3_client.upload_fileobj(file_as_binary, bucket, file_name)

    # TODO: Прописать ошибку
    except:
        return False

    return file_name


def create_url(file_name, expire_in=5):
    s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

    try:
        url = s3.generate_presigned_url('get_object', Params={'Bucket': 'backend.documents', 'Key': file_name},
                                        ExpiresIn=expire_in)
        return url

    # TODO: Прописать ошибку
    except:
        raise HTTPException(status_code=404, detail="There is not such document ")
