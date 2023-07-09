from main import MainPage, Controller, NewBooksPage


def test_get_page(mocker):
    mocker.patch("main.Printer", return_value="test")
    controller = Controller()
    controller.get_page("main")
    assert isinstance(controller.page, MainPage)
    controller.get_page("new_books")
    assert isinstance(controller.page, NewBooksPage)


def test_handle_event(mocker):
    mocker.patch("main.Printer", return_value="test")
    mocker.patch("main.Controller.exit", return_value=None)
    mocker.patch("main.Controller.get_page", return_value=None)
    controller = Controller()
    controller.handle_event("test1")
    controller.get_page.assert_called_with("test1")
    assert controller.page_stack == ["main", "test1"]
    controller.handle_event("back")
    controller.get_page.assert_called_with("main")
    assert controller.page_stack == ["main"]
    controller.handle_event("back")
    assert controller.page_stack == ["main"]
    controller.handle_event("exit")
    controller.exit.assert_called_once()
