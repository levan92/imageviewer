import os
import cv2
import argparse
from pathlib import Path

IMG_EXTS = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']
IMG_EXTS = [e.lower() for e in IMG_EXTS]
print('Looking for images with extensions: ', IMG_EXTS)
IMG_EXTS.extend([e.upper() for e in IMG_EXTS])

parser = argparse.ArgumentParser()
parser.add_argument('images_dir', help='path to directory of images')
parser.add_argument('--sort-time', help='sort images by time instead of name', action='store_true')
args = parser.parse_args()

images_dir = Path(args.images_dir)
assert images_dir.is_dir()

image_paths = [ip for ip in images_dir.rglob('*') if ip.suffix in IMG_EXTS]
if args.sort_time:
    sortkey = os.path.getmtime
    print('Sorting from earlier to latest..')
else:
    sortkey = lambda x: str(x).lower()
    print('Sorting alphabetically..')
image_paths.sort(key=sortkey)

num_images = len(image_paths)
print('Total number of images found: {}'.format(num_images))

ff10 = int(round(0.1 * num_images))

win_name = '{}'.format(images_dir.name)
# win_name = '({}/{}) {}'.format(i+1, num_images, imgpath.name)
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

i = 0
def trackbar_callback(value):
    pass

trackbar_name = ''
cv2.createTrackbar(trackbar_name, win_name, 1, num_images, trackbar_callback)

print('`f` for forward and `d` to move back.')
print('`g` to fast forward and `s` to fast back.')
print('`enter` or `spacebar` to print filename.')
print('`q` or `Esc` to quit.')

# for imgpath in image_paths:
while True:
    i_plus_1 = cv2.getTrackbarPos(trackbar_name, win_name)
    i = i_plus_1 - 1
    imgpath = image_paths[i]
    img = cv2.imread(str(imgpath))
    cv2.imshow(win_name, img)
    new_i = i
    key = cv2.waitKey(5) & 0xff
    if key == ord('q') or key == 27: #esc
        break
    elif key == ord('f') or key == 83: #right
        new_i = i + 1
    elif key == ord('g'):
        new_i = i + ff10
    elif key == ord('d') or key == 81: #left
        new_i = i - 1
    elif key == ord('s'):
        new_i = i - ff10
    elif key == 10 or key == 32: #enter
        print('Image filename: {}'.format(imgpath.name))
    if new_i < 0:
        new_i = 0
    elif new_i >= num_images:
        new_i = num_images - 1

    if new_i != i:
        cv2.setTrackbarPos(trackbar_name, win_name, new_i+1)