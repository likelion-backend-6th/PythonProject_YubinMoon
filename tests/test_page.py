from main import MainPage, BaseMenuPage, NewBooksPage, NewBooksWithUserInput


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
    assert result == "test"
    page.selected = 2
    result = page.run("enter")
    assert result == "test"
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
    assert page.data[0][0] == "ID"
    assert page.data[0][1] == "B001"

    page.run("enter")
    for c in "myTitle":
        page.run(c)
    assert page.selected_num == 1
    assert page.data[1][0] == "TITLE"
    assert page.data[1][1] == "myTitle"

    page.run("enter")
    for c in "myTitle":
        page.run(c)
    assert page.selected_num == 1
    assert page.data[1][0] == "TITLE"
    assert page.data[1][1] == "myTitle"
