import cv2, pickle, cvzone, requests
import numpy as np

# Stream webserver camera
URL_cam81 = "http://192.168.43.81:81/stream"
URL_cam136 = "http://192.168.43.136:81/stream"
requests.get(URL_cam81 + "/control?var=framesize&val=7")
requests.get(URL_cam136 + "/control?var=framesize&val=7")
cam_81 = cv2.VideoCapture(URL_cam81)
cam_136 = cv2.VideoCapture(URL_cam136)
AWB = True

PATH_data = ".\\car-slot-detection\\data_posisi\\"

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)



#def frameImagePro(frameOri):
#	ret, frame = frameOri.read()
#	imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#	imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
#	imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#												 cv2.THRESH_BINARY_INV, 25, 16) 
#	return frame, imgThres

def checkCameraAman(framePro,cam_id):
	with open(PATH_data+'ROI_Full'+cam_id, 'rb') as f:
		pts_poly = pickle.load(f)

	for count, poly in enumerate(pts_poly):
		# Hitung pixel tiap slot
		cnt = np.array(poly)
		x,y,w,h = cv2.boundingRect(cnt)
		croped = framePro[y:y+h, x:x+w].copy()
		
		cnt_mask = cnt - cnt.min(axis=0)
		mask = np.zeros(croped.shape[:2], np.uint8)
		cv2.drawContours(mask, [cnt_mask], -1, (255, 255, 255), -1, cv2.LINE_AA)
		
		final_ROI = cv2.bitwise_and(croped, croped, mask=mask)
		#cv2.imshow(f"ROI Extract {count+1}", final_ROI) #====Tampilkan view tiap slot ====#
		space_count = cv2.countNonZero(final_ROI)
		if space_count < 1000:
			return(1)


def checkParkingSpace(frameOri,framePro,cam_id):
	free_space = 0
	with open(PATH_data+'titik_polygon_'+cam_id, 'rb') as f:
		pts_poly = pickle.load(f)

	for count, poly in enumerate(pts_poly):
		
		# Hitung pixel tiap slot
		cnt = np.array(poly)
		x,y,w,h = cv2.boundingRect(cnt)
		croped = framePro[y:y+h, x:x+w].copy()
		
		cnt_mask = cnt - cnt.min(axis=0)
		mask = np.zeros(croped.shape[:2], np.uint8)
		cv2.drawContours(mask, [cnt_mask], -1, (255, 255, 255), -1, cv2.LINE_AA)
		
		final_ROI = cv2.bitwise_and(croped, croped, mask=mask)
		#cv2.imshow(f"ROI Extract {count+1}", final_ROI) #====Tampilkan view tiap slot ====#
		space_count = cv2.countNonZero(final_ROI)

		# Anotasi ROI Polygon & Teksnya 
		index = (count+1) if cam_id == "81" else 7-(count+1)	#==== Indeks tiap slot ====#
		ROI_color, status, ROI_thick = COLOR_RED, "FULL", 1
		if space_count < 150: #==== Threshold pixel slot-FREE ====#
			ROI_color, status, ROI_thick = COLOR_GREEN, "Free", 2
			slot_index[str(index)] = 1
		
		poly_ROI = cnt.reshape((-1,1,2))
		cv2.polylines(frameOri, [poly_ROI], isClosed=True,
					  color=ROI_color, thickness=ROI_thick)
		
		cvzone.putTextRect(frameOri, (f"{index}|{status}"), (int(x+w*0.4),int(y+0.5*h)), scale=1.2,
						   thickness=ROI_thick, offset=5, colorR=ROI_color)
	
	# Tampilkan total free slot
	for slot in slot_index:
		if slot_index[slot] == 1:
			free_space += 1
	if cam_id=='136':
		cvzone.putTextRect(frameOri, f'Free: {free_space}/6', (0,25), scale=2,
                    thickness=2, offset=5, colorR=COLOR_GREEN)			
						   

# ===== MAIN ===== #
if __name__ == '__main__':
	while True:
		# Inisiasi 6 slot 
		slot_index = [str(i+1) for i in range(6)]
		slot_index = dict.fromkeys(slot_index, 0)

		cam_81_mati = 0
		cam_136_mati = 0
		
		## Cam 136 idup saja
		#if cam_136_mati==0 and cam_81_mati==1:
		#	ret, frame_136 = cam_136.read()
		#	cam_136 = cv2.VideoCapture(URL_cam136)
		#	imgGray136 = cv2.cvtColor(frame_136, cv2.COLOR_BGR2GRAY)
		#	imgBlur136 = cv2.GaussianBlur(imgGray136, (3, 3), 1)
		#	imgThresh_136 = cv2.adaptiveThreshold(imgBlur136, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
		#										 cv2.THRESH_BINARY_INV, 25, 16)
		#	
		#	checkCameraAman(imgThresh_136, cam_id="136")
		#	checkParkingSpace(frameOri=frame_136, framePro=imgThresh_136, cam_id="136")
		#	
		#	cv2.imshow("Live CAM-136", frame_136)

		# Monitor slot parkir
		if cam_81.isOpened() and cam_136.isOpened() and cam_136_mati == 0 and cam_81_mati == 0:
			ret, frame_81 = cam_81.read()
			ret, frame_136 = cam_136.read()

			imgGray81 = cv2.cvtColor(frame_81, cv2.COLOR_BGR2GRAY)
			imgBlur81 = cv2.GaussianBlur(imgGray81, (3, 3), 1)
			imgThresh_81 = cv2.adaptiveThreshold(imgBlur81, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
												 cv2.THRESH_BINARY_INV, 25, 16) 

			imgGray136 = cv2.cvtColor(frame_136, cv2.COLOR_BGR2GRAY)
			imgBlur136 = cv2.GaussianBlur(imgGray136, (3, 3), 1)
			imgThresh_136 = cv2.adaptiveThreshold(imgBlur136, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
												 cv2.THRESH_BINARY_INV, 25, 16)
			
			cam_81_mati= checkCameraAman(imgThresh_81, cam_id="81")
			cam_136_mati = checkCameraAman(imgThresh_136, cam_id="136")

			if cam_81_mati == 1 or cam_136_mati == 1:
				cv2.destroyAllWindows()
				continue

			checkParkingSpace(frameOri=frame_81, framePro=imgThresh_81, cam_id="81")
			checkParkingSpace(frameOri=frame_136, framePro=imgThresh_136,  cam_id="136")

			cv2.imshow("Live CAM-81", frame_81)
			cv2.imshow("Live CAM-136", frame_136)
			cv2.imshow("Live Tresh CAM-81", imgThresh_81)
			cv2.imshow("Live Tresh CAM-136", imgThresh_136)

		key = cv2.waitKey(10)
		if key == 27:
			break
		elif key == ord('p'):
			cv2.waitKey(0)
		## Tampilkan slot free-full 	
		#print(slot_index)
		#for index in slot_index:
		#	status_slot = "Free" if slot_index[index] == 1 else "FULL"
		#	print(f"Slot {index}: {status_slot}")

	cv2.destroyAllWindows()
	cam_81.release()
	cam_136.release()