from typing import Set, List, Tuple


class NonContextGrammar:
    def __init__(self, grammar_input: str) -> None:
        self._non_terminals: Set[str] = set()
        self._terminals: Set[str] = set()
        # transition = (non_terminal, sequence of symbols)
        self._transitions: Set[Tuple[str, Tuple[str]]] = set()
        self._set_grammar(grammar_input)

    def _set_grammar(self, grammar_input: str) -> None:
        symbols: Set[str] = set()
        for line in grammar_input.split("\n"):
            sequence: List[str] = line.split()
            non_terminal: str = sequence[0]
            del sequence[:2]
            self._non_terminals.add(non_terminal)
            transition = (non_terminal, tuple(sequence))
            self._transitions.add(transition)
            for symbol in sequence:
                symbols.add(symbol)

        self._terminals = symbols - self._non_terminals

        return None

    def get_terminals(self) -> Set[str]:
        return self._terminals

    def get_non_terminals(self) -> Set[str]:
        return self._non_terminals

    def get_transitions(self) -> Set[Tuple[str, Tuple[str]]]:
        return self._transitions

    def _eliminate_left_recursion(self) -> None:
        non_terminals: List[str] = list(self._non_terminals)
        for i in range(len(non_terminals)):
            for j in range(i - 1):
                for transition in self._transitions:
                    if (non_terminals[i] == transition[0]) \
                            and (non_terminals[j] == transition[1][0]):
                        pass
