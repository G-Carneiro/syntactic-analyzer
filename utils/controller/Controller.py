from ..view.View import View

class Controller:
    def __init__(self) -> None:
        self._view = View()

    def run(self) -> None:
        self._view.mainloop()
        return None
