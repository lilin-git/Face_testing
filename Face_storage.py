# -*- coding: utf-8 -*-
import base64
from aip import AipFace
import os
from Face_testing.Face_test import face_recognition, face_alignment
photo = '/home/pushi_dev/a-ll/Face_testing/photo/'

def face_storage(image, userId, group_Id='0'):
    APP_ID = '14967518'
    API_KEY = '9t30hVBaZ1nBz7KRTF7iAbVn'
    SECRECT_KEY = 'q9PAF4h0dyADGYnuK3eNbptwfl5VTCGy'

    client = AipFace(APP_ID, API_KEY, SECRECT_KEY)
    file_road = image
    i = open(file_road, 'rb')
    img = base64.b64encode(i.read())
    imageType = "BASE64"

    groupId = str(group_Id)

    userId = str(userId)


    options = {
        "quality_control": "NORMAL"
    }

    """ 带参数调用人脸注册 """
    try:
        client.addUser(img, imageType, groupId, userId, options)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    count = 5
    for filename in os.listdir(photo):
        if '.jpg' or '.jpeg' or '.png' in filename:
            message = face_recognition(photo+filename)
            if message:
                group_id, user_id, score = face_alignment(photo + filename)
                if score > 85:
                    # print group_id, user_id, score
                    print('用户云端有人脸相册,用户user_id:%d'%user_id)
                    face_storage(photo + filename, user_id, group_id)
                else:
                    print('用户云端没有人脸相册，新建user_id:%d'%count)
                    face_storage(photo+filename, count)
                    count += 1
                # os.remove(photo+filename)
            else:
                pass