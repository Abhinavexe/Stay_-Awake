{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "from scipy.spatial import distance\n",
    "from imutils import face_utils\n",
    "from pygame import mixer\n",
    "import imutils\n",
    "import dlib\n",
    "import cv2\n",
    "import time"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "def eye_aspect_ratio(eye):\n",
    "\tA = distance.euclidean(eye[1], eye[5])\n",
    "\tB = distance.euclidean(eye[2], eye[4])\n",
    "\tC = distance.euclidean(eye[0], eye[3])\n",
    "\tear = (A + B) / (2.0 * C)\n",
    "\treturn ear"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "mixer.init()\n",
    "sound = mixer.Sound('alarm.wav')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [],
   "source": [
    "thresh = 0.25\n",
    "frame_check = 20\n",
    "detect = dlib.get_frontal_face_detector()\n",
    "predict = dlib.shape_predictor(\"shape_predictor_68_face_landmarks.dat\")# Dat file is the crux of the code"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {},
   "outputs": [],
   "source": [
    "(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS[\"left_eye\"]\n",
    "(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS[\"right_eye\"]\n",
    "cap=cv2.VideoCapture(0)\n",
    "cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)\n",
    "cap.set(3,1000)\n",
    "cap.set(4,1000)\n",
    "cap.set(10,60)\n",
    "flag=0"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {},
   "outputs": [],
   "source": [
    "while True:\n",
    "    \n",
    "    ret, frame=cap.read()\n",
    "   \n",
    "    frame = imutils.resize(frame, width=1000)\n",
    "   \n",
    "    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)\n",
    "    sub = detect(gray, 0)\n",
    "    for subject in sub:\n",
    "        \n",
    "        shape = predict(gray, subject)\n",
    "        shape = face_utils.shape_to_np(shape)#converting to NumPy Array\n",
    "        leftEye = shape[lStart:lEnd]\n",
    "        rightEye = shape[rStart:rEnd]\n",
    "        leftEAR = eye_aspect_ratio(leftEye)\n",
    "        rightEAR = eye_aspect_ratio(rightEye)\n",
    "        ear = (leftEAR + rightEAR) / 2.0\n",
    "        leftEyeHull = cv2.convexHull(leftEye)\n",
    "        rightEyeHull = cv2.convexHull(rightEye)\n",
    "        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)\n",
    "        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)\n",
    "        if ear < thresh:\n",
    "            flag += 1\n",
    "            if flag >= frame_check:\n",
    "                cv2.putText(frame, \"****************ALERT!****************\", (10, 30),\n",
    "                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)\n",
    "                sound.play()\n",
    "                time.sleep(1)\n",
    "                sound.stop()\n",
    "                cv2.putText(frame, \"****************ALERT!****************\", (10,325),\n",
    "                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)\n",
    "        else:\n",
    "            sound.stop()\n",
    "            flag = 0\n",
    "    cv2.imshow(\"Frame\", frame)\n",
    "    key = cv2.waitKey(1) & 0xFF\n",
    "    if key == ord(\"q\"):\n",
    "        cv2.destroyAllWindows()\n",
    "        cap.release()\n",
    "        break"
   ]
  },
  {
   "cell_type": "code",
   "execution_count":null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
