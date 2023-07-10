from main import MainPage, Controller, NewBooksPage


def test_get_page(mocker):
    mocker.patch("main.Printer", return_value="test")
    controller = Controller()
    controller.change_page("main")
    assert isinstance(controller.page_stack[-1], MainPage)
    controller.change_page("new_books")
    assert isinstance(controller.page_stack[-1], NewBooksPage)


def test_handle_event(mocker):
    mocker.patch("main.Printer", return_value="test")
    mocker.patch("main.Controller.exit", return_value=None)
    mocker.patch("main.Controller.get_page_by_name", return_value="test")
    controller = Controller()
    controller.handle_event("test1")
    assert len(controller.page_stack) == 2
    controller.handle_event("back")
    assert len(controller.page_stack) == 1
    controller.handle_event("back")
    assert len(controller.page_stack) == 1
    controller.handle_event("exit")
    controller.exit.assert_called_once()
