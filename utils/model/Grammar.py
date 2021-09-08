from typing import Set, List, Tuple
from copy import copy


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
        non_terminals: List[str] = list(sorted(self._non_terminals))
        for i in range(len(non_terminals)):
            for j in range(i):
                transitions = copy(self._transitions)
                for transition in transitions:
                    if (non_terminals[i] == transition[0]) \
                            and (non_terminals[j] == transition[1][0]):
                        self._transitions.remove(transition)
                        alpha = list(transition[1][1:])
                        productions = self.get_all_productions_of_state(non_terminals[j])
                        for production in productions:
                            self._transitions.add((non_terminals[i], tuple(list(production) + alpha)))

            self._eliminate_immediate_left_recursion(non_terminals[i])

        return None

    def _eliminate_immediate_left_recursion(self, state: str) -> None:
        if self.have_immediate_left_recursion(state):
            new_state: str = state + "\'"
            self._non_terminals.add(new_state)
            epsilon_production = (new_state, tuple("&"))
            self._transitions.add(epsilon_production)
            transitions = copy(self._transitions)
            for transition in transitions:
                if transition[0] == state:
                    self._transitions.remove(transition)
                    if transition[1][0] == state:
                        new_production = (new_state, tuple(list(transition[1][1:]) + [new_state]))
                    else:
                        new_production = (state, tuple(list(transition[1]) + [new_state]))

                    self._transitions.add(new_production)

        return None

    def have_immediate_left_recursion(self, state: str) -> bool:
        for transition in self._transitions:
            if (transition[0] == state) and (transition[1][0] == state):
                return True

        return False

    def get_all_productions_of_state(self, state: str) -> Set[Tuple[str]]:
        all_productions = set()
        for transition in self._transitions:
            if transition[0] == state:
                all_productions.add(tuple(transition[1]))

        return all_productions

    def _left_factoring(self) -> None:
        return None

    def __repr__(self) -> str:
        output: str = ""
        for state in sorted(self._non_terminals):
            output += f"{state} -> {self.get_all_productions_of_state(state)}\n"

        return output
