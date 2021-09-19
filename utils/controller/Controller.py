from typing import Dict

from ..view.View import View
from ..view.Form import Form

class Controller:
    def __init__(self) -> None:
        self._view = View()
        self._bind_callbacks()

    def run(self) -> None:
        self._view.mainloop()
        return None

    def _bind_callbacks(self) -> None:
        idd: str = "grammar_input"
        grammar_input: Form = self._view.get_form_by_id(idd)
        grammar_input.add_btn_callback(btn_id=idd, callback=self._handle_add_grammar_input_callback)

        idd: str = "token_input"
        token_table_input: Form = self._view.get_form_by_id(idd)
        token_table_input.add_btn_callback(btn_id=idd, callback=self._handle_add_token_input_callback)
        return None

    def _handle_add_grammar_input_callback(self, response: Dict) -> None:
        try:
            print(response)
        except:
            self._log("Algo deu errado ao adicionar a definição da gramática")
        else:
            print("else")
        return None

    def _handle_add_token_input_callback(self, response: Dict) -> None:
        try:
            print(response)
        except:
            self._log("Algo deu errado ao adicionar a tabela de tokens")
        else:
            print("else")
        return None

    def _log(self, message: str) -> None:
        self._view.log_msg(message)
        return None
