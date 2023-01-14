import cv2
import numpy as np
import pickle

width, height = 50, 50
PATH_img = ".\\car-slot-detection\\data_sampleVideo\\CAM.136.png"
#PATH_img = ".\\car-slot-detection\\data_sampleVideo\\CAM.136.png"
PATH_pos = ".\\car-slot-detection\\data_posisi\\"

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)

def split_list(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out


def mouseClick(events, x, y, flags, params):
	if events == cv2.EVENT_LBUTTONDOWN:
		posList.append((x, y))
	if events == cv2.EVENT_RBUTTONDOWN:
		for i, pos in enumerate(posList):
			x1, y1 = pos
			if x1 < x < x1 + width and y1 < y < y1 + height:
				posList.pop(i)

	# Simpan titik koordinat
	with open(PATH_pos+'titik_koordinat_136', 'wb') as f:
		pickle.dump(posList, f)

	# Simpan titik polygon
	if len(posList) != 0 and len(posList)%4 == 0:		
		total_poly = len(posList)//4
		pts_poly = list(split_list(posList, total_poly))
		with open(PATH_pos+'titik_polygon_136', 'wb') as f:
			pickle.dump(pts_poly, f)


# =====================================================================
try:
	with open(PATH_pos+'titik_koordinat_136', 'rb') as f:
		posList = pickle.load(f)
except:
	posList = []
while True:
	img = cv2.imread(PATH_img)
	# Anotasi titik koordinat
	for pos in posList:
		x, y = pos[0], pos[1]
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(img, str(x)+','+str(y), (x, y),
					font, 0.2, COLOR_BLUE, 1)
	
	# Anotasi ROI polygon
	if len(posList) != 0 and len(posList)%4 == 0:		
		with open(PATH_pos+'titik_polygon_136', 'rb') as f:
			pts_poly = pickle.load(f)
		for count, poly in enumerate(pts_poly):
			pts = np.array(poly, np.int32)
			pts = pts.reshape((-1,1,2))
			cv2.polylines(img, [pts], isClosed=True,
						  color=COLOR_GREEN, thickness=1)
	cv2.imshow("ROI CAM136", img)
	cv2.setMouseCallback("ROI CAM136", mouseClick)
	k = cv2.waitKey(10)
	# Exit camera
	if k == 27:
		cv2.destroyAllWindows()
		break