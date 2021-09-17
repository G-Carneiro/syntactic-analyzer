from typing import Tuple, Set, List
import os


def find_longest_common_prefix(productions: List[Tuple]) -> Tuple[str]:
    prefix: Tuple = tuple()
    maxsize: int = 0

    for i in range(len(productions) - 1):
        for j in range(i + 1, len(productions)):
            t = common_prefix_size(productions[i], productions[j])
            maxsize = max(maxsize, t)
            if maxsize == t:
                prefix = productions[i][:maxsize]

    return prefix


def common_prefix_size(prefix1: Tuple[str, ...], prefix2: Tuple[str, ...]) -> int:
    size: int = 0
    i: int = 0
    while i < min(len(prefix1), len(prefix2)):
        if prefix1[i] == prefix2[i]:
            size += 1
            i += 1
        else:
            break

    return size


def add_factored_transition(new_transitions: Set[Tuple[str, Tuple[str, ...]]],
                            production: Tuple[str, ...],
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


def get_new_body(production: Tuple[str, ...],
                 production_to_replace: Tuple[str, ...],
                 nt_to_replace: str
                 ) -> Tuple[str, ...]:
    production_list = list(production)
    production_to_replace_list = list(production_to_replace)
    index = production_to_replace.index(nt_to_replace)
    new_body: Tuple[str, ...] = tuple(production_list + production_to_replace_list[index + 1:])

    return new_body


def assemble_new_transition(non_terminal: str, longest_commom_prefix: Tuple[str, ...]) -> Tuple[Tuple[str, Tuple[str, ...]], str]:
    temp_list: List[str] = list(longest_commom_prefix)
    new_non_terminal: str = non_terminal + "'"
    temp_list.append(new_non_terminal)
    new_body: Tuple[str, ...] = tuple(temp_list)
    transition: Tuple[str, Tuple[str, ...]] = (non_terminal, new_body)

    return transition, new_non_terminal


def latex_analysis_table(non_terminals: Set[str], terminals: Set[str], analysis_table) -> None:
    latex_table: str = "\\begin{array}{|"
    latex_table += "c|" * (len(terminals) + 1) + "}\n\t"
    for terminal in sorted(terminals):
        latex_table += f"& {check_symbol(terminal)} "

    for non_terminal in sorted(non_terminals):
        latex_table += f"\\\\\n\t" \
                       f"\\hline \n\t" \
                       f"{check_symbol(non_terminal)}"
        for terminal in sorted(terminals):
            try:
                latex_table += f" & {check_symbol(analysis_table[non_terminal][terminal])}"
            except KeyError:
                latex_table += " &"

    latex_table += "\n\\end{array}"

    table_repr = open("../../docs/analysis_table.tex", "w")
    table_repr.write(latex_table)
    table_repr.close()

    os.system("latex ../../docs/main.tex")
    os.system("dvipdf main.dvi")
    os.remove("main.dvi")

    return None


def check_symbol(symbol: str) -> str:
    special_chars = ["#", "$", "%", "_", "{", "}", "&"]

    if symbol == "\\":
        return "\\backslash"
    elif symbol in special_chars:
        return ("\\" + symbol)

    return symbol
