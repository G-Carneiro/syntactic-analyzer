from typing import Set, Tuple, List, Dict


class PushDownAutomata:
    def __init__(self,
                 initial_state: str,
                 analysis_table: Dict[str, Dict[str, Tuple[str, ...]]]) -> None:
        self._states: Set[str] = set(analysis_table.keys())
        self._initial_state: str = initial_state
        self._stack: List[str] = ["$", initial_state]
        self._analysis_table: Dict[str, Dict[str, Tuple[str, ...]]] = analysis_table

    def run(self, sentence: List[str]) -> bool:
        sentence.append("$")
        for symbol in sentence:
            top = self.top_of_stack()
            if (top == "$" == symbol):
                return True
            elif top == symbol:
                self._stack.pop()
            elif top in self._states:
                try:
                    production = self._analysis_table[top][symbol]
                    self._stack.pop()
                    for element in reversed(production):
                        if element == "&":
                            break
                        self._stack.append(element)

                except KeyError:
                    return False

        return False

    def top_of_stack(self) -> str:
        return self._stack[-1]
