from __future__ import annotations
import psycopg2
import setting
import database as db
import keyboard
import os
import csv


def real_len(text: str) -> int:
    result = 0
    for c in text:
        result += 1 if len(c.encode("utf-8")) == 1 else 2
    return result


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
        if real_len(text) <= width:
            rest = width - real_len(text)
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
    # TODO 방향키 입력 추가
    # TODO data 클래스 따로 빼기
    data: list[list[str]] = []

    def __init__(self):
        super().__init__()
        NewBooksWithUserInput.data = [
            ["ID", ""],
            ["TITLE", ""],
            ["AUTHOR", ""],
            ["PUB", ""],
        ]
        self.base_detail = """도서 추가"""
        self.selected_num = 0

    def get_render_data(self) -> RenderData:
        self.detail = self.base_detail
        for index, (name, value) in enumerate(NewBooksWithUserInput.data):
            self.detail += f"\n{name}: {value}" + (
                "|" if self.selected_num == index else ""
            )
        return super().get_render_data()

    def run(self, key: str) -> str | None:
        if key == "esc":
            return "back"
        self.add_text(key)
        if key == "enter":
            if self.selected_num == len(NewBooksWithUserInput.data) - 1:
                return "new_book_with_user_input_check"
            else:
                self.selected_num += 1

    def add_text(self, key: str) -> None:
        if len(key) == 1:
            self.data[self.selected_num][1] += key
        elif key == "space":
            self.data[self.selected_num][1] += " "
        elif key == "backspace":
            self.data[self.selected_num][1] = self.data[self.selected_num][1][:-1]


class NewBooksWithUserInputCheck(BasePage):
    def __init__(self):
        super().__init__()
        self.user_selected = "Y"
        self.base_detail = """도서 추가 확인\nsdaasdfasdfasdfasdfasdfasdfasdfgahjsdfgjhasdgjhfgashjdfgjahsdgfjhasdgfjhasgdhjfgasdjhfgjhasdhjfgasdhjgfjhagd"""

    def get_render_data(self) -> RenderData:
        self.detail = self.base_detail
        self.detail += "\n"
        for index, (name, value) in enumerate(NewBooksWithUserInput.data):
            self.detail += f"\n{name}: {value}"
        self.detail += "\n\n"
        if self.user_selected == "Y":
            self.detail += "|Y|  N "
        else:
            self.detail += " Y  |N|"
        return super().get_render_data()

    def run(self, key: str) -> str | None:
        key = key.lower()
        if key == "l":
            self.user_selected = "N"
        elif key == "h":
            self.user_selected = "Y"
        elif key == "esc":
            return "back"
        elif key == "enter":
            if self.user_selected == "Y":
                self.create_new_book()
                return "new_book_with_user_input_done"
            else:
                return "back"

    def create_new_book(self) -> None:
        db.create_book(
            NewBooksWithUserInput.data[0][1],
            NewBooksWithUserInput.data[1][1],
            NewBooksWithUserInput.data[2][1],
            NewBooksWithUserInput.data[3][1],
        )


class NewBooksWithUserInputDone(BasePage):
    def __init__(self):
        super().__init__()
        self.detail = """도서 추가 완료\n\nPress any key to continue..."""

    def run(self, key: str) -> str:
        return "new_books"


class NewBooksWithFileInput(BasePage):
    selected_file: str | None = None

    def __init__(self):
        super().__init__()
        self.base_detail = """도서 추가"""
        self.file_list = []
        self.selected_num = 0
        self.input_folder = os.path.join(os.getcwd(), setting.INPUT_FOLDER)
        if os.path.isdir(self.input_folder):
            self.file_list = self.get_file_list()

    def get_file_list(self) -> list[str]:
        file_list = []
        for root, _, files in os.walk(self.input_folder):
            for file in files:
                if file.endswith((".json", ".csv", ".xml")):
                    file_list.append(os.path.join(root, file))
        return file_list

    def get_render_data(self) -> RenderData:
        self.detail = self.base_detail
        if self.file_list:
            self.detail += "\n"
            for index, file in enumerate(self.file_list):
                self.detail += f"\n{file}" + (
                    " <" if self.selected_num == index else ""
                )
        else:
            self.detail += "\n"
            self.detail += "\nNo file"
            self.detail += "\nPlease add file to input folder"
            self.detail += f"\ninput folder: {self.input_folder}"
        return super().get_render_data()

    def run(self, key: str) -> str | None:
        if key == "esc" or key == "b":
            return "back"
        elif key == "enter":
            if self.file_list:
                NewBooksWithFileInput.selected_file = self.file_list[self.selected_num]
                return "new_book_with_file_input_check"
            else:
                return "back"
        else:
            self.move_list(key)

    def move_list(self, key: str) -> None:
        key = key.lower()
        if key == "k":
            if 0 < self.selected_num:
                self.selected_num -= 1
            else:
                self.selected_num = len(self.file_list) - 1
        elif key == "j":
            if self.selected_num < len(self.file_list) - 1:
                self.selected_num += 1
            else:
                self.selected_num = 0


class NewBooksWithFileInputCheck(BasePage):
    def __init__(self):
        super().__init__()
        self.user_selected = "Y"
        self.base_detail = """도서 추가 확인"""
        self.data = self.get_data_from_file()

    def get_data_from_file(self) -> list[list[str]]:
        # TODO 다른 파일 형식 지원
        try:
            file = NewBooksWithFileInput.selected_file
            if file.endswith(".csv"):
                return self.get_data_from_csv(file)
            elif file.endswith(".json"):
                raise NotImplementedError("from json not implemented")
            elif file.endswith(".xml"):
                raise NotImplementedError("from xml not implemented")
            else:
                raise ValueError(f"File name not valid: {file}")
        except Exception as e:
            self.error_message = str(e)
            return []

    def get_data_from_csv(self, file: str) -> list[tuple[str, str]]:
        data_list: list[list[str]] = []
        with open(file, "r", encoding="utf-8") as f:
            rdr = csv.reader(f)
            for line in rdr:
                data_list.append(line)
        col_names: list[str] = data_list.pop(0)
        if col_names[0].lower() not in ["id", "도서id", "도서 id"]:
            print(col_names[0].lower())
            raise ValueError("ID is not in the first column")
        if col_names[1].lower() not in ["title", "도서명", "도서 명", "제목"]:
            raise ValueError("Title is not in the second column")
        if col_names[2].lower() not in ["author", "저자"]:
            raise ValueError("Author is not in the third column")
        if col_names[3].lower() not in ["pub", "publisher", "출판사"]:
            raise ValueError("Publisher is not in the fourth column")
        if col_names[4].lower() not in [
            "is_available",
            "is available",
            "도서상태",
            "도서 상태",
        ]:
            raise ValueError("Is_available is not in the fifth column")
        for data in data_list:
            is_available = data[4].lower()
            if is_available in ["true", "대출 가능", "대출가능"]:
                data[4] = True
            else:
                data[4] = False
        return data_list

    def get_render_data(self) -> RenderData:
        self.detail = self.base_detail
        self.detail += "\n"
        if self.data:
            self.detail += f'--{["ID", "도서명", "저자", "출판사", "도서 상태"]}--'
            for data in self.data:
                self.detail += f"\n{data}"
            self.detail += "\n\n"
            if self.user_selected == "Y":
                self.detail += "|Y|  N "
            else:
                self.detail += " Y  |N|"
        else:
            self.detail += self.error_message
        return super().get_render_data()

    def run(self, key: str) -> str | None:
        key = key.lower()
        if key == "l":
            self.user_selected = "N"
        elif key == "h":
            self.user_selected = "Y"
        elif key == "esc":
            return "back"
        elif key == "enter":
            if self.user_selected == "Y":
                self.create_new_book()
                return "new_book_with_file_input_done"
            else:
                return "back"


class Controller:
    def __init__(self):
        self.printer = Printer()
        self.render_data = RenderData()
        self.page_stack: list[BasePage] = []
        self.page_name_stack: list[str] = []
        self.change_page("main")

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
                self.page_name_stack.pop()
        elif event == "exit":
            self.exit()
        else:
            self.change_page(event)

    def change_page(self, event: str) -> None:
        if event in self.page_name_stack:
            index = self.page_name_stack.index(event)
            self.page_stack = self.page_stack[: index + 1]
            self.page_name_stack = self.page_name_stack[: index + 1]
        else:
            page = self.get_page_by_name(event)
            self.page_stack.append(page)
            self.page_name_stack.append(event)

    def get_page_by_name(self, name: str) -> BasePage:
        if name == "main":
            return MainPage()
        elif name == "new_books":
            return NewBooksPage()
        elif name == "new_book_with_user_input":
            return NewBooksWithUserInput()
        elif name == "new_book_with_user_input_check":
            return NewBooksWithUserInputCheck()
        elif name == "new_book_with_user_input_done":
            return NewBooksWithUserInputDone()
        elif name == "new_book_with_file_input":
            return NewBooksWithFileInput()
        elif name == "new_book_with_file_input_check":
            return NewBooksWithFileInputCheck()
        else:
            raise ValueError(f"page: {name} is not exist")

    def exit(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print("종료합니다.")
        exit(0)


if __name__ == "__main__":
    db.create_tables()
    Controller().run()
