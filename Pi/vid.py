from picamera import PiCamera
from picamera import PiCameraCircularIO
import time
import RPi.GPIO as GPIO
import subprocess
import sys
import boto3
import threading
import random
from flask import Flask, request, jsonify
import requests
import base64
import io
import ast
import json
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from ast import literal_eval
import cv2
import os


def upload_file(file_name, bucket, object_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3', region_name='us-east-1', aws_access_key_id='AKIAU26NNX3KUZL2A6KE',
                             aws_secret_access_key='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')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_respnse(filepath, filename,start,num):
    with open(filepath, "rb") as img_file:
        img_as_byte = base64.b64encode(img_file.read())
    # img_as_byte = base64.b64encode(file.read())
    img_as_string = img_as_byte.decode('UTF-8')
    message = {"imgStr": img_as_string, "imgName": filename}
    message = json.dumps(message)
    # msg_body = 'Sending images to App Tier'
    uri = 'https://i94akakfz7.execute-api.us-east-1.amazonaws.com/test/facerecognition'
    r = requests.post(uri, message)
    # print ([filename,r.content, time.time()-start])
    user_info=literal_eval(r.content.decode('utf-8'))['userInfo']
    print(["Person " + str(num) + " recognized: " + user_info['first_name'] + ", " + user_info['major'] + ", " + user_info['year'] + ", " + "Latency: " + str(time.time()-start // 0.01 / 100)])
    return True


def capture_frame(num):
    # Read the video from specified path
    framepath='/home/pi/Desktop/video/frames/' + ('frame%02d.jpg' % num)
    vidpath='/home/pi/Desktop/video/vids/clip%02d.h264' % num
    cam = cv2.VideoCapture(vidpath)
    time.sleep(0.1)
    ret, frame = cam.read()
    if ret:
        cv2.imwrite(framepath, frame)
        start = time.time()
        get_respnse(framepath, 'frame%02d.jpg' % num,start,num)
        upload_file(vidpath, 'vidinput','clip%02d.h264' % num)
    cam.release()
    cv2.destroyAllWindows()

    return True

sensor = 12
camera = PiCamera()
camera.exposure_mode = 'antishake'
camera.resolution=(160,160)
time.sleep(2)

vid_dir = '/home/pi/Desktop/video/vids/'
frame_dir='/home/pi/Desktop/video/frames/'
recordDuration = 0.25
#Filename suffix for videos
j=1

camera.start_preview()

try:
    threads = []
    totstart = time.time()
    num=1
    for filename in camera.record_sequence(
            '/home/pi/Desktop/video/vids/clip%02d.h264' % i for i in range(1,601)):
        start = time.time()
        camera.wait_recording(0.5 - (time.time() - start))
        video_thread = threading.Thread(target=capture_frame, args=([num]))
        threads.append(video_thread)
        video_thread.start()
        num+=1

    for thread in threads:
        thread.join()

finally:
    print(time.time()-totstart)
    camera.stop_preview()
    camera.close()

