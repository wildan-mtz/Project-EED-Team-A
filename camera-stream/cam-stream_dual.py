import cv2
import numpy as np

import requests

'''
INFO SECTION
- if you want to monitor raw parameters of ESP32CAM, open the browser and go to http://192.168.x.x/status
- command can be sent through an HTTP get composed in the following way http://192.168.x.x/control?var=VARIABLE_NAME&val=VALUE (check varname and value in status)
'''

# ESP32 URL
URL_CAM0 = "http://192.168.43.136"
URL_CAM1 = "http://192.168.43.81"
AWB = True

# Face recognition and opencv setup
cap_0 = cv2.VideoCapture(URL_CAM0 + ":81/stream")
cap_1 = cv2.VideoCapture(URL_CAM1 + ":81/stream")

def set_resolution(url: str, index: int=1, verbose: bool=False):
    try:
        if verbose:
            resolutions = """10: UXGA(1600x1200)\n
                            9: SXGA(1280x1024)\n
                            8: XGA(1024x768)\n
                            7: SVGA(800x600)\n
                            6: VGA(640x480)\n
                            5: CIF(400x296)\n
                            4: QVGA(320x240)\n
                            3: HQVGA(240x176)\n
                            0: QQVGA(160x120)"""
            print("available resolutions\n{}".format(resolutions))

        if index in [10, 9, 8, 7, 6, 5, 4, 3, 0]:
            requests.get(url + "/control?var=framesize&val={}".format(index))
        else:
            print("Wrong index")
    except:
        print("SET_RESOLUTION: something went wrong")

camera_res = 7
if __name__ == '__main__':
    set_resolution(URL_CAM0, index=camera_res)
    set_resolution(URL_CAM1, index=camera_res)
    while True:
        if cap_0.isOpened() and cap_1.isOpened():
            ret, frame0 = cap_0.read()
            ret, frame1 = cap_1.read()

            imgGray0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
            imgBlur0 = cv2.GaussianBlur(imgGray0, (3, 3), 1)
            imgThreshold0 = cv2.adaptiveThreshold(imgBlur0, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                 cv2.THRESH_BINARY_INV, 25, 16) 
            imgGray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            imgBlur1 = cv2.GaussianBlur(imgGray1, (3, 3), 1)
            imgThreshold1 = cv2.adaptiveThreshold(imgBlur1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                 cv2.THRESH_BINARY_INV, 25, 16) 

            cv2.imshow("Live CAM0", frame0)
            cv2.imshow("Live CAM1", frame1)

            cv2.imshow("Live Tresh CAM0", imgThreshold0)
            cv2.imshow("Live Tresh CAM1", imgThreshold1)

            key = cv2.waitKey(1)
            if key == 27:
                break

    cv2.destroyAllWindows()
    cap_0.release()
    cap_1.release()