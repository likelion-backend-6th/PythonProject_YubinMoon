from __future__ import annotations


class RenderData:
    def __init__(
        self,
        menu_list: list[str] | None = None,
        select_data: int | None = None,
        detail_data: str = "",
    ):
        self.menu_list = menu_list
        self.select_data = select_data
        self.detail_data = detail_data

    def update(self, data: RenderData) -> None:
        if data.menu_list:
            self.menu_list = data.menu_list
        if data.select_data is not None:
            self.select_data = data.select_data
        if data.detail_data:
            self.detail_data = data.detail_data
        if self.select_data == -1:
            self.select_data = None
