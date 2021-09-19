from copy import copy
from typing import Dict, List, Set, Tuple, cast

from utils.utils import (
    latex_analysis_table,
    add_factored_transition,
    assemble_new_transition,
    find_longest_common_prefix,
    get_new_body,
)


class NonContextGrammar:
    def __init__(self, grammar_input: str) -> None:
        self._non_terminals: Set[str] = set()
        self._terminals: Set[str] = set()
        # transition = (non_terminal, sequence of symbols)
        self._transitions: Set[Tuple[str, Tuple[str, ...]]] = set()
        self._set_grammar(grammar_input)

    def convert_grammar(self) -> None:
        self._eliminate_left_recursion()
        self._left_factoring()
        self._set_first()
        self._set_follow()
        return None

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
            for symbol in sequence: symbols.add(symbol)

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

    def _left_factoring(self) -> None:
        self._replace_indirect_with_direct_non_determinism()
        self._remove_direct_non_determinism()
        return None

    def _replace_indirect_with_direct_non_determinism(self) -> None:
        productions_with_same_terminals: Dict[str, Set] = self._get_productions_with_same_terminals()

        for _, non_terminals in productions_with_same_terminals.items():
            for non_terminal in self._non_terminals:
                productions = self.get_all_productions_of_state(non_terminal)
                sum_ = 0
                for production in productions:
                    for nt in non_terminals:
                        if nt in production:
                            sum_ += 1
                    if sum_ >= 2:
                        for nt_to_replace in non_terminals:
                            self._replace_indirect_nd_transitions(non_terminal, nt_to_replace)

        return None

    def _get_productions_with_same_terminals(self) -> Dict[str, Set]:
        ways_to_get_to_terminal: Dict[str, Set] = {terminal: set() for terminal in self._terminals}

        for non_terminal in self._non_terminals:
            productions = self.get_all_productions_of_state(non_terminal)
            for production in productions:
                for symbol in production:
                    if symbol in self._terminals:
                        ways_to_get_to_terminal[symbol].add(non_terminal)

        return dict(filter(lambda item: len(item[1]) > 1, ways_to_get_to_terminal.items()))

    def _replace_indirect_nd_transitions(self, non_terminal: str, nt_to_replace: str) -> None:
        productions: List[Tuple[str]] = list(self.get_all_productions_of_state(nt_to_replace))
        productions_to_replace: List[Tuple[str]] = list(self.get_all_productions_of_state(non_terminal))

        for production in productions:
            for production_to_replace in productions_to_replace:
                if nt_to_replace in production_to_replace:
                    new_body: Tuple[str, ...] = get_new_body(production, production_to_replace, nt_to_replace)
                    new_transition: Tuple[str, Tuple[str, ...]] = (non_terminal, new_body)
                    self._transitions.add(new_transition)

                    removed_transition: Tuple[str, Tuple[str, ...]] = (non_terminal, tuple(production_to_replace))
                    if removed_transition in self._transitions:
                        self._transitions.remove(removed_transition)

        return None

    def _remove_direct_non_determinism(self) -> None:
        new_transitions: Set[Tuple[str, Tuple[str, ...]]] = set()
        new_non_terminals_to_add = set()

        for non_terminal in self._non_terminals:
            productions: List[Tuple[str]] = list(self.get_all_productions_of_state(non_terminal))
            longest_commom_prefix: Tuple[str] = find_longest_common_prefix(productions)

            if longest_commom_prefix:
                transition_to_add, non_terminal_to_add = assemble_new_transition(non_terminal, longest_commom_prefix)
                new_non_terminals_to_add.add(non_terminal_to_add)
                self._transitions.add(transition_to_add)
                self._replace_transitions(new_transitions, productions, longest_commom_prefix, non_terminal)

        for transition in new_transitions:
            transition = cast(Tuple[str, Tuple[str, ...]], transition)
            self._transitions.add(transition)

        for non_terminal in new_non_terminals_to_add:
            self._non_terminals.add(non_terminal)
        return None

    def _replace_transitions(self,
                             new_transitions: Set[Tuple[str, Tuple[str, ...]]],
                             productions: List[Tuple[str]],
                             prefix: Tuple[str, ...],
                             non_terminal: str
                             ) -> Set[Tuple[str, Tuple[str, ...]]]:
        for production in productions:
            if set(prefix).issubset(production):
                self._transitions.remove((non_terminal, production))
                new_transitions = add_factored_transition(new_transitions, production, prefix, non_terminal)

        return new_transitions

    def _set_first(self) -> None:
        self._first: Dict[str, Set[str]] = {non_terminal: set() for non_terminal in self._non_terminals}
        for non_terminal in self._non_terminals:
            self._set_first_of_non_terminal(non_terminal)

        return None

    def _set_first_of_non_terminal(self, non_terminal: str) -> None:
        if self._first[non_terminal]:
            return None
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
                    elif i == len(production) - 1:
                        self._first[non_terminal].add("&")

        return None

    def _get_first_of_non_terminal(self, non_terminal: str) -> Set[str]:
        if not self._first[non_terminal]:
            self._set_first_of_non_terminal(non_terminal)

        return self._first[non_terminal]

    def _set_follow(self) -> None:
        self._follow: Dict[str, Set[str]] = {non_terminal: set() for non_terminal in self._non_terminals}
        self._follow[self._initial_symbol].add("$")
        for non_terminal in sorted(self._non_terminals):
            self._set_follow_of_non_terminal(non_terminal)

        return None

    def _set_follow_of_non_terminal(self, non_terminal: str) -> None:
        if (non_terminal != self._initial_symbol) and (self._follow[non_terminal]):
            return None
        productions: Set[Tuple[str, Tuple[str, ...]]] = set()
        for production in self._transitions:
            if non_terminal in production[1]:
                productions.add(production)

        for production in productions:
            state: str = production[0]
            symbols: Tuple[str, ...] = production[1]
            for i in range(len(symbols)):
                actual_symbol = symbols[i]
                if actual_symbol == non_terminal:
                    if i == len(symbols) - 1:
                        if actual_symbol != state:
                            self._follow[actual_symbol] |= self._get_follow_of_non_terminal(state)
                    elif symbols[i + 1] in self._terminals:
                        self._follow[actual_symbol].add(symbols[i + 1])
                    else:
                        first_of_next_symbol = self._get_first_of_non_terminal(symbols[i + 1])
                        self._follow[actual_symbol] |= first_of_next_symbol - {"&"}
                        count = i + 1
                        while "&" in first_of_next_symbol and count <= len(symbols) - 2:
                            next_symbol = symbols[count + 1]
                            if next_symbol in self._terminals:
                                break
                            first_of_next_symbol = self._get_first_of_non_terminal(symbols[count + 1])
                            self._follow[actual_symbol] |= first_of_next_symbol - {"&"}
                            count += 1

                        if "&" in first_of_next_symbol:
                            self._follow[actual_symbol] |= self._get_follow_of_non_terminal(state)

        return None

    def _get_follow_of_non_terminal(self, non_terminal: str) -> Set[str]:
        if (non_terminal == self._initial_symbol) or (not self._follow[non_terminal]):
            self._set_follow_of_non_terminal(non_terminal)

        return self._follow[non_terminal]

    def construct_analysis_table(self) -> Dict[str, Dict[str, Tuple[str, Tuple[str, ...]]]]:
        productions = list(self._transitions)
        table = {non_terminal: {} for non_terminal in self._non_terminals}
        for production in productions:
            state = production[0]
            symbols = production[1]
            first_of_alpha: set = self._get_first_of_production(symbols)
            if "&" in first_of_alpha:
                follow_of_state = self._get_follow_of_non_terminal(state)
                for terminal in follow_of_state:
                    table[state][terminal] = symbols

                if "$" in follow_of_state:
                    table[state]["$"] = symbols

            first_of_alpha -= {"&"}

            for terminal in first_of_alpha:
                table[state][terminal] = symbols

        # TODO: remove
        # latex_analysis_table(self._non_terminals, self._terminals - {"&"} | {"$"}, table)

        return table

    def _get_first_of_production(self, production: Tuple) -> Set[str]:
        first = set()
        size = len(production)
        for i in range(size):
            symbol = production[i]
            if symbol in self._terminals:
                first.add(symbol)
                break

            first |= self._get_first_of_non_terminal(symbol)
            if ("&" in first) and (i < size - 1):
                first.remove("&")

        return first

    def __repr__(self) -> str:
        output: str = ""
        for state in sorted(self._non_terminals):
            output += f"{state} -> {self.get_all_productions_of_state(state)}\n"

        return output
