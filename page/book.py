from .base import BasePage, BaseMenuPage
from datetime import datetime
from utils import RenderData
import setting
import database as db
import psycopg2
import csv
import os
from .base import detail_pk


class NewBooksPage(BaseMenuPage):
    def __init__(self):
        super().__init__()
        self.menu_list = [
            ["직접 입력", "new_book_with_user_input"],
            ["파일 입력", "new_book_with_file_input"],
        ]
        self.selected = -1
        self.detail = "도서 추가"
        self.detail += "\n\n"
        self.detail += "이곳에서 새로운 도서를 추가하세요"
        self.detail += "\n\n"
        self.detail += "직접 입력할 수도 있고"
        self.detail += "\n파일로도 입력할 수 있습니다."
        self.detail += "\n\n"
        self.detail += "파일로 입력하는 경우"
        self.detail += f"\n'{setting.INPUT_FOLDER}` 폴더에"
        self.detail += "\n파일을 넣어주세요"


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
        self.base_detail = "도서 정보 입력\n"
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
        self.base_detail = "도서 정보 확인\n"

    def get_render_data(self) -> RenderData:
        self.detail = self.base_detail
        for name, value in NewBooksWithUserInput.data:
            self.detail += f"\n{name}: {value}"
        self.detail += "\n\n"
        self.detail += "입력한 정보가 맞습니까?\n"
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
        # TODO 입력 에러처리 추가
        db.create_book(
            NewBooksWithUserInput.data[0][1],
            NewBooksWithUserInput.data[1][1],
            NewBooksWithUserInput.data[2][1],
            NewBooksWithUserInput.data[3][1],
        )


class NewBooksWithUserInputDone(BasePage):
    def __init__(self):
        super().__init__()
        self.detail = "도서 추가 완료"
        self.detail += "\n\n"
        self.detail += "새로운 도서가 추가되었습니다.\n\n"
        self.detail += "Press any key to continue..."

    def run(self, key: str) -> str:
        return "new_books"


class NewBooksWithFileInput(BasePage):
    selected_file: str | None = None

    def __init__(self):
        super().__init__()
        self.base_detail = "도서 파일 선택\n"
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
            self.detail += "입력할 파일을 선택해주세요.\n"
            for index, file in enumerate(self.file_list):
                file_name = file.split(setting.INPUT_FOLDER, 1)[1][1:]
                self.detail += f"\n{file_name}" + (
                    " <" if self.selected_num == index else ""
                )
        else:
            self.detail += "\n입력 파일을 찾을 수 없습니다."
            self.detail += "\n입력 폴더를 확인해 주세요"
            self.detail += f"\ninput folder: {self.input_folder}"
            self.detail += "\n\nvalid file format: json, csv, xml"

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
        self.base_detail = "파일 내용 확인\n"
        self.error_message = ""
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
        if self.error_message:
            self.detail += self.error_message
        else:
            self.detail += f"|  ID  |  도서명  |  저자  |  출판사  |  도서 상태  |"
            self.detail += "\n"
            for data in self.data:
                self.detail += f"\n{data}"
            self.detail += "\n\n"
            self.detail += "입력한 정보가 맞습니까?\n"
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
                try:
                    self.create_new_books()
                except psycopg2.Error as e:
                    self.error_message = str(e)
                    return
                return "new_book_with_file_input_done"
            else:
                return "back"

    def create_new_books(self):
        for data in self.data:
            book = db.create_book(
                book_id=data[0],
                title=data[1],
                author=data[2],
                publisher=data[3],
                is_available=data[4],
            )


class NewBooksWithFileInputDone(BasePage):
    def __init__(self):
        super().__init__()
        self.detail = "도서 추가 완료"
        self.detail += "\n\n"
        self.detail += "새로운 도서가 추가되었습니다.\n\n"
        self.detail += "Press any key to continue..."

    def run(self, key: str) -> str:
        return "new_books"


class BooksListPage(BasePage):
    def __init__(self):
        super().__init__()
        self.base_detail = "도서 목록"
        self.book_count = db.count_books()
        self.selected_num = 0
        self.mode = "normal"
        self.search_type = "id"
        self.input = ""

    def get_render_data(self) -> RenderData:
        if self.selected_num >= self.book_count:
            self.selected_num = self.book_count - 1
        self.detail = self.base_detail
        self.detail += "\n\n"
        if self.mode == "search":
            self.detail += f"Search {self.search_type.upper()}: {self.input}|\n"
        self.detail += self.get_books_table()
        return super().get_render_data()

    def get_books_table(self) -> str:
        global detail_pk
        result = ""
        offset = min(self.book_count - 5, self.selected_num - 5)
        offset = max(0, offset)
        selected_num = self.selected_num - offset
        if self.input:
            if self.search_type == "id":
                book_list = db.read_books_by_Book_id(
                    self.input, offset=offset, limit=20
                )
            elif self.search_type == "title":
                book_list = db.read_books_by_title(self.input, offset=offset, limit=20)
            else:
                book_list = db.read_books(offset=offset, limit=20, order_by="book_id")
        else:
            book_list = db.read_books(offset=offset, limit=20, order_by="book_id")
        result += "---ID---|---Title---|---Author---|---Publisher---|---Status---\n"
        for index, book in enumerate(book_list):
            line = f"{book[1]} | {book[2]} | {book[3]} | {book[4]} | {'대출 가능' if book[5] else '대출 불가능'}"
            if index == selected_num:
                detail_pk = book[0]
                result += f"> {line} <"
            else:
                result += f"  {line}  "
            result += "\n"
        return result

    def run(self, key: str) -> str | None:
        if self.mode == "normal":
            return self.normal_mode(key)
        elif self.mode == "search":
            self.search_id_mode(key)

    def normal_mode(self, key: str) -> str | None:
        key = key.lower()
        if key == "k":
            if 0 < self.selected_num:
                self.selected_num -= 1
        elif key == "j":
            if self.selected_num < self.book_count - 1:
                self.selected_num += 1
        elif key == "enter":
            if 0 <= self.selected_num < self.book_count:
                return "book_detail"
        elif key == "i":
            self.mode = "search"
            self.search_type = "id"
        elif key == "t":
            self.mode = "search"
            self.search_type = "title"
        elif key == "h":
            return "book_search_help"
        elif key == "esc" or key == "b" or key == "q":
            return "back"

    def search_id_mode(self, key: str) -> str | None:
        self.insert_text(key)
        key = key.lower()
        if key == "esc" or key == "enter":
            self.mode = "normal"

        if self.search_type == "id":
            self.book_count = db.count_books_by_book_id(book_id=self.input)
        elif self.search_type == "title":
            self.book_count = db.count_books_by_title(title=self.input)

    def insert_text(self, key: str) -> None:
        if len(key) == 1:
            self.input += key
        elif key == "space":
            self.input += " "
        elif key == "backspace":
            self.input = self.input[:-1]


class BookDetailPage(BasePage):
    def __init__(self):
        super().__init__()
        self.user_selected = "L"
        self.base_detail = "도서 상세"
        self.get_book_data()

    def get_book_data(self) -> None:
        self.book = db.read_book_by_pk(detail_pk)

    def get_render_data(self) -> RenderData:
        self.detail = self.base_detail
        self.detail += "\n"
        self.detail += f"\n도서 ID: {self.book[1]}"
        self.detail += f"\n제목: {self.book[2]}"
        self.detail += f"\n저자: {self.book[3]}"
        self.detail += f"\n출판사: {self.book[4]}"
        self.detail += f"\n상태: {'대출 가능' if self.book[5] else '대출 중'}"
        self.detail += "\n\n"

        self.type = "대출하기" if self.book[5] else "반납하기"
        if self.user_selected == "L":
            self.detail += f">대출 기록<  {self.type}"
        elif self.user_selected == "R":
            self.detail += f" 대출 기록  >{self.type}<"
        return super().get_render_data()

    def run(self, key: str) -> str | None:
        key = key.lower()
        if key == "l":
            self.user_selected = "R"
        elif key == "h":
            self.user_selected = "L"
        elif key == "esc" or key == "q" or key == "b":
            return "back"
        elif key == "enter":
            if self.user_selected == "L":
                return "loan_history"
            elif self.user_selected == "R":
                return self.loan_book()

    def loan_book(self) -> str | None:
        if self.book[5]:
            db.create_loan(book_pk=detail_pk, loan_date=datetime.now())
            db.update_book(detail_pk, values={"is_available": False})
        else:
            loan_data = db.read_loan_return_null(detail_pk)
            if loan_data is None:
                pk = db.create_loan(book_pk=detail_pk, loan_date=datetime.now())
            else:
                pk = loan_data[0]
            db.update_loan(pk=pk, values={"return_date": datetime.now()})
            db.update_book(detail_pk, values={"is_available": True})
        self.get_book_data()
