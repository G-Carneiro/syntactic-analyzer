from typing import Set, List, Tuple


class NonContextGrammar:
    def __init__(self, grammar_input: str) -> None:
        self._non_terminals: Set[str] = set()
        self._terminals: Set[str] = set()
        # transition = (non_terminal, sequence of symbols)
        self._transitions: Set[Tuple[str, List[str]]] = set()
        self._set_grammar(grammar_input)

    def _set_grammar(self, grammar_input: str) -> None:
        symbols: Set[str] = set()
        for line in grammar_input.split("\n"):
            sequence: List[str] = line.split()
            non_terminal: str = sequence[0]
            del sequence[:2]
            self._non_terminals.add(non_terminal)
            transition = (non_terminal, sequence)
            self._transitions.add(transition)
            for symbol in sequence:
                symbols.add(symbol)

        self._terminals = symbols - self._non_terminals

        return None




