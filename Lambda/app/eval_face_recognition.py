import torch
import torchvision.transforms as transforms
from PIL import Image
import json
import numpy as np
import build_custom_model
import base64
import boto3

base_path = '/tmp'

def convertToImg(imgPath, imgStr):
     with open(imgPath,"wb") as imageFile:
          imageFile.write(base64.b64decode(imgStr)) 

def recognition(img_path):
     labels_dir = "./checkpoint/labels.json"
     model_path = "./checkpoint/model_vggface2_best.pth"

     # read labels
     with open(labels_dir) as f:
          labels = json.load(f)
     #print(f"labels: {labels}")

     device = torch.device('cpu')
     model = build_custom_model.build_model(len(labels)).to(device)
     model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'))['model'])
     model.eval()
     print(f"Best accuracy of the loaded model: {torch.load(model_path, map_location=torch.device('cpu'))['best_acc']}")


     img = Image.open(img_path)
     img_tensor = transforms.ToTensor()(img).unsqueeze_(0).to(device)
     outputs = model(img_tensor)
     _, predicted = torch.max(outputs.data, 1)
     result = labels[np.array(predicted.cpu())[0]]
     img_name = img_path.split("/")[-1]
     img_and_result = f"({img_name}, {result})"
     print(f"Image and its recognition result is: {img_and_result}")
     return result

def getElement(label):
     dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
     table = dynamodb.Table('students_info')
     response = table.get_item(
          Key = {
        'label':label
     })
     item = response['Item']
     return item

def handler(event, context):
     if event['body']:
          print(event)
          body = json.loads(event['body'])
          imgStr = body['imgStr']
          imgName = body['imgName']
          imgPath = str(base_path) + '/' + imgName
          print(imgPath)
          convertToImg(imgPath, imgStr)
          recResult = recognition(imgPath)
          responseStr = getElement(recResult)
          print(responseStr)
          return {
          "statusCode": 200,
          "headers": {
            "Content-Type": "application/json"
          },
          "body": json.dumps({
            "userInfo": responseStr
          })
          }

#handler()
        
