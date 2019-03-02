# textract
code to extract text using Amazon Textract and detect entities using Amazon Comprehend Medical.
## Steps
NOTE: Before running make sure you have AWS CLI installed and configured with appropriate IAM privilages and also for the region that is whitelisted for Textract.Once Textract is GA, You can ignore this restriction.  
* download the repository to a folder.
* run setup.py using $ python setup.py stack_name (stack name is the name of the cloudformation stack)
* run Textract_Comprehend.py using $ python Textract_Comprehend.py stack_name (stack name is the name of the cloudformation stack. Make sure its the same name as provided in the setup script.)
