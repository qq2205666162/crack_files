import os
import cv2
import numpy as np
import time

def listPathAllfiles(dirname):
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            result.append(apath)
    return result


def h265_to_jpg(video_path, name_front):
    #video_path = '/home/yss/下载/20240619_173159/camera_70.h265'  #2024-04-22_11-21-34.h265 2024-04-22_11-20-46  2024-04-22_11-19-48
    cap = cv2.VideoCapture(video_path)
    #cap = cv2.VideoCapture(0)
    num = 0
    cv2.namedWindow('12', 0)

    while True:
        if num % 150 != 0:
            num = num + 1
            continue
        ret, frame = cap.read()

        if ret:
            ret = ret + 1
        else:
            break

        #cv2.imshow('12', frame)
        #cv2.waitKey(1)
        save_name = os.path.join(name_front, str(num) + '.jpg')
        print('save_name: ', save_name)
        cv2.imwrite(save_name, frame)
        num += 1
        
        
    #    if ret:
    #        if  num%4 == 0 :
    #            cv2.imwrite('C:/Users/Zhangliangshan/Videos/Captures/%d.jpg' % num, frame)  #e:\Zxr Files\my project\11111\Downloads
    #        num += 1
            
    #    else:
    #        break
    cap.release()
    cv2.destroyAllWindows()

def run_grab_fish_data(path_in = '', save_path = ''):
    all_h265 = listPathAllfiles(path_in)
    for h265 in all_h265:
        name_split_all = h265.split("/")
        final_name = name_split_all[len(name_split_all) - 1]
        final_name2 = name_split_all[len(name_split_all) - 2]
        index = final_name.index('.')
        name_prue = final_name[0:index]

        new_name_front = os.path.join(final_name2, name_prue)
        new_name_front = os.path.join(save_path, new_name_front)

        if not os.path.exists(new_name_front): 
            os.makedirs(new_name_front)

        h265_to_jpg(h265, new_name_front)


def del_data(path = '/home/yss/workspace/get_images/fish_data'):
    all_image = listPathAllfiles(path)
    num = 0
    for img_path in all_image:
        num = num + 1
        if num % 8 == 0:
            continue
        else:
            os.remove(img_path)



if __name__ == '__main__':
    del_data()
    exit(0)
    save_path = '/home/yss/workspace/get_images/fish_data'
    run_grab_fish_data('/home/yss/下载/20240619_173159', save_path)

    #h265_to_jpg()    # split_video()
