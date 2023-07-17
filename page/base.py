from utils import RenderData

detail_pk = 0


class BasePage:
    def __init__(self):
        self.menu_list: list[list[str]] | None = None
        self.selected = None
        self.detail = ""

    def get_render_data(self) -> RenderData:
        return RenderData(
            menu_list=None,
            select_data=None,
            detail_data=self.detail,
        )

    def run(self, key: str) -> str | None:
        return "back"


class BaseMenuPage(BasePage):
    def __init__(self):
        super().__init__()
        self.menu_list: list[list[str]] = []
        self.selected = -1

    def get_render_data(self) -> RenderData:
        return RenderData(
            menu_list=[name for name, _ in self.menu_list],
            select_data=self.selected,
            detail_data=self.detail,
        )

    def run(self, key: str) -> str | None:
        key = key.lower()
        self.move_menu(key)
        if key == "h":
            return "help"
        elif key == "q":
            return "exit"
        elif key == "b":
            return "back"
        elif key == "enter":
            if self.selected is not None and 0 <= self.selected < len(self.menu_list):
                return self.menu_list[self.selected][1]

    def move_menu(self, key: str) -> None:
        key = key.lower()
        if key == "k":
            if self.selected is None:
                self.selected = 0
            elif 0 < self.selected:
                self.selected -= 1
            else:
                self.selected = len(self.menu_list) - 1
        elif key == "j":
            if self.selected is None:
                self.selected = 0
            elif self.selected < len(self.menu_list) - 1:
                self.selected += 1
            else:
                self.selected = 0
        elif key == "esc":
            self.selected = -1
