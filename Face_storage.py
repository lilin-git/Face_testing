# -*- coding: utf-8 -*-
import base64
from aip import AipFace
import os
from Face_testing import face_recognition, face_alignment

photo = '/home/pushi_dev/a-ll/Face_Distinguish/photo/'

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


    """ 如果有可选参数 """
    options = {}
    options["quality_control"] = "NORMAL"

    """ 带参数调用人脸注册 """
    try:
        client.addUser(img, imageType, groupId, userId, options)
    except Exception as e:
        print e


if __name__ == '__main__':
    count = 0
    for filename in os.listdir(photo):
        if '.jpg' or '.jpeg' or '.png' in filename:
            message = face_recognition(photo+filename)
            if message:
                group_id, user_id, score = face_alignment(photo + filename)
                if score > 88:
                    # print group_id, user_id, score
                    face_storage(photo + filename, user_id, group_id)
                else:
                    face_storage(photo+filename, count)
                    count += 1
                # os.remove(photo+filename)
            else:
                pass