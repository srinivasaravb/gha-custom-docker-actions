import os
import boto3
import mimetypes
from botocore.config import Config


def run():
    aws_access_key = os.getenv("INPUT_AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("INPUT_AWS_SECRET_ACCESS_KEY")
    bucket = os.getenv("INPUT_BUCKET")
    bucket_region = os.getenv("INPUT_REGION")
    dist_folder = os.getenv("INPUT_DIS-FOLDER")

    configuration = Config(region_name=bucket_region)
    
    s3_client = boto3.client(
        's3',
        region_name=bucket_region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        config=configuration
    )

    for root, subdirs, files in os.walk(dist_folder):
        for file in files:
            s3_client.upload_file(
                os.path.join(root, file),
                bucket,
                os.path.join(root, file).replace(dist_folder + '/', ''),
                ExtraArgs={"ContentType": mimetypes.guess_type(file)[0]}
            )

    website_url = f'http://{bucket}.s3-website-{bucket_region}.amazonaws.com'
    # The below code sets the 'website-url' output (the old ::set-output syntax isn't supported anymore - that's the only thing that changed though)
    with open(os.environ['GITHUB_OUTPUT'], 'a') as gh_output:
        print(f'website-url={website_url}', file=gh_output)


if __name__ == '__main__':
    run()