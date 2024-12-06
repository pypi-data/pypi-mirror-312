import boto3
from botocore.exceptions import ClientError

class S3Helper():
    
    def __init__(self, aws_region: str, bucket_name: str):
        self.s3_client = boto3.client('s3', region_name=aws_region)
        self.aws_region = aws_region
        self.bucket_name = bucket_name
    
    
    def bucketExists(self) -> bool:
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError as e:
            return not e.response['Error']['Code'] == 404
        
    def createBucket(self):
        s3_resource = boto3.resource('s3', region_name=self.aws_region)
        s3_resource.create_bucket(Bucket=self.bucket_name)
                    
        
    def uploadFile(self, filepath: str, s3path: str) -> str:
        
        if not self.bucketExists():
            self.createBucket()
        
        response = self.s3_client.upload_file(filepath, self.bucket_name, s3path)
        
        return "https://" + self.bucket_name + '.s3.' + self.aws_region + '.amazonaws.com/' + s3path

class SnsHelper():
    
    def __init__(self, aws_region: str, topicname: str = None, arn : str = None):
        self.name = topicname
        self.aws_region = aws_region
        self.arn = arn
        self.sns_client = boto3.client('sns', region_name=aws_region)
    
    def assertTopicCreated(self):
        if self.arn is None:
            self.createTopic()
        
    def createTopic(self) -> str:
        topic_response = self.sns_client.create_topic(Name=self.name)
        
        self.arn = topic_response['TopicArn']
        
        return self.arn
        
    def subscribeEmail(self, email: str):
        self.assertTopicCreated()
        subscription_response = self.sns_client.subscribe(
            TopicArn=self.arn,
            Protocol='email',
            Endpoint=email
        )
    
    def publish(self, subject: str, message: str):
        self.assertTopicCreated()
        publish_response = self.sns_client.publish(
            TopicArn=self.arn,
            Message=message,
            Subject=subject
        )
        
        