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
        text_list = self.data.detail_data.split("\n")
        print_data = ""
        print_data += self.make_top()
        for line_num in range(self.height - 2):
            print_data += self.make_line(text_list, line_num)
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

    def make_line(self, text_list: list[str], line_num: int) -> str:
        result = ""
        text = ""
        if line_num < len(self.data.menu_list):
            text = self.data.menu_list[line_num]
        if self.data.select_data is not None and line_num == self.data.select_data:
            result += f"> {text}"
        else:
            result += f"  {text}"
        result += " " * (self.split_loc - self.real_len(result) - 1)
        result += "│"
        content = " "
        if line_num < len(text_list):
            content += text_list[line_num]
        content += " " * (self.width - self.split_loc - self.real_len(content) - 2)
        return "│" + result + content + "│\n"

    def real_len(self, text: str) -> int:
        result = 0
        for c in text:
            result += 1 if len(c.encode("utf-8")) == 1 else 2
        return result


class BasePage:
    def __init__(self):
        self.menu_list: list[list[str]] | None = None
        self.selected = None
        self.detail = ""

    def get_render_data(self) -> RenderData:
        return RenderData(
            menu_list=None,
            select_data=None,
            detail_data=self.detail,
        )

    def run(self) -> str | None:
        raise NotImplementedError


class BaseMenuPage(BasePage):
    def __init__(self):
        super().__init__()
        self.menu_list: list[list[str]] = []
        self.selected = -1

    def get_render_data(self) -> RenderData:
        return RenderData(
            menu_list=[name for name, _ in self.menu_list],
            select_data=self.selected,
            detail_data=self.detail,
        )

    def run(self, key: str) -> str | None:
        key = key.lower()
        self.move_menu(key)
        if key == "h":
            return "help"
        elif key == "q":
            return "exit"
        elif key == "b":
            return "back"
        elif key == "enter":
            if self.selected is not None and 0 <= self.selected < len(self.menu_list):
                return self.menu_list[self.selected][1]

    def move_menu(self, key: str) -> None:
        key = key.lower()
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
        elif key == "esc":
            self.selected = -1


class MainPage(BaseMenuPage):
    def __init__(self):
        super().__init__()
        self.menu_list = [
            ["도서 추가", "new_books"],
            ["도서 조회", "test"],
            ["대출 조회", "test"],
        ]
        self.selected = -1
        self.detail = """WELCOME
this page is main
made by yubin
press "h" to help"""


class NewBooksPage(BaseMenuPage):
    def __init__(self):
        super().__init__()
        self.menu_list = [
            ["직접 입력", "new_book_with_user_input"],
            ["파일 입력", "new_book_with_file_input"],
        ]
        self.selected = -1
        self.detail = """도서 추가"""


class NewBooksWithUserInput(BasePage):
    data: list[list[str]] = []

    def __init__(self):
        super().__init__()
        self.data = [["ID", ""], ["TITLE", ""], ["AUTHOR", ""], ["PUB", ""]]
        self.base_detail = """도서 추가"""
        self.selected_num = 0

    def get_render_data(self) -> RenderData:
        self.detail = self.base_detail
        for index, (name, value) in enumerate(self.data):
            self.detail += f"\n{name}: {value}" + (
                "|" if self.selected_num == index else ""
            )
        return super().get_render_data()

    def run(self, key: str) -> str | None:
        if key == "esc":
            return "back"
        self.add_text(key)
        if key == "enter":
            if self.selected_num == len(self.data) - 1:
                return "next"
            else:
                self.selected_num += 1

    def add_text(self, key: str) -> None:
        if len(key) == 1:
            self.data[self.selected_num][1] += key
        elif key == "space":
            self.data[self.selected_num][1] += " "
        elif key == "backspace":
            self.data[self.selected_num][1] = self.data[self.selected_num][1][:-1]


class Controller:
    def __init__(self):
        self.printer = Printer()
        self.render_data = RenderData()
        self.page_stack: list[BasePage] = []
        self.insert_page("main")

    def run(self) -> None:
        while True:
            self.print_display()
            key = self.get_key_input()
            event = self.page_stack[-1].run(key)
            if event:
                self.handle_event(event)

    def print_display(self) -> None:
        render_data = self.page_stack[-1].get_render_data()
        self.render_data.update(render_data)
        self.printer.print(self.render_data)

    def get_key_input(self) -> str:
        try:
            while True:
                key = keyboard.read_event()
                if key.event_type == "down":
                    return key.name
        except KeyboardInterrupt:
            self.exit()

    def handle_event(self, event: str) -> None:
        if event == "back":
            if 1 < len(self.page_stack):
                self.page_stack.pop()
        elif event == "exit":
            self.exit()
        else:
            self.insert_page(event)

    def insert_page(self, event: str) -> None:
        page = self.get_page_by_name(event)
        self.page_stack.append(page)

    def get_page_by_name(self, name: str) -> BasePage:
        if name == "main":
            return MainPage()
        elif name == "new_books":
            return NewBooksPage()
        elif name == "new_book_with_user_input":
            return NewBooksWithUserInput()
        else:
            raise ValueError(f"page: {name} is not exist")

    def exit(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print("종료합니다.")
        exit(0)


if __name__ == "__main__":
    Controller().run()
