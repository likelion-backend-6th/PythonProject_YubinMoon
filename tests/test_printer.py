from main import RenderData, Printer
import os


class TestClass:
    columns = 50
    lines = 30


def test_print(mocker):
    test = TestClass()
    mocker.patch("os.get_terminal_size", return_value=TestClass)
    printer = Printer()
    render_data = RenderData(
        menu_list=["abc", "ccc", "bdc"], select_data=3, detail_data="testDetail"
    )
    result = printer.render(render_data)
    assert "abc" in result
    assert "ccc" in result
    assert "bdc" in result
    assert "testDetail" in result
    assert ">" in result

    data_list = result.split("\n")
    assert len(data_list) == test.lines
    for data in data_list:
        assert len(data) <= test.columns

    num_list = [d.find("||") for d in data_list]
    assert len(set(num_list))


def test_print_no_select(mocker):
    test = TestClass()
    mocker.patch("os.get_terminal_size", return_value=TestClass)
    printer = Printer()
    render_data = RenderData(menu_list=["abc", "ccc", "bdc"], detail_data="testDetail")
    result = printer.render(render_data)
    assert "abc" in result
    assert "ccc" in result
    assert "bdc" in result
    assert "testDetail" in result
    assert ">" not in result

    data_list = result.split("\n")
    assert len(data_list) == test.lines
    for data in data_list:
        assert len(data) <= test.columns

    num_list = [d.find("||") for d in data_list]
    assert len(set(num_list))
