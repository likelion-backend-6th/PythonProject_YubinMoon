from main import MainPage


def test_main_page_get_render_data():
    page = MainPage()
    render_data = page.get_render_data()
    menu_list = render_data.menu_list
    assert 0 < len(menu_list)
    for menu in menu_list:
        assert 0 < len(menu)
    assert render_data.select_data is None
    assert "WELCOME" in render_data.detail_data


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
    assert result == "도서 추가"
    page.selected = 1
    result = page.run("enter")
    assert result == "도서 조회"
    page.selected = 2
    result = page.run("enter")
    assert result == "대출 조회"
    page.selected = 3
    result = page.run("enter")
    assert result is None
    page.selected = -1
    result = page.run("enter")
    assert result is None
    page.selected = None
    result = page.run("enter")
    assert result is None
