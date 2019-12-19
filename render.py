import cv2
import os
from PIL import Image

def render(im):
  lines = []
  for x in range(7):
    pixels = []
    for y in range(15):
      pixels.append(im.getpixel((x,y))[0])
    lines.append(",".join(map(str, pixels)))
  return '{' + ",\n".join(lines) + '}'

vidcap = cv2.VideoCapture("cap.mp4")
length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
vidcap.set(1, (length / 2) + 800)
area = (823, 93, 1107, 609)

success,image = vidcap.read()
count = 0
success = True
frames = []
while success and count < 1000:
  fname = "frame%d.bmp" % count
  cv2.imwrite(fname, image)
  im = Image.open(fname).crop(area).convert('LA').resize((7, 15))
  frames.append(render(im))
  os.remove(fname)
  success, image = vidcap.read()
  count += 1

with open("output.txt", "w") as f:
  f.write('{' + ",\n".join(frames) + '}')
