import glob
import cv2
import os

from PIL import Image


def get_frames():
    vidcap = cv2.VideoCapture('./assets/test3.mp4')

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(length)

    success, image = vidcap.read()
    count = 0
    while success:
        if 1/3*length < count < 1/3*length+fps*15:
            cv2.imwrite("./assets/images/frame%d.png" % count, image)
        success, image = vidcap.read()
        count += 1
    return fps


def to_gif(fps):
    # filepaths


    fp_in = "./assets/images/frame*.png"
    fp_out = "./assets/out/image.gif"

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif

    imgs = (Image.open(f) for f in sorted(glob.glob(fp_in)))
    img = next(imgs)  # extract first image from iterator
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=1/fps, loop=0)


if __name__ == '__main__':
    fps = get_frames()
    to_gif(fps)
