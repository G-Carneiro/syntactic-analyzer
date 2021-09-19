from typing import Dict

from ..view.View import View
from ..view.Form import Form

from ..model.Grammar import NonContextGrammar
from ..model.PushdownAutomata import PushDownAutomata

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
            grammar_input: str = response["text_entries"]["grammar_input"][0:-1]
            self.grammar = NonContextGrammar(grammar_input)
        except:
            self._log("Algo deu errado ao adicionar a definição da gramática")
        else:
            self.grammar.convert_grammar()
            table: Dict = self.grammar.construct_analysis_table()
            self._view.insert_text(idd="analysis_table", text=str(table))
            initial_state: str = self.grammar.get_initial_state()
            self.pd_automata: PushDownAutomata = PushDownAutomata(initial_state, table)
            self._log("Gramática Criada Com Sucesso")
        return None

    def _handle_add_token_input_callback(self, response: Dict) -> None:
        try:
            token_table = list(response["text_entries"]["token_input"])[:-1]
            # ["a", " ", "b", "\n"]
            print(token_table)
        except:
            self._log("Algo deu errado ao adicionar a tabela de tokens")
        else:
            is_accepted: bool = self.pd_automata.run(token_table)
            if is_accepted:
                self._log("Aceito")
            else:
                self._log("Não aceito")
        return None

    def _log(self, message: str) -> None:
        self._view.log_msg(message)
        return None
