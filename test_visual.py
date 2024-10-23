import json
import math
import open3d as o3d
import numpy as np
import os
import cv2
import pickle


def listPathAllfiles(dirname):
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            result.append(apath)
    return result

def check_results(loaded_data):
    detections = loaded_data
    for i, voli in enumerate(detections['dets']['velocity']):
        detections['dets']['velocity'][i] = [0, 0]
    return detections



def visual(path = '/home/yss/下载/yss'):
    all_files = listPathAllfiles(path)
    files_sorted = sorted(all_files)

    for file in files_sorted:
        with open(file, 'rb') as f:
            loaded_data = pickle.load(f)
            print("loaded_data: ", loaded_data)
            detections = check_results(loaded_data)
            #save_data = {}
            #save_data['dets'] = detections
            #print("save_data: ", save_data)
            with open(file, 'wb') as f2:
                pickle.dump(detections, f2)
            
            break



if __name__ == '__main__':


    visual()