from __future__ import annotations
import keyboard
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
        os.system("cls")
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
        text_data_list = data.detail_data.split("\n")
        text_list = []
        for text_data in text_data_list:
            while text_data:
                text_list.append(text_data[:width])
                text_data = text_data[width:]
        return text_list


class BasePage:
    def __init__(self):
        pass

    def get_render_data(self) -> RenderData:
        raise NotImplementedError

    def run(self) -> str | None:
        raise NotImplementedError


class MainPage(BasePage):
    def __init__(self):
        super().__init__()
        self.menu_list = [
            "메뉴1",
            "메뉴2",
            "메뉴3",
        ]
        self.selected = None
        self.detail = """
        WELCOME
        this page is main
        made by yubin
        press "h" to help"""

    def get_render_data(self) -> RenderData:
        return RenderData(
            menu_list=self.menu_list,
            select_data=self.selected,
            detail_data=self.detail,
        )

    def run(self, input) -> str | None:
        return input


class Controller:
    def __init__(self):
        self.page = self.get_page("main")
        self.printer = Printer()
        self.page_stack = ["main"]

    def run(self):
        while True:
            self.printer.print(self.page.get_render_data())
            key = self.get_key_input()
            result = self.page.run(key)

    def get_page(self, page_name: str):
        if page_name == "main":
            return MainPage()
        raise ValueError(f"page_name: {page_name} is not exist")

    def get_key_input(self) -> str:
        while True:
            key = keyboard.read_event()
            if key.event_type == "down":
                return key.name


if __name__ == "__main__":
    Controller().run()
