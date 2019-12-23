import cv2
import os
import time
from PIL import Image, ImageChops, ImageFilter


def render(im, fnum):
    lines = []
    luminosity = 0
    for x in range(7):
        pixels = []
        for y in range(15):
            pixel = im.getpixel((x, y))[0]
            luminosity += pixel
            pixels.append(pixel)
        lines.append(",".join(map(str, pixels)))
    if luminosity < 1000:
        print(f"Skipping frame {fnum}, luminosity too low")
        return None
    return '{' + ",\n".join(lines) + '}'


vidcap = cv2.VideoCapture("cap.mp4")
skip_first_seconds = 20
area = (823, 93, 1107, 609)

success, image = vidcap.read()
count = 0
success = True
frames = []
frame_count = 10000
start_time = time.time()
fps = 30
minutes = (frame_count // fps) // 60
seconds = (frame_count // fps) % 60
print(f"Rendering ~{minutes:02}:{seconds:02} of video")

if skip_first_seconds:
    vidcap.set(1, skip_first_seconds * fps)

while success and count < frame_count:
    fname = "frame%d.bmp" % count
    cv2.imwrite(fname, image)
    im = Image.open(fname).crop(area).convert('LA').resize((7, 15))
    rendered = render(im, count)
    if rendered:
        frames.append(rendered)
    os.remove(fname)
    success, image = vidcap.read()
    count += 1
    percentage_complete = int(100 * count / frame_count)
    prog = int(percentage_complete / 5)
    time_elapsed = (time.time() - start_time) * 1000
    frames_per_second = count / time_elapsed
    seconds_to_go = int((frame_count - count) * frames_per_second)
    minutes_to_go = seconds_to_go // 60
    seconds_to_go = seconds_to_go % 60
    time_str = f"{minutes_to_go:02}:{seconds_to_go:02}"
    print(" {}% [{}] {}/{} [ETA: {}]".format(
        percentage_complete,
        '=' * prog + '>' + ' ' * (20 - prog),
        count,
        frame_count,
        time_str,
    ), end="\r")
print("Written output to output.txt")


with open("output.txt", "w") as f:
    f.write('{' + ",\n".join(frames) + '}')
