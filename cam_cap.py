import cv2
import time, tempfile

def cam_cap():
	try:
		img_path = '{}\\cam_{}.jpg'.format(tempfile.gettempdir(),time.strftime('%Y%m%d_%H%M%S'))
		cam = cv2.VideoCapture(0)
		ret, frame = cam.read()
		cv2.imwrite(img_path, frame)
		result = img_path
	except Exception as e:
		result = e
	finally:
		cam.release()
		print("Cam Released")
		return result



if __name__ == '__main__':
	print(cam_cap())
