from typing import Set, List, Tuple, Dict, cast
from copy import copy


class NonContextGrammar:
    def __init__(self, grammar_input: str) -> None:
        self._non_terminals: Set[str] = set()
        self._terminals: Set[str] = set()
        # transition = (non_terminal, sequence of symbols)
        self._transitions: Set[Tuple[str, Tuple[str, ...]]] = set()
        self._set_grammar(grammar_input)
        self._set_first()
        self._set_follow()

    def _set_grammar(self, grammar_input: str) -> None:
        symbols: Set[str] = set()
        self._initial_symbol: str = grammar_input[0]
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

    def get_transitions(self) -> Set[Tuple[str, Tuple[str, ...]]]:
        return self._transitions

    def get_first(self) -> Dict[str, Set[str]]:
        return self._first

    def get_follow(self) -> Dict[str, Set[str]]:
        return self._follow

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

    def _add_new_transition(self, non_terminal: str, longest_commom_prefix: Tuple[str, ...]) -> None:
        temp_list: List[str] = list(longest_commom_prefix)
        temp_list.append(non_terminal + "'")
        new_body: Tuple[str, ...] = tuple(temp_list)
        transition: Tuple[str, Tuple[str, ...]] = (non_terminal, new_body)
        self._transitions.add(transition)

        return None

    def _add_factored_transition(self,
                                new_transitions: Set[Tuple[str, Tuple[str, ...]]],
                                production: Tuple[str],
                                prefix: Tuple[str, ...],
                                non_terminal: str
                            ) -> Set[Tuple[str, Tuple[str, ...]]]:
        new_transition: List = list()
        prefix_size: int = len(prefix)
        new_production: Tuple[str, ...] = production[prefix_size:] if len(production[prefix_size:]) > 1 \
                                                                    else tuple(production[prefix_size:])
        if not(new_production):
            new_production = tuple("&")

        new_transition.append(non_terminal + "'")
        new_transition.append(new_production)
        new_transition_tuple: Tuple = tuple(new_transition)
        new_transitions.add(new_transition_tuple)

        return new_transitions

    def _replace_transitions(self,
                            new_transitions: Set[Tuple[str, Tuple[str, ...]]],
                            productions: List[Tuple[str]], 
                            prefix: Tuple[str, ...], 
                            non_terminal: str
                        ) -> Set[Tuple[str, Tuple[str, ...]]]:
        for production in productions:
            if set(prefix).issubset(production):
                self._transitions.remove((non_terminal, production))
                new_transitions = self._add_factored_transition(new_transitions, production, prefix, non_terminal)

        return new_transitions

    def _left_factoring(self) -> None:
        new_transitions: Set[Tuple[str, Tuple[str, ...]]] = set()

        for non_terminal in self._non_terminals:
            productions: List[Tuple[str]] = list(self.get_all_productions_of_state(non_terminal))
            longest_commom_prefix: Tuple[str] = self._find_longest_common_prefix(productions)

            if longest_commom_prefix:
                self._add_new_transition(non_terminal, longest_commom_prefix)
                self._replace_transitions(new_transitions, productions, longest_commom_prefix, non_terminal)

        for transition in new_transitions:
            transition = cast(Tuple[str, Tuple[str, ...]], transition)
            self._transitions.add(transition)

        return None

    def _common_prefix_size(self, prefix1: Tuple[str, ...], prefix2: Tuple[str, ...]) -> int:
        size: int = 0
        i: int = 0
        while i < min(len(prefix1), len(prefix2)):
            if prefix1[i] == prefix2[i]:
                size += 1
                i += 1
            else:
                break

        return size

    def _find_longest_common_prefix(self, productions: List[Tuple]) -> Tuple[str]:
        prefix: Tuple = tuple()
        maxsize: int = 0

        for i in range(len(productions) - 1):
            for j in range(i + 1, len(productions)):
                t = self._common_prefix_size(productions[i], productions[j])
                maxsize = max(maxsize, t)
                if maxsize == t:
                    prefix = productions[i][:maxsize]

        return prefix

    def _set_first(self) -> None:
        self._first: Dict[str, Set[str]] = {non_terminal: set() for non_terminal in self._non_terminals}
        for non_terminal in self._non_terminals:
            self._set_first_of_non_terminal(non_terminal)

        return None

    def _set_first_of_non_terminal(self, non_terminal: str) -> None:
        productions = self.get_all_productions_of_state(non_terminal)
        for production in productions:
            actual_symbol_of_production = production[0]
            if actual_symbol_of_production in self._terminals:
                self._first[non_terminal].add(actual_symbol_of_production)
            elif actual_symbol_of_production == "&":
                self._first[non_terminal].add("&")
            else:
                for i in range(len(production)):
                    if production[i] in self._terminals:
                        self._first[non_terminal].add(production[i])
                        break

                    first_of_symbol: Set[str] = self._get_first_of_non_terminal(production[i])
                    self._first[non_terminal] |= first_of_symbol - {"&"}
                    if "&" not in first_of_symbol:
                        break
                    elif i == len(production):
                        self._first[non_terminal].add("&")

        return None

    def _get_first_of_non_terminal(self, non_terminal: str) -> Set[str]:
        if not self._first[non_terminal]:
            self._set_first_of_non_terminal(non_terminal)

        return self._first[non_terminal]

    def _set_follow(self) -> None:
        self._follow: Dict[str, Set[str]] = {non_terminal: set() for non_terminal in self._non_terminals}
        self._follow[self._initial_symbol].add("$")
        for non_terminal in self._non_terminals:
            self._set_follow_of_non_terminal(non_terminal)

        return None

    def _set_follow_of_non_terminal(self, non_terminal: str) -> None:
        return None

    def __repr__(self) -> str:
        output: str = ""
        for state in sorted(self._non_terminals):
            output += f"{state} -> {self.get_all_productions_of_state(state)}\n"

        return output
