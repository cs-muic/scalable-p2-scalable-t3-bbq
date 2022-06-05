import cv2
import imutils
import sys


def get_frames(fp_in):
    vidcap = cv2.VideoCapture(fp_in)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    success, image = vidcap.read()
    count = 0
    while success:
        if 1 / 3 * length < count < 1 / 3 * length + fps * 15:
            frame = imutils.resize(image, width=480)
            cv2.imwrite("/images/frame%d.png" % count, frame)
        success, image = vidcap.read()
        count += 1
    return fps


if __name__ == '__main__':
    fp_in = sys.argv[1]
