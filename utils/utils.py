from typing import Tuple, Set, List, Dict
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
                            new_non_terminal: str
                        ) -> Set[Tuple[str, Tuple[str, ...]]]:
    new_transition: List = list()
    prefix_size: int = len(prefix)
    new_production: Tuple[str, ...] = production[prefix_size:] if len(production[prefix_size:]) > 1 \
                                                                else tuple(production[prefix_size:])
    if not(new_production):
        new_production = tuple("&")

    new_transition.append(new_non_terminal)
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


def assemble_new_transition(non_terminal: str, longest_commom_prefix: Tuple[str, ...], new_non_terminal: str) -> Tuple[str, Tuple[str, ...]]:
    temp_list: List[str] = list(longest_commom_prefix)
    temp_list.append(new_non_terminal)
    new_body: Tuple[str, ...] = tuple(temp_list)
    transition: Tuple[str, Tuple[str, ...]] = (non_terminal, new_body)

    return transition


def latex_analysis_table(non_terminals: Set[str], terminals: Set[str], analysis_table) -> None:
    latex_table: str = "$\n" \
                       "\\begin{array}{|"
    latex_table += "c|" * (len(terminals) + 1) + "}\n\t"
    latex_table += "\\hline \n\t"
    for terminal in sorted(terminals):
        latex_table += f"& {check_symbol(terminal)} "

    latex_table += "\\\\"

    for non_terminal in sorted(non_terminals):
        latex_table += f"\n\t" \
                       f"\\hline \n\t" \
                       f"{check_symbol(non_terminal)}"
        for terminal in sorted(terminals):
            try:
                string = analysis_table[non_terminal][terminal]
                latex_table += f" & {check_str(string)}"
            except KeyError:
                latex_table += " &"

        latex_table += " \\\\"

    latex_table += "\n\t\\hline" \
                   "\n\\end{array}\n" \
                   "$"

    table_repr = open("docs/analysis_table.tex", "w")
    table_repr.write(latex_table)
    table_repr.close()

    os.system("latex docs/main.tex")
    os.system("dvipdf main.dvi")
    os.remove("main.dvi")

    return None


def check_symbol(symbol: str) -> str:
    special_chars = ["#", "$", "%", "_", "{", "}"]

    if symbol == "\\":
        return "\\backslash"
    elif symbol == "&":
        return "\\varepsilon "
    elif symbol in special_chars:
        return ("\\" + symbol)

    return symbol


def check_str(string: str) -> str:
    output = ""
    for symbol in string:
        output += check_symbol(symbol)

    return output


def tuple_to_str(production: tuple) -> str:
    output = ""
    for symbol in production:
        output += str(symbol)

    return output

def should_replace(productions, non_terminals) -> bool:
    sum_ = 0
    for production in sorted(productions):
        if production[0] in non_terminals:
            sum_ += 1

    if sum_ > 1:
        return True
    else:
        return False

def table_to_str(table: Dict[str, Dict[str, Tuple[str, ...]]],
                 non_terminals: Set[str],
                 terminals: Set[str]) -> str:
    terminals -= {"&"}
    terminals.add("$")
    output: str = ""
    for non_terminal in sorted(non_terminals):
        for terminal in sorted(terminals):
            try:
                production: str = tuple_to_str(table[non_terminal][terminal])
                output += f"M[{non_terminal}][{terminal}] = {production} \n"
            except KeyError:
                pass

    return output
