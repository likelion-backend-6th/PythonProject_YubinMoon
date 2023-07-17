from __future__ import annotations
import unicodedata
import os


def get_string_width(string: str) -> int:
    count = sum(1 + (unicodedata.east_asian_width(c) in "WF") for c in string)
    return count


def pre_format(string: str, width: int, align: str = "<", fill: str = " ") -> str:
    count = width - sum(1 + (unicodedata.east_asian_width(c) in "WF") for c in string)
    return {
        ">": lambda s: fill * count + s,  # lambda 매개변수 : 표현식
        "<": lambda s: s + fill * count,
        "^": lambda s: fill * (count // 2) + s + fill * (count // 2 + count % 2),
    }[align](string)


class RenderData:
    def __init__(
        self,
        menu_list: list[str] | None = None,
        select_data: int | None = None,
        detail_data: list[list[str]] | str = [],
    ):
        self.menu_list = menu_list
        self.select_data = select_data
        if isinstance(detail_data, str):
            self.detail_data = []
            for line in detail_data.split("\n"):
                self.detail_data.append([line])
            detail_data = [[detail_data]]
        else:
            self.detail_data = detail_data

    def update(self, data: RenderData) -> None:
        if data.menu_list:
            self.menu_list = data.menu_list
        if data.select_data is not None:
            self.select_data = data.select_data
        if data.detail_data:
            self.detail_data = data.detail_data
        if self.select_data == -1:
            self.select_data = None

    def get_detail_line_with_width(self, num: int, width: int) -> str:
        if num >= len(self.detail_data):
            return " " * width
        line = self.detail_data[num]
        text = line[0]
        center = False
        ellipsis = "right"
        if len(line) > 1:
            for option in line[1:]:
                if option == "center":
                    center = True
                elif option.startswith("ellipsis"):
                    el_type = option.split("-")[1]
                    if el_type == "left":
                        ellipsis = "left"
                    elif el_type == "right":
                        ellipsis = "right"
                    elif el_type == "center":
                        ellipsis = "center"
        if get_string_width(text) <= width:
            rest = width - get_string_width(text)
            if center:
                return " " * (rest // 2) + text + " " * (rest - rest // 2)
            else:
                return text + " " * rest
        else:
            if ellipsis == "right":
                return text[: width - 3] + "..."
            elif ellipsis == "left":
                return "..." + text[3 - width :]
            elif ellipsis == "center":
                return text[: (width - 3) // 2] + "..." + text[1 - (width - 3) // 2 :]


class Printer:
    def __init__(self):
        # TODO 화면 설정 같은 것들 추가
        window = os.get_terminal_size()
        self.width = window.columns
        self.height = window.lines
        self.split_loc = 20
        self.clear_code = "cls" if os.name == "nt" else "clear"
        self.pre_screen = ""

    def print(self, data: RenderData) -> None:
        self.data = data
        print_data = self.render()
        if self.pre_screen != print_data:
            self.pre_screen = print_data
            # os.system(self.clear_code)
            for _ in range(self.height):
                print("\033[F", end="")
            print(print_data, end="")

    def render(self) -> str:
        print_data = ""
        print_data += self.make_top()
        for line_num in range(self.height - 2):
            print_data += self.make_line(line_num)
        print_data += self.make_bottom()
        return print_data.rstrip()

    def make_top(self) -> str:
        top = ["─"] * (self.width)
        top[0] = "┌"
        top[-1] = "┐"
        top[self.split_loc] = "┬"
        return "".join(top) + "\n"

    def make_bottom(self) -> str:
        bottom = ["─"] * (self.width)
        bottom[0] = "└"
        bottom[-1] = "┘"
        bottom[self.split_loc] = "┴"
        return "".join(bottom) + "\n"

    def get_split_num(self, data: RenderData) -> int:
        return max([len(x) for x in data.menu_list]) + 4

    def make_line(self, line_num: int) -> str:
        result = ""
        text = ""
        if line_num < len(self.data.menu_list):
            text = self.data.menu_list[line_num]
        if self.data.select_data is not None and line_num == self.data.select_data:
            result += f"> {text}"
        else:
            result += f"  {text}"
        result += " " * (self.split_loc - self.real_len(result) - 1)
        content = self.data.get_detail_line_with_width(
            line_num, self.width - self.split_loc - 3
        )
        return "│" + result + "│ " + content + "│\n"

    def real_len(self, text: str) -> int:
        result = 0
        for c in text:
            result += 1 if len(c.encode("utf-8")) == 1 else 2
        return result
