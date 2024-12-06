#!/usr/bin/env python3

import sys
import time
import subprocess
import os

CLOCK_SPEED = 1  # Set to 0.001 for testing

# Color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'

# Initialize colorama on Windows for colored output
try:
    import colorama
    colorama.init()
except ImportError:
    if sys.platform.startswith('win'):
        print("For colored output on Windows, please install the 'colorama' module.")
        print("You can install it by running 'pip install colorama'.")

WORK_TIME = 25
BREAK_TIME = 5
ROUNDS = 4

def play_sound(sound_type):
    """
    Plays a sound depending on the sound_type.
    """
    if sys.platform.startswith('win'):
        try:
            import winsound
            if sound_type == 'work':
                frequency = 1000  # Hz
            elif sound_type == 'break':
                frequency = 600  # Hz
            elif sound_type == 'final_break':
                frequency = 800  # Hz
            duration = 500  # milliseconds
            winsound.Beep(frequency, duration)
        except ImportError:
            print("winsound module not available.")
    elif sys.platform.startswith('darwin'):
        # macOS
        if sound_type == 'work':
            os.system('say "Work time started"')
        elif sound_type == 'break':
            os.system('say "Break time started"')
        elif sound_type == 'final_break':
            os.system('say "Final break time started"')
    else:
        # For other platforms, attempt to print a bell character
        print('\a')

def progress_bar(msg, time_sec, color):
    print(f"{color}{msg} for {time_sec // 60} min{RESET}")
    try:
        for i in range(1, time_sec + 1):
            perc = i * 100 // time_sec
            candle = "█" * (perc // 2) + "-" * (50 - (perc // 2))
            print(f'\r{color}{candle} {perc}%{RESET}', end='', flush=True)
            time.sleep(CLOCK_SPEED)
        print("\n")
    except KeyboardInterrupt:
        # In case you stop the code from the execution.
        sys.exit(1)

def calculate_final_break(work_time, break_time, rounds):
    """
    Calculates the final break time in seconds based on the given work time, break time, and number of rounds.

    Args:
        work_time (int): The duration of each work interval in minutes.
        break_time (int): The duration of each regular break in minutes.
        rounds (int): The total number of completed pomodoro intervals (work round + break) so far.

    Returns:
        int: The calculated final break time in seconds.

    Comment:
    This function by default sets a default final break time of 30 minutes, assuming each work interval is 25 minutes and each regular break is 5 minutes for 4 completed rounds.

    Please note that this function will be further modified in the future with a statistical model to consider work, break, round, and human fatigue factors for more accurate final break time calculations.
    """
    final_break_time = 30  # mins
    final_break = final_break_time * 60  # seconds
    return final_break

def pomodoro(*args, **kwargs):
    default_values = {'-w': WORK_TIME, '-b': BREAK_TIME, '-r': ROUNDS}
    work_time = kwargs.get('-w', default_values['-w'])
    break_time = kwargs.get('-b', default_values['-b'])
    rounds = kwargs.get('-r', default_values['-r'])

    total_sessions = [work_time, break_time] * rounds
    total_min = sum(total_sessions)
    try:
        for work_or_break, session in enumerate(total_sessions):
            if work_or_break % 2 == 0:
                round_num = work_or_break // 2 + 1
                print(f"{BLUE}Round: {round_num}{RESET}")

            if work_or_break % 2 == 0:
                msg = "Work Time"
                time_seconds = session * 60
                color = GREEN
                sound_type = 'work'
                play_sound(sound_type)
                progress_bar(msg, time_seconds, color)
            elif work_or_break == len(total_sessions) - 1:
                msg = "Final Break"
                final_break = calculate_final_break(work_time, break_time, rounds)
                color = CYAN
                sound_type = 'final_break'
                play_sound(sound_type)
                progress_bar(msg, final_break, color)
            else:
                msg = "Break Time"
                time_seconds = session * 60
                color = YELLOW
                sound_type = 'break'
                play_sound(sound_type)
                progress_bar(msg, time_seconds, color)
    finally:
        print(f"{MAGENTA}End!{RESET}")

def help():
    print("""
        Pomodoro Timer Help
        -------------------
        Usage:
        $ termato [OPTIONS]

        Options:
        -w=<work_time>  Set the duration of each work interval in minutes. Default: 25 minutes.
        -b=<break_time> Set the duration of each regular break in minutes. Default: 5 minutes.
        -r=<rounds>     Set the total number of completed pomodoro intervals (work round + break). Default: 4.
        -h              Display this help message.

        Example:
        $ termato -w=30 -b=10 -r=3
        This will start a pomodoro timer with work interval of 30 minutes, break of 10 minutes, and 3 completed rounds.
        
        Default values are : -w=25 -b=5 -r=4

        Note:
        The script will use default values if any option is not provided.
        Only -w, -b, -r options are recognized. All other parameters will be ignored.
        Press Ctrl+C during the timer to stop the script.
        """)


def run_pomo():
    if len(sys.argv) <= 1:
        pomodoro()
    elif '-h' in sys.argv:
        help()
        sys.exit(0)
    else:
        args_dict = {}
        valid_args = {'-b', '-r', '-w'}
        for arg in sys.argv[1:]:
            if '=' in arg:
                key, value = arg.split("=")
                if key in valid_args:
                    args_dict[key] = int(value)
                else:
                    print(f"We have ignored your arg: {key}\nFor help please try -h.\n")
            else:
                print(f"Invalid argument format: {arg}\nFor help please try -h.\n")
        pomodoro(**args_dict)

if __name__ == "__main__":
    run_pomo()
