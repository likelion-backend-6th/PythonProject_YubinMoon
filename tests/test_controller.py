from main import MainPage, Controller


def test_get_page(mocker):
    mocker.patch("main.Printer", return_value="test")
    controller = Controller()
    menu = controller.get_page("main")
    assert isinstance(menu, MainPage)
