import unittest
from copy import copy

from utils.model.Grammar import NonContextGrammar


class NonContextGrammarTests(unittest.TestCase):
    def test_grammar_input(self) -> None:
        grammar_input: str = "P -> K V C \n" \
                             "K -> c K \n" \
                             "K -> & \n" \
                             "V -> v V \n" \
                             "V -> F \n" \
                             "F -> f P ; F \n" \
                             "F -> & \n" \
                             "C -> b V C e \n" \
                             "C -> com ; C \n" \
                             "C -> &"

        grammar = NonContextGrammar(grammar_input)
        non_terminals = {"P", "K", "V", "C", "F"}
        terminals = {"c", "v", "f", "com", ";", "b", "e", "&"}
        transitions = {("P", ("K", "V", "C")),
                       ("K", ("c", "K")),
                       ("K", tuple("&")),
                       ("V", ("v", "V")),
                       ("V", tuple("F")),
                       ("F", ("f", "P", ";", "F")),
                       ("F", tuple("&")),
                       ("C", ("b", "V", "C", "e")),
                       ("C", ("com", ";", "C")),
                       ("C", tuple("&"))
                       }
        self.assertEqual(non_terminals, grammar.get_non_terminals())
        self.assertEqual(terminals, grammar.get_terminals())
        self.assertEqual(transitions, grammar.get_transitions())

        return None

    # FIXME: Erro não determinístico ocorrendo
    @unittest.skip("")
    def test_left_recursion(self) -> None:
        grammar_input = "S -> S c \n" \
                        "S -> A a \n" \
                        "S -> c \n" \
                        "A -> S a \n" \
                        "A -> B b \n" \
                        "A -> a \n" \
                        "B -> S c \n" \
                        "B -> B b"

        grammar = NonContextGrammar(grammar_input)
        expected_productions = {("S", ("A", "a", "S'")),
                                ("S", ("c", "S'")),
                                ("S'", tuple("&")),
                                ("S'", ("c", "S'")),
                                ("A", ("B", "b", "A'")),
                                ("A", ("a", "A'")),
                                ("A", ("c", "S'", "a", "A'")),
                                ("A'", ("a", "S'", "a", "A'")),
                                ("A'", tuple("&")),
                                ("B", ("c", "S'", "c", "B'")),
                                ("B", ("a", "A'", "a", "S'", "c", "B'")),
                                ("B", ("c", "S'", "a", "A'", "a", "S'", "c", "B'")),
                                ("B'", ("b", "B'")),
                                ("B'", ("b", "A'", "a", "S'", "c", "B'")),
                                ("B'", tuple("&"))
                                }
        expected_productions = {("A", ("S", "a")),
                                ("A", ("B", "b")),
                                ("A", tuple("a")),
                                ("B", ("S", "c", "B'")),
                                ("B'", ("b", "B'")),
                                ("B'", tuple("&")),
                                ("S", ("a", "a", "S'")),
                                ("S", ("c", "S'")),
                                ("S'", ("c", "S'")),
                                ("S'", ("a", "a", "S'")),
                                ("S'", ("c", "B'", "b", "a", "S'")),
                                ("S'", tuple("&"))
                                }
        for _ in range(10000):
            aux_grammar = copy(grammar)
            aux_grammar._eliminate_left_recursion()
            self.assertEqual(aux_grammar.get_transitions(), expected_productions)

        return None

    def test_first(self) -> None:
        grammar_input = "S -> A B \n"\
                        "A -> a B A \n"\
                        "A -> & \n"\
                        "B -> C D \n"\
                        "C -> b D C \n"\
                        "C -> & \n"\
                        "D -> c S c \n"\
                        "D -> d"
        grammar = NonContextGrammar(grammar_input)
        expected_first = {"S": {"a", "b", "c", "d"},
                          "A": {"a", "&"},
                          "B": {"b", "c", "d"},
                          "C": {"b", "&"},
                          "D": {"c", "d"}}
        self.assertEqual(grammar.get_first(), expected_first)

        return None

    @unittest.skip("Method not ready for testing")
    def test_left_factoring(self) -> None:
        grammar_input = "S -> i E t S \n"\
                        "S -> i E t S e S \n"\
                        "S -> a \n"\
                        "E -> b"
        grammar = NonContextGrammar(grammar_input)
        expected = {
            ("E", tuple("b")),
            ("S", ("i", "E", "t", "S", "S'")),
            ("S'", ("e", "S", "&"))
        }
        grammar._left_factoring()
        actual = grammar.get_transitions()
        self.assertEqual(actual, expected)
        return None

    def test_find_longest_prefix(self) -> None:
        grammar_input = "S -> i E t S \n"\
                        "S -> i E t S e S \n"\
                        "S -> a \n"\
                        "E -> b"
        production = [('a',), ('i', 'E', 't', 'S', 'e', 'S'), ('i', 'E', 't', 'S')]
        grammar = NonContextGrammar(grammar_input)

        expected = ('i', 'E', 't', 'S')
        actual = grammar._find_longest_common_prefix(production)
        self.assertEqual(expected, actual)

        production = [
            ('f', 'o', 'o'),
            ('f', 'o', 'o', 'b', 'a', 'r'),
            ('f', 'o', 'o', 't', 'b', 'a', 'l', 'l'),
            ('f', 'o', 'o', 't', 'b', 'a', 'g'),
            ('b', 'a', 'r'),
        ]

        expected = ('f', 'o', 'o', 't', 'b', 'a')
        actual = grammar._find_longest_common_prefix(production)
        self.assertEqual(expected, actual)
        return None
