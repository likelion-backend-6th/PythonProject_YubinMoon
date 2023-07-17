from datetime import datetime
from utils import Printer, RenderData, pre_format
from page.base import BasePage
import database as db
import keyboard
import os
import page


class Controller:
    def __init__(self):
        self.printer = Printer()
        self.render_data = RenderData()
        self.page_stack: list[BasePage] = []
        self.page_name_stack: list[str] = []
        self.change_page("main")

    def run(self) -> None:
        while True:
            try:
                self.print_display()
                key = self.get_key_input()
                event = self.page_stack[-1].run(key)
                if event:
                    self.handle_event(event)
            except KeyboardInterrupt:
                self.exit()

    def print_display(self) -> None:
        render_data = self.page_stack[-1].get_render_data()
        self.render_data.update(render_data)
        self.printer.print(self.render_data)

    def get_key_input(self) -> str:
        while True:
            key = keyboard.read_event()
            if key.event_type == "down":
                return key.name

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
            return page.MainPage()
        elif name == "help":
            return page.HelpPage()
        elif name == "new_books":
            return page.NewBooksPage()
        elif name == "new_book_with_user_input":
            return page.NewBooksWithUserInput()
        elif name == "new_book_with_user_input_check":
            return page.NewBooksWithUserInputCheck()
        elif name == "new_book_with_user_input_done":
            return page.NewBooksWithUserInputDone()
        elif name == "new_book_with_file_input":
            return page.NewBooksWithFileInput()
        elif name == "new_book_with_file_input_check":
            return page.NewBooksWithFileInputCheck()
        elif name == "new_book_with_file_input_done":
            return page.NewBooksWithFileInputDone()
        elif name == "inquire_all_books":
            return page.BooksListPage()
        elif name == "book_detail":
            return page.BookDetailPage()
        elif name == "loan_history":
            return page.LoanHistoryPage()
        elif name == "all_loan_history":
            return page.AllLoanHistoryPage()
        else:
            raise ValueError(f"page: {name} is not exist")

    def exit(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print("종료합니다.")
        exit(0)


if __name__ == "__main__":
    db.create_tables()
    Controller().run()
