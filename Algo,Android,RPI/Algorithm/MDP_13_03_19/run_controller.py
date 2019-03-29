import argparse

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
    controller = Controller()

    # Keep main thread alive to keep daemons alive
    while True:
        pass
