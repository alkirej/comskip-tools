
class Chapter:
    # **********************************
    # index = srt file index line (often ignored by video display apps)
    # times = TimeBlock indicating when the subtitle should begin and end
    #                its display on the screen.
    # text  = what to display on the screen subtitle line
    # **********************************
    def __init__(self,
                 header: str,
                 timebase: int,
                 start: int,
                 end: int,
                 title: str
                 ):
        self.header: str = header
        self.timebase: int = timebase
        self.start: int = start
        self.end: int = end
        self.title: str = title

    def truncate_to(self, last_second: float) -> None:
        end_time: int = int(last_second * self.timebase)
        if self.end > end_time:
            self.end = end_time
        if self.start > end_time:
            self.start = end_time

    def __str__(self) -> str:
        return "".join(
                f"{self.header}\n"
                + f"TIMEBASE=1/{self.timebase}\n"
                + f"START={self.start}\n"
                + f"END={self.end}\n"
                + f"title={self.title}\n"
        )


class FFMetaFile:
    def __init__(self, filename: str):
        self._filename: str = filename
        self._comment: str | None = None
        self._chapters: [Chapter] = self._load_from_file()

    def _load_from_file(self) -> [Chapter]:
        chapters = []

        with open(self._filename, "r", encoding="utf-8") as ffmeta_file:
            lines: [str] = ffmeta_file.readlines()
            lines = [ln.strip() for ln in lines]

        line_count: int = len(lines)
        ln_nbr: int = 0
        if lines[ln_nbr].startswith(";"):
            self._comment = lines[ln_nbr]
            ln_nbr += 1

        while ln_nbr < line_count:
            chapter_hdr: str = lines[ln_nbr]
            timebase: int = int(lines[ln_nbr+1].split("1/")[1])
            start: int = int(lines[ln_nbr+2].split("=")[1])
            end: int = int(lines[ln_nbr+3].split("=")[1])
            title: str = lines[ln_nbr+4].split("=")[1]
            ln_nbr += 5

            chapter = Chapter(chapter_hdr, timebase, start, end, title)
            chapters.append(chapter)

        return chapters

    def write_metadata(self) -> None:
        with open(self._filename, "w", encoding="utf-8") as ffmeta_file:
            ffmeta_file.write(str(self))

    def __str__(self) -> str:
        body: [str] = [str(ch) for ch in self._chapters]
        return f"{self._comment}\n{"".join(body)}"

    def truncate_to(self, end_of_video: float) -> None:
        for ch in self._chapters:
            ch.truncate_to(end_of_video)
