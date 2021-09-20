from tkinter import Tk, DISABLED
from typing import Dict

from .Container import Container
from .Form import Form
from .Logger import Logger


class View(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Syx")
        self._forms: Dict[str, Form] = {}
        self._create_widgets()

    def get_form_by_id(self, idd: str) -> Form:
        return self._forms[idd]

    def _create_widgets(self) -> None:
        menu: Container = Container(parent=self, label="Menu", rowspan=2)
        self._create_token_input_form(menu)
        self._create_grammar_input_form(menu)

        view: Container = Container(parent=self, label="View", column=1)
        self._create_analysis_table(view)

        logs: Container = Container(parent=self, label="Logger", row=1, column=1)
        self._logger = Logger(logs)
        return None


    def _create_project_form(self, parent: Container) -> None:
        idd: str = "regular_definition_input"
        new_form: Form = Form(parent=parent, label="Regular Definition Input")
        new_form.add_entry(idd="rd_entry", label="New Regex:")
        new_form.add_button(idd="rd_add", label="Add Regex", row=1, column=0)
        new_form.add_button(idd="rd_done", label="Done", row=1, column=1)
        self._forms[idd] = new_form
        return None

    def _create_token_input_form(self, parent: Container) -> None:
        idd: str = "token_input"
        new_form: Form = Form(parent=parent, label="Token Table Input", row=2)
        new_form.add_text_entry(idd=idd, height=13)
        new_form.add_button(idd=idd, label="Enter Token Table", row=1)
        self._forms[idd] = new_form
        return None

    def _create_analysis_table(self, parent: Container) -> None:
        idd: str = "analysis_table"
        new_form: Form = Form(parent=parent, label="Analysis Table", row=1)
        new_form.add_text_entry(idd=idd, state=DISABLED, width=60)
        self._forms[idd] = new_form
        return None

    def _create_grammar_input_form(self, parent: Container) -> None:
        idd: str = "grammar_input"
        new_form: Form = Form(parent=parent, label="Grammar Input", row=1)
        new_form.add_text_entry(idd=idd, height=6)
        new_form.add_button(idd=idd, label="Enter Grammar", row=1)
        self._forms[idd] = new_form
        return None

    def insert_text(self, idd: str, text: str) -> None:
        self._forms[idd].insert_text(idd, text)
        return None

    def clear_text(self, idd: str) -> None:
        self._forms[idd].clear_text(idd)
        return None

    def log_msg(self, msg: str) -> None:
        self._logger.log(msg)
        return None
