from main import MainPage


def test_menu_page():
    page = MainPage()
    render_data = page.get_render_data()
    menu_list = render_data.menu_list
    assert 0 < len(menu_list)
    for menu in menu_list:
        assert 0 < len(menu)
    assert render_data.select_data is None
    assert "WELCOME" in render_data.detail_data

    run_result = page.run("test")
    assert run_result == "test"
