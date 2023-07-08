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
        self.split_loc = 20
        self.clear_code = "cls" if os.name == "nt" else "clear"
        self.pre_screen = ""

    def print(self, data: RenderData) -> None:
        self.data = data
        print_data = self.render()
        if self.pre_screen != print_data:
            self.pre_screen = print_data
            os.system(self.clear_code)
            print(print_data, end="")

    def render(self) -> str:
        text_list = self.make_str_list(self.width - self.split_loc - 3)
        print_data = ""
        for line_num in range(self.height):
            print_data += self.make_line(text_list, line_num)
        return print_data.rstrip()

    def get_split_num(self, data: RenderData) -> int:
        return max([len(x) for x in data.menu_list]) + 4

    def make_str_list(self, width: int) -> list[str]:
        text_data_list = self.data.detail_data.split("\n")
        text_list = []
        for text_data in text_data_list:
            while text_data:
                text_list.append(text_data[:width])
                text_data = text_data[width:]
        return text_list

    def make_line(self, text_list: list[str], line_num: int) -> str:
        result = ""
        text = ""
        if line_num < len(self.data.menu_list):
            text = self.data.menu_list[line_num]
        text_len = self.real_len(text)
        if self.data.select_data is not None and line_num == self.data.select_data:
            result += f"> {text}"
        else:
            result += f"  {text}"
        result += " " * (self.split_loc - self.real_len(result) - 4)
        result += "||"
        if line_num < len(text_list):
            result += text_list[line_num]
        result += "\n"
        return result

    def real_len(self, text: str) -> int:
        result = 0
        for c in text:
            result += 1 if len(c.encode("utf-8")) == 1 else 2
        return result


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

    def run(self, key: str) -> str | None:
        if key == "k":
            if self.selected is None:
                self.selected = 0
            elif 0 < self.selected:
                self.selected -= 1
            else:
                self.selected = len(self.menu_list) - 1
        elif key == "j":
            if self.selected is None:
                self.selected = 0
            elif self.selected < len(self.menu_list) - 1:
                self.selected += 1
            else:
                self.selected = 0
        elif key == "h":
            return "help"
        elif key == "q":
            return "exit"
        elif key == "enter":
            return self.menu_list[self.selected]
        elif key == "esc":
            self.selected = -1


class Controller:
    def __init__(self):
        self.page = self.get_page("main")
        self.printer = Printer()
        self.render_data = RenderData()
        self.page_stack = ["main"]

    def run(self):
        while True:
            self.print_display()
            key = self.get_key_input()
            result = self.page.run(key)
            if result:
                self.page = self.get_page(result)

    def print_display(self):
        render_data = self.page.get_render_data()
        self.render_data.update(render_data)
        self.printer.print(self.render_data)

    def get_page(self, page_name: str):
        if page_name == "main":
            return MainPage()
        if page_name == "exit":
            self.exit()
        raise ValueError(f"page_name: {page_name} is not exist")

    def get_key_input(self) -> str:
        try:
            while True:
                key = keyboard.read_event()
                if key.event_type == "down":
                    return key.name
        except KeyboardInterrupt:
            self.exit()

    def exit(self):
        print()
        print("종료합니다.")
        exit(0)


if __name__ == "__main__":
    Controller().run()
