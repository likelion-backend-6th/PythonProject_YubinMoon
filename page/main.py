from utils import pre_format
from .base import BasePage, BaseMenuPage


class HelpPage(BasePage):
    def __init__(self):
        super().__init__()
        self.detail = ""
        self.detail += "도움말"
        self.detail += "\n\n"
        self.detail += pre_format("k", 8)
        self.detail += ": UP\n"
        self.detail += pre_format("j", 8)
        self.detail += ": DOWN\n"
        self.detail += pre_format("h", 8)
        self.detail += ": LEFT | 도움말\n"
        self.detail += pre_format("l", 8)
        self.detail += ": RIGHT\n"
        self.detail += pre_format("q", 8)
        self.detail += ": 종료 | 뒤로가기\n"
        self.detail += pre_format("b", 8)
        self.detail += ": 뒤로가기\n"
        self.detail += pre_format("i", 8)
        self.detail += ": id 검색\n"
        self.detail += pre_format("t", 8)
        self.detail += ": title 검색\n"
        self.detail += pre_format("esc", 8)
        self.detail += ": 뒤로가기\n"
        self.detail += pre_format("enter", 8)
        self.detail += ": 선택\n"
        self.detail += "\nPress any key to continue..."


class MainPage(BaseMenuPage):
    def __init__(self):
        super().__init__()
        self.menu_list = [
            ["도서 추가", "new_books"],
            ["도서 조회", "inquire_all_books"],
            ["대출 조회", "all_loan_history"],
        ]
        self.selected = -1
        self.detail = "WELCOME"
        self.detail += "\n"
        self.detail += "\nthis page is main"
        self.detail += "\nmade by yubin"
        self.detail += "\npress `h` to help"
