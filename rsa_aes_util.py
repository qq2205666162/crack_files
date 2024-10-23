import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5

import cv2
import open3d as o3d
import json
import numpy as np
import requests
import io
import time

from load_pcd import PointCloud

PRIVATE_PKCS1_PEM = """
-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC8D6tf0uj6PQJs
uWGOV69Xq7ZQky3ddgjP0OuarAWD1qu7iMAt0q3n7IYaZ8UmeQtPX3rJPuITTsWG
78q+Z8WS6eHs/NsY3FDvypzDs/2f8LRWMdk+BRG2otoizmM74UJNhER9LBx1/Nvk
bkHZlwHpzqoL+tou815f/7JZ9XGKDz8UadJiP2+Lur28qzf3gnyOfdrx0m9KcLyg
dYQX/rTiu1U3ZrN/9KG2dkqzQUqDs9iix5zJjSLtqQmckpdNA/UvgaTBsOdebfx5
IIl59PRVkflrbZzE7ETvdRNOtH0RHbsaVC98ctBKQmWd+SWP4qJYfSjUML03f48G
nfpgRlsrAgMBAAECggEAIJnSypTEYITtA64LVGKs+dTBkSxCei65DlWYUkLZ3eX7
9VGahxcLoLXm9XLhwW6gYE0b+wEUreYs5dxx2BojLPmweaXH0YJ34WnNTTvJjs1q
ZbrUfyTf0jpe+EOw/jNpjAiO2ugnsuh3shzO+4prAX4bCmKdKiB0Ts4DvAaJfTYl
RwyijwqHChPuZDAfVu/txI/3LD8gkW+SSlJhaDG7fCOszuKGIaA1ruZ3FSuFAgeB
wPZ6ZTI6r+/qMB7+B3tL9QpBqKAa82qALClIA9TmSgeOuxOCSvTwRc54kQh7BPqW
sUOnxTdE7nBt8dGaRAC9HJ0wz9QphHXMrW0wcuXR+QKBgQDj+rLrrf34nUo7P7K1
XbjO0qzuaeUdAwMEny6T2c1ER5K/RlDatPPEcoQf8wUJGIWwyGUT/va9UuczTdxj
XuAHGMz/KG4RQ7rAtz1+ZlXWWeE9yeaijjJuDJPQeCd5RZ3Wzw48nvAWGcPokDSW
UnSJUEWBwyGAZkB/5HVzlp73pQKBgQDTLPW1yrJmOHv9uD58ibcvfc+IaTrii+0s
QZ3sPdobue9xUAhqq3L895mcnporhstf+QZdiO8ip5Ck77Uj8YkYJpBxWMa7nbK5
dJCuK2snHFguyLUG6XoQsJGqUmR0LiisTWIumpBENkbptBK/eE8t+uS4gcV0uxbK
BNh4AQMOjwKBgF6a3jynC0lsHC3SFRrmNZa+Hj0hfI45fbshQ3bfXysCeIcfatYX
WUEgNGv9sQ1BO9lMj4VovIN8L60+lkI2UMkhJZCM+n/3lzv5zm7xkJVO3wWBD1BN
qee5GG3eLqNInGNTsRi+6+p/7qhHj0sCFJIW2YErtG9P/1wTNhotWvJxAoGAO5RB
top7jq98+/ZRWt2X20RJmxjlTilgPs48efxxXsU0sul7lmzMwmYw5qkwofsjwe4G
R7lsjoBsJLykhIGOxkuLEQ+U8jXpyL0EXL9POfebQYfK2ypgD/lg/4bDZKvpOcOT
Ycal0TjnBOSTLYYKANT6Vrv2M5rdMR3w3NqcPC0CgYBifjM8O5h9SR+2hjU/BL8w
0uNZt1V+c72vF/IiRqW/qI3lF7wsRk7X42MPkWmAIFl1gCEv8dbLZkusEw30gquB
3eBA1zCZUdUHvxMmbMwW/B9+mDRWpoH7LXDt8aIWfpbcQxe8UAchaEQnbnFVMap4
OvGxA0Efqwnmm0vIJSYSvg==
-----END PRIVATE KEY-----"""

def generateRsaPrivateKeyFromString(PRIVATE_PKCS1_PEM):
    adjustStr = PRIVATE_PKCS1_PEM.replace("-----BEGIN PRIVATE KEY-----", "")
    adjustStr = adjustStr.replace("-----BEGIN RSA PRIVATE KEY-----", "")
    adjustStr = adjustStr.replace("-----END PRIVATE KEY-----", "")
    adjustStr = adjustStr.replace("-----END RSA PRIVATE KEY-----", "")
    key = adjustStr.replace("\n", "")
    private_key = '-----BEGIN PRIVATE KEY-----\n' + key + '\n-----END PRIVATE KEY-----'
    return private_key

def decrype_rsa(encrpt_data, private_key):
    decodeStr = base64.b64decode(encrpt_data)
    rsakey = RSA.importKey(private_key)
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    cipher_text = cipher.decrypt(decodeStr,b'rsa')
    return cipher_text.decode('utf8')

def decryptFile(inputFile, outputFile):
    lines = open(inputFile,'r').readlines()
    encryptedAESKey = lines[0]
    encryptedAESData = lines[1]
    # rsa私钥解aes_key
    private_key = generateRsaPrivateKeyFromString(PRIVATE_PKCS1_PEM)
    aes_key = decrype_rsa(encryptedAESKey, private_key)
    # aes_key解加密数据
    aes = AES.new(base64.b64decode(aes_key), AES.MODE_ECB)
    decrypted_data = aes.decrypt(base64.b64decode(encryptedAESData))
    unpadded_data = unpad(decrypted_data, AES.block_size, style='pkcs7')
    with open(outputFile,'wb') as f:
        f.write(unpadded_data)

def test(file_name = '/home/yss/file1', save_name = 'image.jpeg'):
    
    decryptFile(file_name, save_name)

def deal_download_data(data):
    encryptedAESKey = data[0]
    encryptedAESData = data[1]
    # rsa私钥解aes_key
    private_key = generateRsaPrivateKeyFromString(PRIVATE_PKCS1_PEM)
    aes_key = decrype_rsa(encryptedAESKey, private_key)
    # aes_key解加密数据
    aes = AES.new(base64.b64decode(aes_key), AES.MODE_ECB)
    decrypted_data = aes.decrypt(base64.b64decode(encryptedAESData))
    unpadded_data = unpad(decrypted_data, AES.block_size, style='pkcs7')
    return unpadded_data

def getting_image(url_iamge):
    start_time = time.time()
    r_data = requests.get(url_iamge, allow_redirects=True)
    imageaa = np.empty((480, 640, 3), np.uint8)
    
    if r_data.status_code == 200:
        print("Download image sucesses!" + str(len(r_data.content)))
    else:
        print("Download image fails!" + str(r_data.status_code))
        return imageaa

    lines = r_data.text.splitlines()
    info_crackted = deal_download_data(lines)
   
    np_arr = np.asarray(bytearray(info_crackted), np.uint8).reshape(1, -1)
    imageaa = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)

    end_time_download = time.time()
    elapsed_time = end_time_download - start_time
    print("Download time use: "+ str(elapsed_time))

    return imageaa

def getting_pointcloud(url_pointcloud):
    start_time = time.time()
    r_data = requests.get(url_pointcloud, allow_redirects=True)
    
    if r_data.status_code == 200:
        print("Download pointcloud sucesses!" + str(len(r_data.text)))
    else:
        print("Download pointcloud fails!" + str(r_data.status_code))

    lines = r_data.text.splitlines()
    info_crackted = deal_download_data(lines)

    pc = PointCloud(io.BytesIO(info_crackted)).numpy(fields=['x', 'y', 'z', 'intensity', 'i'])

    end_time_download = time.time()
    elapsed_time = end_time_download - start_time
    print("Download time use: "+ str(elapsed_time))
    return pc, r_data.status_code

def getting_json(url_json):
    start_time = time.time()
    r_data = requests.get(url_json, allow_redirects=True)
    
    if r_data.status_code == 200:
        print("Download json file sucesses!" + str(len(r_data.text)))
    else:
        print("Download json file fails!" + str(r_data.status_code))

    lines = r_data.text.splitlines()
    info_crackted = deal_download_data(lines)
    position = json.loads(info_crackted)
    #print("position: ", position)
    end_time_download = time.time()
    elapsed_time = end_time_download - start_time
    print("Download time use: "+ str(elapsed_time))
    return position

if __name__=='__main__':

    test('/home/yss/mark_plantform/python-scripts/crack_files/image.txt')
    exit(0)


    inputfile = 'samples_new4/image0/1701757143925.jpeg'
    # inputfile = 'samples_new4/point_cloud/1701757143925.pcd'
    # inputfile = 'samples_new4/position/1701757143925.json'
    savefile = 'test.jpeg'
    decryptFile(inputfile, savefile)
