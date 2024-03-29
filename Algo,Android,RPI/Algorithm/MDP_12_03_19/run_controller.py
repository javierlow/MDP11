import argparse

import tkinter as tk
# import GUI
import GUI_real_time
from controller_with_sim import SimController
from controller import Controller
import utils as u

if __name__ == '__main__':

    # Handle CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug-mode', action='store_true',
                        help='enable console printout at the cost of a slower run')
    parser.add_argument('-l', '--localhost', action='store_true',
                        help='connect to localhost for debugging')
    parser.add_argument('-a', '--arrow-scan', action='store_true',
                        help='scan for arrows during exploration')
    parser.add_argument('-s', '--simulation', action='store_true',
                        help='real run with simulator')
    args = parser.parse_args()

    keys = list(vars(args).keys())

    for key in keys:
        print('%s=%s' % (key.upper(), str(vars(args)[key]).upper()))
    print()

    if args.localhost:
        u.HOST = '127.0.0.1'

    u.ARROW_SCAN = args.arrow_scan

    u.DEBUG_MODE = args.debug_mode
    u.disable_print()

    # Initialize Controller
    if args.simulation:
        _root = tk.Tk()
        _gui = GUI_real_time.Window(_root)
        _gui.mainloop()
    else:
        controller = Controller()

    # Keep main thread alive to keep daemons alive
    while True:
        pass
