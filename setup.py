import boto3
import sys

cfn = boto3.client('cloudformation')
s3 = boto3.resource('s3')
stack_name = str(sys.argv[1])

print ('Creating stack '+stack_name+'....')

with open('dynamo_s3.yaml', 'r') as template:
  data = template.read()

cfn.create_stack(StackName = stack_name, TemplateBody=data)


waiter = cfn.get_waiter('stack_create_complete')
waiter.wait(StackName=stack_name)



bucket = cfn.describe_stacks(StackName=stack_name)['Stacks'][0]['Outputs'][0]['OutputValue']
table = cfn.describe_stacks(StackName=stack_name)['Stacks'][0]['Outputs'][1]['OutputValue']


s3.meta.client.upload_file(Filename = 'images/textract1.jpg', Bucket = bucket, Key = '/images/textract1.jpg')


print ('Stack '+stack_name+'created.')
print ('S3 bucket name: '+bucket)
print ('DynamoDB table name: '+table)

