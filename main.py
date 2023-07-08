from __future__ import annotations
import os


class RenderData:
    def __init__(
        self,
        menu_list: list[str] | None = None,
        select_data: int | None = None,
        detail_data: str = "",
    ):
        self.menu_list = menu_list
        self.select_data = select_data
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


class Printer:
    def __init__(self, size: tuple[int, int] = None):
        # TODO 화면 설정 같은 것들 추가
        window = os.get_terminal_size()
        self.width = window.columns
        self.height = window.lines

    def print(self, data: RenderData) -> None:
        print_data = self.render(data)
        print(print_data, end="")

    def render(self, data: RenderData) -> str:
        split_num = self.get_split_num(data)
        text_list = self.make_str_list(data, self.width - split_num - 3)
        print_data = ""
        for i in range(self.height):
            text = ""
            if i < len(data.menu_list):
                text = data.menu_list[i]
            if data.select_data is not None and i == data.select_data:
                print_data += f"> {text:<{split_num}}||"
            else:
                print_data += f"  {text:<{split_num}}||"
            if i < len(text_list):
                print_data += text_list[i]
            print_data += "\n"
        return print_data.rstrip()

    def get_split_num(self, data: RenderData) -> int:
        return max([len(x) for x in data.menu_list]) + 4

    def make_str_list(self, data: RenderData, width: int) -> list[str]:
        text_data = data.detail_data
        text_list = []
        while text_data:
            text_list.append(text_data[:width])
            text_data = text_data[width:]
        return text_list


if __name__ == "__main__":
    printer = Printer()
    render_data = RenderData(
        menu_list=["a", "b", "c"], select_data=1, detail_data="detail"
    )
    printer.print(render_data)
    input()
