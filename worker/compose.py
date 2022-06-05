import glob
from PIL import Image
import sys
import extract


def to_gif(fps, fp_out):
    # filepaths
    frames = "/images/frame*.png"

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif

    imgs = (Image.open(f) for f in sorted(glob.glob(frames)))
    img = next(imgs)  # extract first image from iterator
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=1 / fps, loop=0)


if __name__ == '__main__':
    fps = sys.argv[1]
    # TODO: parse fps from extracted frame (previous job)
    fp_out = sys.argv[2]
    fps = get_frames(fp_in)
    to_gif(fps, fp_out)
