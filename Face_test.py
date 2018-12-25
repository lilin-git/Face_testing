# -*- coding: utf-8 -*-
import aip
from aip import AipBodyAnalysis
from aip import AipOcr
from aip import AipFace
from PIL import Image
import numpy as np
import time
import os
import base64
import copy
from shutil import copyfile

image_raw = '/home/pushi_dev/a-ll/Face_testing/image_raw/'
photo = '/home/pushi_dev/a-ll/Face_testing/photo/'
output = '/home/pushi_dev/a-ll/Face_testing/output/'
#检测人脸
def face_recognition(face):
    APP_ID = '14967518'
    API_KEY = '9t30hVBaZ1nBz7KRTF7iAbVn'
    SECRECT_KEY = 'q9PAF4h0dyADGYnuK3eNbptwfl5VTCGy'

    client = AipFace(APP_ID, API_KEY, SECRECT_KEY)

    file_road = face
    i = open(file_road, 'rb')
    img = base64.b64encode(i.read())
    print("face alignment in processing")

    imageType = "BASE64"
    options = {
        "face_field": "age",
        "max_face_num": 1,
        "face_type": "LIVE"
    }


    """ 带参数调用人脸检测 """
    try:
        message = client.detect(img, imageType, options)
        if message[u'result'] == None:
            return None
        else:
            return message
    except Exception as s:
        return s

#人脸切割
def face_cut(file_road, message):
    width = message[u'result'][u'face_list'][0][u'location'][u'width']
    top = message[u'result'][u'face_list'][0][u'location'][u'top']
    left = message[u'result'][u'face_list'][0][u'location'][u'left']
    height = message[u'result'][u'face_list'][0][u'location'][u'height']
    img_1 = Image.open(file_road)
    filename = os.path.basename(file_road)
    # 建立文件夹（以图片名称为文件夹名称）在output文件夹里面
    if os.path.exists(output) == True:
        region = img_1.crop((int(left), int(top), int(left) + int(width), int(top) + int(height)))
        region.save(output + 'face_' + filename)

#人脸搜索
def face_alignment(face):
    APP_ID = '14967518'
    API_KEY = '9t30hVBaZ1nBz7KRTF7iAbVn'
    SECRECT_KEY = 'q9PAF4h0dyADGYnuK3eNbptwfl5VTCGy'

    client = AipFace(APP_ID, API_KEY, SECRECT_KEY)
    file_road = face
    i = open(file_road, 'rb')
    img = base64.b64encode(i.read())
    imageType = "BASE64"

    groupIdList = "0"

    """ 调用人脸搜索 """
    try:
        message = client.search(img, imageType, groupIdList)
        # print message
        if message[u'result']:
            group_id = message[u'result'][u'user_list'][0][u'group_id']
            user_id = message[u'result'][u'user_list'][0][u'user_id']
            score = message[u'result'][u'user_list'][0][u'score']
            return group_id, user_id, score
        else:
            return None, None, None
    except Exception as e:
        print(e)


if __name__ == '__main__':


    for filename in os.listdir(image_raw):
        if '.jpg' or '.jpeg' or '.png' in filename:
                message = face_recognition(image_raw+filename)
                if message:
                    face_cut(image_raw+filename, message)
                    print('面部切割完成')
                else:
                    print('没有面部信息')
        else:
            pass


    for filename in os.listdir(output):
        if '.jpg' or '.jpeg' or '.png' in filename:
            group_id, user_id, score = face_alignment(output+filename)
            print(score)
        else:
            pass
