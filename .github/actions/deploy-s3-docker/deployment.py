import os
import boto3
import mimetypes
from botocore.config import Config


def run():
    bucket = os.getenv("INPUT_BUCKET")
    region = os.getenv("INPUT_REGION")
    dist_folder = os.getenv("INPUT_DIS_FOLDER")  # ✅ correct

    if not dist_folder:
        raise ValueError("dist_folder is missing")

    s3_client = boto3.client(
        "s3",
        config=Config(region_name=region)
    )

    for root, _, files in os.walk(dist_folder):
        for file in files:
            file_path = os.path.join(root, file)
            s3_key = file_path.replace(dist_folder + "/", "")

            s3_client.upload_file(
                file_path,
                bucket,
                s3_key,
                ExtraArgs={
                    "ContentType": mimetypes.guess_type(file)[0] or "application/octet-stream"
                }
            )

    website_url = f"http://{bucket}.s3-website-{region}.amazonaws.com"

    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
        print(f"website-url={website_url}", file=fh)


if __name__ == "__main__":
    run()