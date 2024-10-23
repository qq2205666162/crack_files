import time
import cv2
import numpy as np
import rsa_aes_util
import requests
import io
from load_pcd import PointCloud
import open3d as o3d
import json
import detection_final.interface_all_obj as iao

def test_getting_image(url_iamge):
    start_time = time.time()
    r_data = requests.get(url_iamge, allow_redirects=True)
    
    if r_data.status_code == 200:
        print("Download image sucesses!" + str(len(r_data.content)))
    else:
        print("Download image fails!" + str(r_data.status_code))

    lines = r_data.text.splitlines()
    info_crackted = rsa_aes_util.deal_download_data(lines)
   
    np_arr = np.asarray(bytearray(info_crackted), np.uint8).reshape(1, -1)
    imageaa = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)

    end_time_download = time.time()
    elapsed_time = end_time_download - start_time
    print("Download time use: "+ str(elapsed_time))

    
    json_result1 = iao.detect_pdface(imageaa, 0.5)
    json_result2 = iao.detect_nusc(imageaa, 0.5)
    json_result3 = iao.detect_coco(imageaa, 0.5)

    cv2.namedWindow('img_show', 0)
    cv2.imshow('img_show', imageaa)
    cv2.waitKey(0)

def test_getting_pointcloud(url_pointcloud):
    start_time = time.time()
    r_data = requests.get(url_pointcloud, allow_redirects=True)
    
    if r_data.status_code == 200:
        print("Download pointcloud sucesses!" + str(len(r_data.text)))
    else:
        print("Download pointcloud fails!" + str(r_data.status_code))

    lines = r_data.text.splitlines()
    info_crackted = rsa_aes_util.deal_download_data(lines)


    pc = PointCloud(io.BytesIO(info_crackted)).numpy(fields=['x', 'y', 'z', 'intensity', 'i'])

    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name='draw result')
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0]) 
    opt.point_size = 1

    point_cloud = o3d.geometry.PointCloud()
    for i in range(len(pc)):
        point_cloud.points.append([pc[i][0], pc[i][1], pc[i][2]])

    end_time_download = time.time()
    elapsed_time = end_time_download - start_time
    print("Download time use: "+ str(elapsed_time))

    vis.add_geometry(point_cloud)
    vis.run()

def test_getting_json(url_json):
    start_time = time.time()
    r_data = requests.get(url_json, allow_redirects=True)
    
    if r_data.status_code == 200:
        print("Download json file sucesses!" + str(len(r_data.text)))
    else:
        print("Download json file fails!" + str(r_data.status_code))

    lines = r_data.text.splitlines()
    info_crackted = rsa_aes_util.deal_download_data(lines)

    position = json.loads(info_crackted)

    print("position: ", position)
    end_time_download = time.time()
    elapsed_time = end_time_download - start_time
    print("Download time use: "+ str(elapsed_time))




if __name__ == '__main__':
    
    #url_iamge = 'https://test-cloud-control-1258234669.cos.ap-guangzhou.myqcloud.com/217/1263/2af4da02bf6b4e89afe568cca87cbe38/samples_new_2/image3/1701757144425.jpeg?sign=q-sign-algorithm%3Dsha1%26q-ak%3DAKIDDtSIVfIjXgB1evJtlt3tLlWiBtMytOKvYLmrwTRIKGEKmH8NOfjuqynJV7jdclJ4%26q-sign-time%3D1717571676%3B1717575276%26q-key-time%3D1717571676%3B1717575276%26q-header-list%3Dhost%26q-url-param-list%3D%26q-signature%3Dd40897ffec7c09e75d057e25a4259c9b58dbe53f&x-cos-security-token=8TflOKMDHDmyGAyQAiYkvLlWvjPWOkVaa8fe9c835bffffce96789fa107b901e4-XQe6wzOSoPRT7PCDIa3J6H45cKILwBELeXsefUMF-kzncyhd26wsvftZU99LjdCI878tCerBAHuMg_jKl6Ks14hFTshfVr1H4zNJ7HORzAIqN7bpdJeOjpW5GhgU_YRaZ9Futh7dLwoMAiUPGkDkoivi54UvSyiZ2OV4X7n6Itm7CGuG4gEFtxeD8_44q5TAjIrFodP6mQvZjfJJ5mo7Uie3Hv09k3_WoBcHBGQAfutff_iRL1dqnlMDRtJT8zhCAZBjmRE04WN7LWQQQ-EuQFBVP5r7e1P4qSEVSKhKACoHM4SaOXOWcMMriokJMVRJSvTSPcpmMVHa1DVUHk0ZBx2z2Lg-tMUorVRAa-rbHXs11UmdmaG0r9yuJJu-pdpASqOG18QTpjT1ZKJRgVXXZuQdfuGuyu-TrQhFuubT2tkl-PN7sZM568aqACRUc81rxkJ7qvvk96IugQ-I4pFEmltzWY-K4DJmmHPpYU1ap8jXfW0CWZha5Qiim2QcTqfTm-efrb4SFPwpOMe5GL1jQnlJbmY5sdrQS4R7iD_XTOrKjHfN2x-qBMBgn9cDbniB_CtqlWnxOCASqMi_4cDyqWx_vG2uAGuAKetr1Av8RCxzQra1zbtgayAOEUVuiQ3m16KG9zEgJzzsqwp483l0wGjkLo2v8za8W86fjac8i2EiKTwMuLWWmCNFe2Mv04IOTpvKRFg6EpbqiMPbgKJJs1Azbn_z4AcB4s1xVE2vX-z4yjtjV56UULHbRJi0uoG'
    #test_getting_image(url_iamge)

    #url_pointcloud = 'https://test-cloud-control-1258234669.cos.ap-guangzhou.myqcloud.com/40/1180/3941f36a67f748a89e13eecd7d9724be/GACRT015_1715846504_ruqi/point_cloud/1715846523700000000_640_195.pcd?sign=q-sign-algorithm%3Dsha1%26q-ak%3DAKIDRYccl4fZt8qtkLVD057lbWY59DHTIVA8sVjRRSgpeiCoBbSXg9b5Bvo5UvpX5x8b%26q-sign-time%3D1718791422%3B1718921022%26q-key-time%3D1718791422%3B1718921022%26q-header-list%3Dhost%26q-url-param-list%3D%26q-signature%3D6460883684be74d0184ee521b1dabfd1f8c99e77&x-cos-security-token=5HRdOZqa3F9CCP2m5rVLe4JLbcADugdad07672c25a234183f452c83988b03461P_oeQ3bdZFmaKmf6Q6J_mIU__HTY2BAaZKpmba9vKDNbHMDfn7IpGcYMnzCO5_fwIUR3MA4oMIaQf1htN98Dhmr7Yyy5twYEP7Ra4weJQHgynEaXu1sBrInp28NfL37zKwfFD2i8X5QHRbILTwrVurQpjtqYqjqcBhCL6RgxjrEa1Ssdc34L1GbeFh9flU0T9Hqg1Hn9P9U6eP-7MBglwmTlUm8bNHXOKIHacccLX8kOL50aAr3InCMpNPKoCF5hQajwcXDlZCRH8ZkGfas1iLPwO4w-zylhVhuLEDDouxzAvuTCU92o0MIikWqpCJ23cOOgPNrJQ5mizDqhG5B2Xb2YP8aTTe-aRYHfGJ_d_tUAVFZ1DJG9xpXNwop9YlQTJDoYts0EY5iYR9WzkhXmuCmeBcUy5bqnWTySm-vQzsSXjPZiG8YDKQvxcqQjkx_1Dt6zShiIRLMin_JcGV9OI42jXma0kNoQ1eeFPa5ISO4Oyfa5Osy5dMfJtagP8thq30BLGoTm7qDV3zd94UXVnCJAXDtFvIFjivCNWVQpNyGrnKHMfhgzQ6eGAvehCWnJgPsk0BMFxtsJgjus6taoqDuFwdZwSMVwF-IcdVS6aiZnHv7vISin2CnyycXLpNKladtR5vhGNFe8_l5I5XjA94OpBt9WwYrjU4yWzDWmyaXtnTImGfDcM4g-DjWhnasEb6-NHoI5yXn-8hq6iqwqtg1I6pLDRG2rywxsiuHWHzG_SXVYEerisDA4sWsr-aDK'
    #test_getting_pointcloud(url_pointcloud)

    url_json = 'https://test-cloud-control-1258234669.cos.ap-guangzhou.myqcloud.com/217/1626/354e53885b124615a9e9b0df06d63f79/samples_new_2/camera_config/1701757143925.json?sign=q-sign-algorithm%3Dsha1%26q-ak%3DAKID636qUVr_rlgFGFwu18TC8fm8euNnk-80vsmVYy3TYypnhL09r9shI-0Z9Zmv72GQ%26q-sign-time%3D1719478796%3B1719608396%26q-key-time%3D1719478796%3B1719608396%26q-header-list%3Dhost%26q-url-param-list%3D%26q-signature%3Db3f4c5d86b7349016e770604089374960a21972b&x-cos-security-token=zBe0Oo4CPX7n5utv2PIhRJDFRw6QsuSa8e4caf1c6614a2800db07aedfed0a0a4smLksXN0g1JDfXGzeMa23vSGKrWTnQPOmoH_Mboo8HD9OJS0gXFR1oHMVYeZtPYxBMzYTztfXgiE7R3aSWgyJWZDb5snTte-U0askCVeem4M_cS4WopMktPvQMhlseG5Fz3heubzqFtYRPJdcYHV3Q2pGHrn8c_GNc0Ax9mOrrF2ccqcHAz-9-Cwv64MvS-YAIxdkam7wBzceS8jSQIrOpBqo_3tfETpPDZ--gN9ddxP8-ULKIbsKY16Yxh65RjDMAcN0CsgUXZLxk_Khj2j_95gD0QMS_tTmqYdqBLsUmNhR0K2faBH5pQkSc-y4l6cnOy9eivbKushJRX5Lg0XXhKt0bnOG8BIz_K3P4QQj54MEx2ScI0iG7861djcjeNlkdbrgwx0W-24QZaPS47sN2dwGqnosi4mpPV1VIj-n6teFqBcTrWyb4M3ASC-5dd9A1b48DBR63u_hwHYnhJcz0iacb8CWykLubOs7_otHX7zahBO-mwmDyIWfxUjsrpd0mlRW0582wvRf94RLj-qRwGnPRclbc6cAGLcaLQ9f6mWJzh0Qr1sM06uDgGxKwz-DaGT9pleMv3yYY0q9jYL6dPJlL21YH821RwlQ-qm7-uy8HbK6eVEWwDMdFxCkwm59uLwMsK5SsuHEeQrswUmBCUDAt84gXGpyrw-Ubzun2KinLl-ILs9HYA1nvTvpobgSTgidyheuRQJWcyi5FNJXXH4RmSgbnJJYU7sH6tumGJrYbKwv0OXz9I_5ogmsGpO'
    test_getting_json(url_json)
