# Real-Time Face Recognition on PAAS
We are building a real-time scalable face recognition system on an Edge device, Raspberry Pi. In project 1, we were using building IAAS service where EC2 instances keep running even when we are not using, while in this project we are using serverless component AWS Lambda to implement Function as a Service and invoking lambda function only when we need recognition.  In this project, we are trusting the cloud for autoscaling and other features, so that we can focus more on the problem of concern given a reliable face recognition system with high accuracy.

![alt text](PAAS.png)


## Architecture Description

### Raspberry Pi

The raspberry pi is the starting component of this service with the responsibility of constantly recording videos, uploading them to the cloud and listening for image recognition responses. In order to perform all these activities, the raspberry pi interacts with S3 and Amazon Lambda (through API Gateway)

### AWS Lambda

Lambda is a compute service that lets us run code without provisioning or managing servers. Here the code is organized into functions. Lambda runs the function only when needed and scales automatically. In our project, the lambda function was used to implement one of the core functionalities of our application, i.e. face recognition. The lambda function is created using a docker image deployed to Amazon Elastic Container Registry (ECR). Our lambda function is responsible for processing the requested image frame sent from pi, perform face recognition on the image and fetch the results of the identified person from DynamoDB back to pi


### Amazon API Gateway

Using API Gateway we can create RESTful APIs that enable real-time two-way communication in applications. In our project, we built a Lambda proxy integration using API gateway. In this way, the input to the integrated lambda function could be expressed in the body of the request and the response could be sent to the client, which is pi in our case.


### S3
Amazon Simple Storage Service (S3) stores huge amounts of data (even in terabytes) and dynamically grows as per the requirement. We are using S3 bucket “vidinput” to store the recorded videos. This bucket contains the video name as the key.

### DynamoDB

AWS DynamoDB manages the scalable NoSQL database server. We created the student_info table and stored teammates' information from the boto3 library. When we get frame results from the trained model from docker, with the output label, we are getting the person's information from the DynamoDB as shown in the project architecture.




<!-- ### Custom face-recognition model
https://drive.google.com/drive/folders/1qrNfLNGy0WS8_L82BnHh-5EwQwSGUYwJ?usp=sharing

### Instruction to use this project
    - Power on the raspberry pi.
    - Connect to it via monitor or ssh.
    - Install required python modules using the pip install command.
    - Transfer the python file via SCP.
    - To run the real-time face recognition application, go the the appropriate folder & execute the following command: python vid.py

### AWS Credentials
    Access key ID: AKIAU26NNX3KUZL2A6KE
    Secret access key: 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
    Region: US East (N. Virginia) us-east-1

### S3 Bucket Name
    vidinput

### DynamoDB Table
    Table Name: student_info
    Partition Key: label
### API Gateway
    uri = 'https://i94akakfz7.execute-api.us-east-1.amazonaws.com/test/facerecognition'
    message = {"imgStr": img_as_string, "imgName": filename}

### AWS Lambda
    Function Name: faceRecognitionCore
    Invocation Type: http request through API gateway

### Team:57
    Mani Sai Tejaswy Valluri (mvallur2@asu.edu)
    Pavan Mallina (pmallina@asu.edu)
    Takshshila Rawat (trawat2@asu.edu) -->
