# textract
code to extract text using Amazon Textract and detect entities using Amazon Comprehend Medical. The detected entities are stored into a DynamoDB table. A sample image is provided in the images/ folder.
## Steps
NOTE: Before running make sure you have AWS CLI installed and configured with appropriate IAM privilages. Look at the following link that explains how to install and configure the AWS CLI:
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

\textbf {The default region for the CLI should be configured to the region where textract service is available.}

* download the repository to a folder.
* run setup.py using python setup.py stack_name (stack name is the name of the cloudformation stack). 

Ex: If your stack name is textract, you should run the command python setup.py textract.

* run Textract_Comprehend.py using  python Textract_Comprehend.py stack_name (stack name is the name of the cloudformation stack. Make sure its the same name as provided in the setup script). 


Ex: After setting up, you should run the command python Textract_Comprehend.py textract.


Once Executed, you will be able to see the output of textract on the command line. You can navigate to the DynamoDB table to view the entities extracted by Comprehend Medical.
