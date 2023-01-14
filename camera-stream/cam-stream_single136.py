import cv2
import numpy as np

import requests

'''
INFO SECTION
- if you want to monitor raw parameters of ESP32CAM, open the browser and go to http://192.168.x.x/status
- command can be sent through an HTTP get composed in the following way http://192.168.x.x/control?var=VARIABLE_NAME&val=VALUE (check varname and value in status)
'''

# ESP32 URL
URL = "http://192.168.43.136"
AWB = True

# Face recognition and opencv setup
cap = cv2.VideoCapture(URL + ":81/stream")

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
    set_resolution(URL, index=camera_res)

    while True:
        if cap.isOpened():
            ret, frame = cap.read()

            imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
            imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                 cv2.THRESH_BINARY_INV, 25, 16) 
            imgMedian = cv2.medianBlur(imgThreshold, 5)
            kernel = np.ones((3, 3), np.uint8)
            imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
            cv2.imshow("Frame tres", imgThreshold)
            cv2.imshow("frame", frame)
            key = cv2.waitKey(1)

            if key == ord('q'):
                break

    cv2.destroyAllWindows()
    cap.release()