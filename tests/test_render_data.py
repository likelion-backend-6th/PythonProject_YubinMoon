import pytest
from main import RenderData


def test_make_instance_with_no_data():
    render_data = RenderData()
    assert render_data.menu_list == None
    assert render_data.select_data == None
    assert render_data.detail_data == ""


def test_make_instance_with_menu_list():
    render_data = RenderData(menu_list=["a", "b", "c"])
    assert render_data.menu_list == ["a", "b", "c"]
    assert render_data.select_data == None
    assert render_data.detail_data == ""


def test_make_instance_with_select_data():
    render_data = RenderData(select_data=1)
    assert render_data.menu_list == None
    assert render_data.select_data == 1
    assert render_data.detail_data == ""


def test_make_instance_with_detail_data():
    render_data = RenderData(detail_data="detail")
    assert render_data.menu_list == None
    assert render_data.select_data == None
    assert render_data.detail_data == "detail"


def test_make_instance_with_all_data1():
    render_data = RenderData(
        menu_list=["a", "b", "c"], select_data=1, detail_data="detail"
    )
    assert render_data.menu_list == ["a", "b", "c"]
    assert render_data.select_data == 1
    assert render_data.detail_data == "detail"


def test_make_instance_with_all_data2():
    render_data = RenderData(menu_list=[], select_data=-1, detail_data="detail\ndetail")
    assert render_data.menu_list == []
    assert render_data.select_data == -1
    assert render_data.detail_data == "detail\ndetail"


def test_data_update1():
    render_data1 = RenderData(
        menu_list=["a", "b", "c"], select_data=2, detail_data="detail"
    )
    render_data2 = RenderData(
        menu_list=["abc", "ccc"], select_data=3, detail_data="submenu"
    )
    render_data1.update(render_data2)
    assert render_data1.menu_list == ["abc", "ccc"]
    assert render_data1.select_data == 3
    assert render_data1.detail_data == "submenu"


def test_data_update2():
    render_data1 = RenderData(
        menu_list=["a", "b", "c"], select_data=2, detail_data="detail"
    )
    render_data2 = RenderData(select_data=-1, detail_data="submenu")
    render_data1.update(render_data2)
    assert render_data1.menu_list == ["a", "b", "c"]
    assert render_data1.select_data == None
    assert render_data1.detail_data == "submenu"


def test_data_update3():
    render_data1 = RenderData(
        menu_list=["a", "b", "c"], select_data=2, detail_data="detail"
    )
    render_data2 = RenderData()
    render_data1.update(render_data2)
    assert render_data1.menu_list == ["a", "b", "c"]
    assert render_data1.select_data == 2
    assert render_data1.detail_data == "detail"
