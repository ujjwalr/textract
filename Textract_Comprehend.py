
import boto3
import os
from decimal import *
import sys
stack_name = str(sys.argv[1])

cfn = boto3.client('cloudformation')
s3 = boto3.client('s3')
textract = boto3.client('textract',region_name='us-east-2') #account whitelisted for only one region so overriding the default region here.
dynamoDBResource = boto3.resource('dynamodb', region_name = 'us-east-1')

#replace StackName with corresponding cloudformation stack name
bucket = cfn.describe_stacks(StackName=stack_name)['Stacks'][0]['Outputs'][0]['OutputValue']
ddb_table = cfn.describe_stacks(StackName=stack_name)['Stacks'][0]['Outputs'][1]['OutputValue']



cm  = boto3.client(service_name='comprehendmedical', use_ssl=True, region_name = 'us-east-2')
table = dynamoDBResource.Table(ddb_table)

                          
list=s3.list_objects(Bucket=bucket, Prefix='textract/images')['Contents']

for s3_key in list[1:]:
    s3_object = s3_key['Key']
    
    print ('extracting text from the image: '+ s3_object + '...')
    
    response = textract.detect_document_text(Document={'S3Object': {'Bucket': bucket, 'Name': s3_object}})

    textract_output = ''
    for Blocks in response["Blocks"]:
    	if Blocks['BlockType']=='LINE':
    		line = Blocks['Text']
    		textract_output = textract_output + line +'\n'

    #print (textract_output)
    print ('text extracted from image. Proceeding to extract clinical entities from the text...')
    
    Trait_List = []
    Attribute_List = []
    testresult = hera.detect_entities(Text = textract_output)
    testentities = testresult['Entities']
    rowid = 1
    #print(testentities)

    for row in testentities:
    	# Remove PHI from the extracted entites
        if row['Category'] != "PERSONAL_IDENTIFIABLE_INFORMATION":
        	for key in row:
        		if key == 'Traits':
        			if len(row[key])>0:
        				Trait_List = []
        				for r in row[key]:
        					Trait_List.append(r['Name'])
        		elif key == 'Attributes':
        			Attribute_List = []
        			for r in row[key]:
        				Attribute_List.append(r['Type']+':'+r['Text'])

        	#print('Text:'+row['Text']+'\n'+'Type:'+row['Type']+'\n'+'Category:'+row['Category']+'\n'+'Score:'+str(row['Score'])+'\n'+'Trait List:'+str(Trait_List)+'\n'+'Attribute List:'+str(Attribute_List))

        	table.put_item(
                Item={
                        'ROWID' : rowid,
                        'ID' : row['Id'],
                        'Text': row['Text'],
                        'Type' : row['Type'],
                        'Category' : row['Category'],
                        'Score' : Decimal(str(row['Score'])),
                        'Trait_List' : str(Trait_List),
                        'Attribute_List' : str(Attribute_List)
                        }
                    )
        rowid = rowid+1

   
    print ('\n\n\n\n****************************Extracted Text***************************\n\n\n\n')
    print (textract_output)
    print('\n\n\n\n**********************************************************************\n\n\n\n')
    print ('Entities extracted and inserted into dynamodb.')



	
     


    

