#!/usr/bin/env python3
import glob

import cv2
import sys

from PIL import Image


def get_frames(fp_in):
    vidcap = cv2.VideoCapture(fp_in)

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(length)

    success, image = vidcap.read()
    count = 0
    while success:
        if 1 / 3 * length < count < 1 / 3 * length + fps * 15:
            cv2.imwrite("/images/frame%d.png" % count, image)
        success, image = vidcap.read()
        count += 1
    return fps


def to_gif(fps, fp_out):
    # filepaths
    frames = "/images/frame*.png"

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif

    imgs = (Image.open(f) for f in sorted(glob.glob(frames)))
    img = next(imgs)  # extract first image from iterator
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=1 / fps, loop=0)


if __name__ == '__main__':
    fp_in = sys.argv[1]
    fp_out = sys.argv[2]
    fps = get_frames(fp_in)
    to_gif(fps, fp_out)
