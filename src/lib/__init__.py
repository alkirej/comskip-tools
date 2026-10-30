import logging as log
import os
import sys

# INI FILE: setting names
INI_MAX_AVG_BRIGHT = "max_avg_brightness"
INI_TEST_BRIGHT = "test_brightness"
INI_MAX_BRIGHT = "max_brightness"

INI_NON_UNIFORMITY = "non_uniformity"
INI_MAX_VOLUME = "max_volume"


def get_number_at(text: str, idx: int) -> int:
    best_answer: int = 0
    if len(text) == 0:
        return 0
    # handle negative number a little different from positive ones.
    first_char: str = text[idx]

    negative: bool = first_char == "-"
    if not negative:
        current_idx: int = idx
    else:
        current_idx: int = idx + 1

    next_char: str = text[current_idx]

    while next_char.isnumeric():
        best_answer = (best_answer * 10) + int(next_char)
        current_idx += 1
        try:
            next_char = text[current_idx]
        except IndexError:
            # end of string reached. No worries - exit loop
            break

    if negative:
        best_answer *= -1
    return best_answer


def set_black_frame_vals_in_ini(
        file_name: [str],
        max_avg_brightness: int,
        non_uniformity: int,
        max_volume: int
) -> None:
    # read ini file into memory
    with open(file_name, "r") as edl_file:
        lines: [str] = edl_file.readlines()

    # overwrite ini file with new values
    with open(file_name, "w") as ini_file:
        to_write: str
        for line in lines:
            if line.startswith(f"{INI_MAX_AVG_BRIGHT}="):
                to_write = f"{INI_MAX_AVG_BRIGHT}={max_avg_brightness+5}\n"
            elif line.startswith(f"{INI_TEST_BRIGHT}="):
                to_write = f"{INI_TEST_BRIGHT}={max_avg_brightness+25}\n"
            elif line.startswith(f"{INI_MAX_BRIGHT}="):
                to_write = f"{INI_MAX_BRIGHT}={max_avg_brightness+45}\n"
            elif line.startswith(f"{INI_NON_UNIFORMITY}="):
                to_write = f"{INI_NON_UNIFORMITY}={non_uniformity}\n"
            elif line.startswith(f"{INI_MAX_VOLUME}="):
                to_write = f"{INI_MAX_VOLUME}={max_volume}\n"
            else:
                to_write = line

            ini_file.write(to_write)


def file_name_check(file_name: str) -> str:
    if os.path.isfile(file_name):
        return file_name
    else:
        log.error(f"{file_name} is not a readable file.")
        print(f"{file_name} is not a readable file.")
        sys.exit(1)


def seconds_check(seconds_val: str) -> float:
    try:
        return float(seconds_val)
    except ValueError:
        print(f"{seconds_val} is not a valid input for # of seconds.")
        sys.exit(1)