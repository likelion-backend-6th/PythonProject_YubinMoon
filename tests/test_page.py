import setting

setting.DB_NAME = "test_library"
from page import (
    MainPage,
    BaseMenuPage,
    NewBooksPage,
    NewBooksWithUserInput,
    NewBooksWithUserInputCheck,
    NewBooksWithUserInputDone,
    NewBooksWithFileInput,
    BooksListPage,
    BookDetailPage,
)


def test_main_page_get_render_data():
    page = MainPage()
    render_data = page.get_render_data()
    assert render_data.menu_list == ["도서 추가", "도서 조회", "대출 조회"]
    assert render_data.select_data is -1
    assert len(render_data.detail_data)


def test_main_page_run():
    page = MainPage()
    page.selected = None
    page.run("k")
    assert page.selected == 0
    page.run("K")
    assert page.selected == 2
    page.run("k")
    assert page.selected == 1

    page.selected = None
    page.run("j")
    assert page.selected == 0
    page.run("J")
    assert page.selected == 1
    page.run("j")
    assert page.selected == 2
    page.run("j")
    assert page.selected == 0
    page.run("esc")
    assert page.selected is -1

    result = page.run("h")
    assert result == "help"
    result = page.run("q")
    assert result == "exit"


def test_main_page_menu():
    page = MainPage()
    page.selected = 0
    result = page.run("enter")
    assert result == "new_books"
    page.selected = 1
    result = page.run("enter")
    assert result == "inquire_all_books"
    page.selected = 2
    result = page.run("enter")
    assert result == "all_loan_history"
    page.selected = 3
    result = page.run("enter")
    assert result is None
    page.selected = -1
    result = page.run("enter")
    assert result is None
    page.selected = None
    result = page.run("enter")
    assert result is None


def test_new_books_page_get_render_data():
    page = NewBooksPage()
    render_data = page.get_render_data()
    menu_list = render_data.menu_list
    assert menu_list == ["직접 입력", "파일 입력"]
    assert render_data.select_data is -1
    assert len(render_data.detail_data)


def test_new_books_page_run():
    page = NewBooksPage()
    page.selected = None
    page.run("k")
    assert page.selected == 0
    page.run("K")
    assert page.selected == 1
    page.run("k")
    assert page.selected == 0

    page.selected = None
    page.run("j")
    assert page.selected == 0
    page.run("J")
    assert page.selected == 1
    page.run("j")
    assert page.selected == 0
    page.run("j")
    assert page.selected == 1
    page.run("esc")
    assert page.selected is -1


def test_new_books_page_menu():
    page = NewBooksPage()
    page.selected = 0
    result = page.run("enter")
    assert result == "new_book_with_user_input"
    page.selected = 1
    result = page.run("enter")
    assert result == "new_book_with_file_input"
    page.selected = 2
    result = page.run("enter")
    assert result is None
    page.selected = -1
    result = page.run("enter")
    assert result is None
    page.selected = None
    result = page.run("enter")
    assert result is None


def test_new_books_with_user_input_get_render_data():
    page = NewBooksWithUserInput()
    render_data = page.get_render_data()
    assert render_data.menu_list is None
    assert render_data.select_data is None
    assert len(render_data.detail_data)


def test_new_books_with_user_input_run():
    page = NewBooksWithUserInput()
    for c in "B001":
        page.run(c)
    assert page.selected_num == 0
    assert NewBooksWithUserInput.data[0][0] == "ID"
    assert NewBooksWithUserInput.data[0][1] == "B001"

    page.run("enter")
    for c in "myTitle":
        page.run(c)
    assert page.selected_num == 1
    assert NewBooksWithUserInput.data[1][0] == "TITLE"
    assert NewBooksWithUserInput.data[1][1] == "myTitle"

    page.run("enter")
    for c in "lime":
        page.run(c)
    assert page.selected_num == 2
    assert NewBooksWithUserInput.data[2][0] == "AUTHOR"
    assert NewBooksWithUserInput.data[2][1] == "lime"

    page.run("enter")
    for c in "pub":
        page.run(c)
    assert page.selected_num == 3
    assert NewBooksWithUserInput.data[3][0] == "PUB"
    assert NewBooksWithUserInput.data[3][1] == "pub"


def test_new_books_with_user_input_check_get_render_data():
    page = NewBooksWithUserInputCheck()
    render_data = page.get_render_data()
    assert render_data.menu_list is None
    assert render_data.select_data is None
    assert len(render_data.detail_data)


def test_new_books_with_user_input_check_run():
    page = NewBooksWithUserInputCheck()
    result = page.run("esc")
    assert result == "back"

    assert page.user_selected == "Y"
    NewBooksWithUserInput.data[0][1] = "A001"
    page.run("l")
    assert page.user_selected == "N"
    result = page.run("enter")
    assert result == "back"
    page.run("h")
    assert page.user_selected == "Y"
    NewBooksWithUserInput.data[0][1] = "A002"
    result = page.run("enter")
    assert result == "new_book_with_user_input_done"


def test_new_books_with_user_input_done_get_render_data():
    page = NewBooksWithUserInputDone()
    render_data = page.get_render_data()
    assert render_data.menu_list is None
    assert render_data.select_data is None
    assert len(render_data.detail_data)


def test_new_books_with_user_input_done_run():
    page = NewBooksWithUserInputDone()
    result = page.run("h")
    assert result == "new_books"


def test_new_books_with_file_input_get_render_data():
    page = NewBooksWithFileInput()
    page.file_list = []
    render_data = page.get_render_data()
    assert render_data.menu_list is None
    assert render_data.select_data is None
    assert ["도서 파일 선택"] in render_data.detail_data

    page.file_list = ["input/test.csv", "input/test.json"]
    render_data = page.get_render_data()
    assert render_data.menu_list is None
    assert render_data.select_data is None
    assert ["test.csv <"] in render_data.detail_data
    assert ["test.json"] in render_data.detail_data


def test_new_books_with_file_input_run():
    page = NewBooksWithFileInput()
    page.file_list = []
    page.selected_num = 0
    page.run("k")
    assert page.selected_num == -1
    page.run("j")
    assert page.selected_num == 0
    page.run("k")
    assert page.selected_num == -1
    page.run("J")
    assert page.selected_num == 0
    page.run("J")
    assert page.selected_num == 0

    page.file_list = ["test.csv", "test.json"]
    page.selected_num = 0
    page.run("j")
    assert page.selected_num == 1
    page.run("J")
    assert page.selected_num == 0
    page.run("k")
    assert page.selected_num == 1
    page.run("K")
    assert page.selected_num == 0


def test_book_list_page_get_render_data():
    page = BookDetailPage()
    pass


def test_book_detail_page_run():
    page = BookDetailPage()
    pass
