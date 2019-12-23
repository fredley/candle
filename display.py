import curses
import json
import time


def main(stdscr):
    # Clear screen
    stdscr.nodelay(True)
    stdscr.clear()
    curses.start_color()
    curses.use_default_colors()
    color_converter = lambda x: int((x * 1000) / 256)
    for i in range(1, curses.COLORS):
        curses.init_color(i, color_converter(i), color_converter(i), 0)
        curses.init_pair(i, i, -1)

    with open("output.txt") as f:
        frames = json.loads(f.read().replace("{", "[").replace("}", "]"))

    done = False
    while not done:
        for fnum, frame in enumerate(frames):
            for i, letter in enumerate(frame):
                y = i % 15
                x = i // 15
                stdscr.addstr(
                    y, x, '█' if letter > 0 else ' ', curses.color_pair(letter)
                )
            stdscr.addstr(16, 0, 'Frame {} of {}'.format(fnum, len(frames)))
            time.sleep(0.002)
            stdscr.refresh()
            try:
                key = stdscr.getkey()
                stdscr.clear()
                stdscr.addstr("Detected key:")
                stdscr.addstr(str(key))
                curses.use_default_colors()
                stdscr.refresh()
                done = True
                break
            except Exception:
                # No input
                pass


curses.wrapper(main)
