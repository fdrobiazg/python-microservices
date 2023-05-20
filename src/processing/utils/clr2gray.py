import json
from bson.objectid import ObjectId
import numpy as np
import cv2
import tempfile

def convert(message, gfs_src, gfs_out, channel): 
    message = json.loads(message)
    img = read_to_cv2(gfs_src, ObjectId(message['img_fid']))
    with tempfile.NamedTemporaryFile(suffix=".png") as tf:
        cv2.imwrite(tf.name, img)
        save(gfs_out, tf)

def read_to_cv2(gfs_src, objectid):
    img = gfs_src.get(objectid).read()
    img_arr = np.fromstring(img, np.uint8)
    img_np = cv2.imdecode(img_arr, cv2.IMREAD_GRAYSCALE)
    # img_cv = cv2.CreateImageHeader((img_np.shape[1], img_np.shape[0]), cv2.IPL_DEPTH_8U, 3)
    # cv2.SetData(img_cv, img_np.tostring(), img_np.dtype.itemsize * 3 * img_np.shape[1])

    return img_np

def save(gfs_out, file):
    try:
        res = gfs_out.put(file)
    except Exception:
        return f"Failed to save file.", 500


        
