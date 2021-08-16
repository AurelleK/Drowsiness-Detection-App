# InchTechs Project Drowsiness detection with Raspberry Pi and Pi Camera and SIM808
# August 2021 www.inchtechs.com
from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
#import module GSM GPS
import smsGPS as sm
from goto import with_goto
#@with_goto
# Initialisation des GPIO
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW) # Buzzer
GPIO.setup(29, GPIO.OUT, initial=GPIO.LOW) # Led Rouge
GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW) # Led Bleu

# Somnolence Part
def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear
	
thresh = 0.25
frame_check = 10
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
cap=cv2.VideoCapture(0)
flag=0
while True:
	ret, frame=cap.read()
	frame = imutils.resize(frame, width=900)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	subjects = detect(gray, 0)
	for subject in subjects:
		shape = predict(gray, subject)
		shape = face_utils.shape_to_np(shape)#converting to NumPy Array
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
		ear = (leftEAR + rightEAR) / 2.0
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
		#label .begin
		if ear < thresh:
			flag += 1
			print (flag)
			GPIO.output(32, GPIO.HIGH) # Turn on
			GPIO.output(29, GPIO.LOW) # Turn off led red
			GPIO.output(40, GPIO.LOW) # Turn off buzzer
			if flag >= frame_check:
				cv2.putText(frame, "***SOMNOLENCE**ALERTE!** SOMNOLENCE***", (10, 30),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				cv2.putText(frame, "***SOMNOLENCE**ALERTE!** SOMNOLENCE***", (10,675),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				#print ("Drowsy")
				GPIO.output(32, GPIO.LOW) # Turn off
				GPIO.output(29, GPIO.HIGH) # Turn on led red
				GPIO.output(40, GPIO.HIGH) # Turn on buzzer
				sm.gpsCoordSMS()
				sm.sendSms1()
				GPIO.output(40, GPIO.LOW) # Turn on buzzer
				frame_check=0
				#goto .begin
				

		else:
			flag = 0
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
cv2.destroyAllWindows()
cap.release() 

