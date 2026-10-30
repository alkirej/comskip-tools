import os
import sys


def dir_exist_check(name: str) -> str:
    if os.path.isdir(name):
        return name
    else:
        print(f"Unable to find a directory named {name}")
        sys.exit(1)


def main() -> int:
    args: str = " ".join(sys.argv[1:])
    paren_loc: int = args.index("(")
    last_char_in_name: int = min(15, paren_loc)
    dir_name: str = args[:last_char_in_name]

    print(f"{dir_name.lower().replace(" ", "-")}")

    return 0


if "__main__" == __name__:
    main()

