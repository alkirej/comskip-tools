import argparse as ap
import logging as log
import os
import sys

import lib

BLACK_FRAME_LINE_TEST: str = "Black frame with brightness of "
VOLUME_TEST: str = "and volume of "
UNIFORM_TEST: str = "uniform of "
BLOCK_LIST_TEST: str = "Block list after weighing"
BLOCK_LIST_SEPARATOR_TEST: str = "----------"

MIN_ALLOWED_VOLUME: int = 250
MAX_ALLOWED_VOLUME: int = 1000

MIN_ALLOWED_NON_UNIFORMITY: int = 250
MAX_ALLOWED_NON_UNIFORMITY: int = 2000


def comskip_block_list(log_info: [str]) -> None:
    at_list_header: bool = False
    at_list_separator: bool = False
    processing_list: bool = False

    # FIND THE START OF THE BLOCK LIST
    for line in log_info:
        if processing_list:
            pass

        elif at_list_separator:
            pass

        elif at_list_header:
            # Next line must be the separator
            if BLOCK_LIST_SEPARATOR_TEST in line:
                at_list_header = False
                at_list_separator = True


def find_uniform(black_frames: [str]) -> [int]:
    answer_coll: [int] = []
    for fr in black_frames:
        uniform_loc: int = fr.find(UNIFORM_TEST) + len(UNIFORM_TEST)
        uniform_level: int = lib.get_number_at(fr, uniform_loc)
        if uniform_level >= 50:
            answer_coll.append(uniform_level)
    answer_coll.sort()
    return answer_coll


def choose_not_uniform_value(black_frames: [int]) -> int:
    vols: [int] = find_uniform(black_frames)
    total_items: int = len(vols)
    last: int = MAX_ALLOWED_NON_UNIFORMITY

    count: int = 0
    for vol in vols:
        count += 1
        last = vol
        if count > total_items / 2:
            break

    if last > MAX_ALLOWED_NON_UNIFORMITY:
        last = MAX_ALLOWED_NON_UNIFORMITY
    elif last < MIN_ALLOWED_NON_UNIFORMITY:
        last = MIN_ALLOWED_NON_UNIFORMITY

    return last


def find_volumes(black_frames: [str]) -> [int]:
    answer_coll: [int] = []
    for fr in black_frames:
        volume_loc: int = fr.find(VOLUME_TEST) + len(VOLUME_TEST)
        volume_level: int = lib.get_number_at(fr, volume_loc)
        if volume_level >= 0:
            answer_coll.append(volume_level)
    answer_coll.sort()
    return answer_coll


def choose_max_volume(black_frames: [int]) -> int:
    vols: [int] = find_volumes(black_frames)
    total_items: int = len(vols)
    last: int = MAX_ALLOWED_VOLUME

    count: int = 0
    for vol in vols:
        count += 1
        last = vol
        if count > total_items / 2:
            break

    if last < MIN_ALLOWED_VOLUME:
        last = MIN_ALLOWED_VOLUME
    elif last > MAX_ALLOWED_VOLUME:
        last = MAX_ALLOWED_VOLUME

    return last


def load_log_file(filename: str) -> [str]:
    return open(filename, "r").read().splitlines()


def keep_only_black_frames(all_lines: [str]) -> [str]:
    black_frame_lines: [str] = []
    for line in all_lines:
        if BLACK_FRAME_LINE_TEST in line:
            black_frame_lines.append(line)
    return black_frame_lines


def get_black_frame_brightnesses(black_frame_lines: [str]) -> [int]:
    brightnesses: [int] = []
    for line in black_frame_lines:
        brightness_loc: int = line.find(BLACK_FRAME_LINE_TEST) + len(BLACK_FRAME_LINE_TEST)
        brightness_str: str = line[brightness_loc:brightness_loc+2]
        brightness: int = int(brightness_str)
        brightnesses.append(brightness)

    return brightnesses


def count_by_brightness(brightnesses: [int]) -> dict[int, int]:
    brightness_counts: dict[int, int] = {}
    for val in brightnesses:
        try:
            brightness_counts[val] += 1
        except KeyError:
            brightness_counts[val] = 1

    return brightness_counts


def file_name_check(file_name: str) -> str:
    if os.path.isfile(file_name):
        return file_name
    else:
        log.error(f"{file_name} is not a readable file.")
        print(f"{file_name} is not a readable file.")
        sys.exit(1)


def read_black_frames(filename: str) -> [str]:
    all_lines: [str] = load_log_file(filename)
    bf_lines: [str] = keep_only_black_frames(all_lines)
    return bf_lines


def comskip_logfile_to_blackframe_brightness_counts(black_frames: [str]) -> dict[int, int]:
    bf_brightness: [int] = get_black_frame_brightnesses(black_frames)
    brightness_counts: dict[int, int] = count_by_brightness(bf_brightness)
    return brightness_counts


def determine_max_avg_brightness(brightness_counts: dict[int, int]) -> int:
    if len(brightness_counts) == 0:
        return 20

    best_answer: int | None = None

    for k in brightness_counts:
        if brightness_counts[k] > 3:
            if best_answer is None:
                best_answer = k
            else:
                best_answer = min(k, best_answer)

    if best_answer is None:
        idx: int = min(brightness_counts.keys())
        best_answer = brightness_counts[idx]

    return best_answer


def blackframe_maxavg_brightness_from_logfile(filename: str) -> int:
    counts: dict[int, int] = comskip_logfile_to_blackframe_brightness_counts(filename)
    answer: int = determine_max_avg_brightness(counts)
    return answer


def main():
    log.info(f"black-frame-info start")
    log.info(f"Command Line Params: {' '.join(sys.argv)}")
    parser: ap.ArgumentParser = ap.ArgumentParser(
                    prog="black-frame-info",
                    description="Read comskip log file and print relevant info on screen."
                    )
    parser.add_argument("comskip_logfile",
                        type=file_name_check,
                        help="Location of log file output of a comskip run."
                        )
    parser.add_argument("--update-ini",
                        type=file_name_check,
                        help="update this file to include the suggested "
                              + "comskip parameters by this utility."
                        )
    try:
        args: ap.Namespace = parser.parse_args()
    except Exception as e:
        print(e)
        print(type(e))
        sys.exit(1)

    black_frames: [str] = read_black_frames(args.comskip_logfile)
    max_avg_bright: int = blackframe_maxavg_brightness_from_logfile(black_frames)
    not_uniform: int = choose_not_uniform_value(black_frames)
    max_vol: int = choose_max_volume(black_frames)

    print(f"BLACK FRAME DETECTION SETTINGS TO USE:")
    print(f"    max_avg_brightness={max_avg_bright+5}")
    print(f"    test_brightness={max_avg_bright+25}")
    print(f"    max_brightness={max_avg_bright+45}")
    print(f"    non_uniformity={not_uniform}")
    print(f"    max_volume={max_vol}")

    if args.update_ini != "":
        print()
        print("********************************************")
        print(f"UPDATE {args.update_ini}")
        print("********************************************")
        lib.set_black_frame_vals_in_ini(
                args.update_ini,
                max_avg_bright,
                not_uniform,
                max_vol
        )


if "__main__" == __name__:
    # SETUP LOGGER BEFORE IMPORTS SO THEY CAN USE THESE SETTINGS
    log.basicConfig(filename="comskip-tools.log",
                    filemode="a",
                    format="%(asctime)s %(filename)15.15s %(funcName)15.15s %(levelname)5.5s %(lineno)4.4s %(message)s",
                    datefmt="%Y%m%d-%H:%M:%S"
                    )
    log.getLogger().setLevel(log.DEBUG)

    main()
