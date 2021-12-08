#!/bin/env python3
"""
Video capture test program.

Press 'q' to exit, 'r' to record (start|stop)
"""

import sys
import argparse
import math
import cv2


def add_label(frame, label, row=1):
    """
    Adds a label to image
    """
    cv2.putText(frame, label,
            (0, row*25),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0, (100, 0, 0),
            thickness=2, lineType=cv2.LINE_AA)


def add_frame(frame, f_w, f_h, margin=50, color=(100, 0, 0)):
    """
    Adds a frame to image
    """
    cv2.rectangle(frame, (margin, margin), (f_w-margin, f_h-margin), color, 1)

def detect_faces(frame, face_cascade):
    """
    Detects faces on image

    Detects faces, wite a frame around them and return the number of detected faces.
    @see https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81
    """
    faces = face_cascade.detectMultiScale(frame, 1.1, 4)
    for face in faces:
        (fcx, fcy, fcw, fch) = face
        cv2.rectangle(frame, (fcx, fcy), (fcx+fcw, fcy+fch), (255, 0, 0), 2)
    return len(faces)

def main(args):
    """
    The file main function
    """
    vid_capture = cv2.VideoCapture(args.camera)
    if not vid_capture.isOpened():
        print("Error opening video")
        sys.exit(1)

    rate = vid_capture.get(cv2.CAP_PROP_FPS)
    f_w = int(vid_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    f_h = int(vid_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    vid_writer = cv2.VideoWriter(
        args.output,
        cv2.VideoWriter_fourcc(*'MJPG'),
        rate, (f_w, f_h)
    )

    is_recording = False

    interval = 1000 / rate

    print("Frame size:", f_w, 'x', f_h)
    print("Frame rate:", rate, 'fps')
    print("Frame interval:", math.floor(interval), 'ms')

    cur = 0
    while vid_capture.isOpened():
        #ret, frame = vid_capture.read()
        ret = vid_capture.grab()
        ret, frame = vid_capture.retrieve()
        if not ret:
            break

        n_faces = detect_faces(frame, face_cascade)
        add_label(frame, f"{f_w} x {f_h} {rate} fps")
        add_label(frame, f"cur: {cur} faces: {n_faces}", row=2)
        add_frame(frame, f_w, f_h, 60)

        if is_recording:
            vid_writer.write(frame)
        cur += 1
        cv2.imshow('Frame', frame)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
        if k == ord('r'):
            is_recording = not is_recording
            print('Recording:', is_recording, '[', args.output, ']')

    vid_capture.release()
    vid_writer.release()


parser = argparse.ArgumentParser(
    description="Video capture test program. Press 'q' to exit, 'r' to record (start|stop)")
parser.add_argument('--camera', '-c',
                    help='Camera divide number',
                    type=int, default=0)
parser.add_argument('--output', '-o',
                    help='File to save recording to',
                    metavar='FILE',
                    type=str, default="/tmp/recording.avi")

g_args = parser.parse_args()

if __name__ == '__main__':
    main(g_args)
