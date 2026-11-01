import os
import pathlib
import sys


def dir_exist_check(name: str) -> str:
    if os.path.isdir(name):
        return name
    else:
        print(f"Unable to find a directory named {name}")
        sys.exit(1)


def main() -> int:
    args: str = " ".join(sys.argv[1:])
    dir_exist_check(args)

    full_path: pathlib.Path = pathlib.Path(args)
    # work_dir: pathlib.Path = full_path.parent

    try:
        paren_loc: int = full_path.name.index("(")
    except ValueError:
        paren_loc = 15
    last_char_in_name: int = min(15, paren_loc)

    show_dir_name: str = full_path.name[:last_char_in_name]
    file_name: str = f"comskip-{show_dir_name.lower().replace(" ", "-")}.ini"

    print(f"{file_name}")

    return 0


if "__main__" == __name__:
    main()
