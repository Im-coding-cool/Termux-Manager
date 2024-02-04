import curses

def main(stdscr):
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    stdscr.clear()
    stdscr.addstr("Click anywhere to get the coordinates\n")
    stdscr.refresh()
    while True:
        c = stdscr.getch()
        if c == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            stdscr.addstr("Mouse click at ({}, {})\n".format(x, y))
            stdscr.refresh()

curses.wrapper(main)
