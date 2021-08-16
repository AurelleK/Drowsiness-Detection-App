# Drowsiness-Detection-App
I provided here a whole of code for drowsiness detection application using MSQL data Based to store any drowsiness activity and a Dashboard to display and search all drowsiness activity 
# this code is developped by Aurelle Tchagna with the help of InchTech's team (inchtechs.com)
we use Raspberry PI 4 with Pi Camera to train and perform our project.
SIM808 GPS, GPRS and GPS to get the position and speed of the Car and to send a message containing all this information.
a buzzer and led is used for indication.
before use the code, you should have a raspberry Pi4 with Pi camera or any USB or IP Cam
download and put in the same folder shape-predictor shape_predictor_68_face_landmarks
install OpenCV, DLIB and other requiment librairies
install Maria DB with a Maria DB client for Python Language

in this project, when a driver drowse, we capture automatically his position and car speed and save it into the Maria DB automatically with the corresponding date.
a SMS is sended automatically to an appropriate personne that we configure the system with his number

To run the code, type `python3 Drowsiness_MainCode.py` in your Raspberry Pi Terminal
