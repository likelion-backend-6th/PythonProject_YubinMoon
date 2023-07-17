from utils import RenderData
from .base import BasePage
import database as db
from .base import detail_pk


class LoanHistoryPage(BasePage):
    def __init__(self):
        super().__init__()
        self.base_detail = "대출 기록"
        self.offset = 0
        self.book_count = db.loan_count_by_book_pk(detail_pk)

    def get_render_data(self) -> RenderData:
        self.detail = self.base_detail
        self.detail += "\n\n"
        self.detail += self.get_loan_table()
        return super().get_render_data()

    def get_loan_table(self) -> str:
        global detail_pk
        result = ""
        loan_list = db.read_loans_by_book_pk(
            book_pk=detail_pk, offset=self.offset, limit=20
        )
        for loan in loan_list:
            if loan[3]:
                result += f"\n반납: {loan[3]}"
            result += f"\n대출: {loan[2]}"
        return result

    def run(self, key: str) -> str | None:
        key = key.lower()
        if key == "k":
            if 0 < self.offset:
                self.offset -= 1
        elif key == "j":
            if self.offset < self.book_count - 5:
                self.offset += 1
        elif key == "esc" or key == "b" or key == "q" or key == "enter":
            return "back"


class AllLoanHistoryPage(BasePage):
    def __init__(self):
        super().__init__()
        self.base_detail = "전체 대출 기록"
        self.offset = 0
        self.book_count = db.all_history_count()

    def get_render_data(self) -> RenderData:
        self.detail = self.base_detail
        self.detail += "\n\n"
        self.detail += "---ID---|---Title---|---Author---|---Publisher---|---Loan Date---|---Return Date---"
        self.detail += self.get_loan_table()
        return super().get_render_data()

    def get_loan_table(self) -> str:
        result = ""
        loan_list = db.all_loan_history(offset=self.offset, limit=20)
        for loan in loan_list:
            text = f"\n{loan[0]} | {loan[1]} | {loan[2]} | {loan[3]} | {loan[4]} "
            if loan[5]:
                text += f"| {loan[5]}"
            else:
                text += "| 대출 중..."
            result += text
        return result

    def run(self, key: str) -> str | None:
        key = key.lower()
        if key == "k":
            if 0 < self.offset:
                self.offset -= 1
        elif key == "j":
            if self.offset < self.book_count - 5:
                self.offset += 1
        elif key == "esc" or key == "b" or key == "q" or key == "enter":
            return "back"
