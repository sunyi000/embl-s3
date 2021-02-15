from minio import Minio
client = Minio("s3.embl.de", access_key="ysun-user", secret_key="PZx9Djtl7yeV7Kp5k8Gsm7y2SFJ2Gw6W", secure=True)
buckets = client.list_buckets()
for bucket in buckets:
    print (bucket).name

print (client.bucket_exists('platybrowser'))
print (client.get_bucket_policy('platybrowser'))