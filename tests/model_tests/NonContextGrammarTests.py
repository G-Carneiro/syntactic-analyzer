import unittest
from copy import copy

from utils.model.Grammar import NonContextGrammar


class NonContextGrammarTests(unittest.TestCase):
    def setUp(self) -> None:
        self.default_grammar_input0 = "S -> i E t S \n"\
                                     "S -> i E t S e S \n"\
                                     "S -> a \n"\
                                     "E -> b"
        self.default_grammar0 = NonContextGrammar(self.default_grammar_input0)
        grammar_input1: str = "P -> K V C \n" \
                              "K -> c K \n" \
                              "K -> & \n" \
                              "V -> v V \n" \
                              "V -> F \n" \
                              "F -> f P ; F \n" \
                              "F -> & \n" \
                              "C -> b V C e \n" \
                              "C -> com ; C \n" \
                              "C -> &"
        self.default_grammar1 = NonContextGrammar(grammar_input1)
        grammar_input2: str = "S -> A B \n" \
                              "A -> a B A \n" \
                              "A -> & \n" \
                              "B -> C D \n" \
                              "C -> b D C \n" \
                              "C -> & \n" \
                              "D -> c S c \n" \
                              "D -> d"
        self.default_grammar2 = NonContextGrammar(grammar_input2)
        grammar_input3: str = "S -> A C\n"\
                            "S -> B C\n"\
                            "A -> a D\n"\
                            "A -> c C\n"\
                            "B -> a B\n"\
                            "B -> d D\n"\
                            "C -> e C\n"\
                            "C -> e A\n"\
                            "D -> f D\n"\
                            "D -> C B"
        self.grammar3 = NonContextGrammar(grammar_input3)

    # TODO: Comportamento estranho na grammar0, grammar3
    # @unittest.skip("")
    def test_convert_grammar(self) -> None:
        grammar_input = "S -> S c \n" \
                        "S -> A a \n" \
                        "S -> c \n" \
                        "A -> S a \n" \
                        "A -> B b \n" \
                        "A -> a \n" \
                        "B -> S c \n" \
                        "B -> B b"

        grammar = NonContextGrammar(grammar_input)
        grammar._eliminate_left_recursion()
        grammar._left_factoring()
        grammar._set_first()
        grammar._set_follow()
        return None

    # @unittest.skip("")
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

    # @unittest.skip("")
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
        expected_productions = {("A", ("S", "a")),
                                ("A", ("B", "b")),
                                ("A", tuple("a")),
                                ("B", ("S", "c", "C")),
                                ("C", ("b", "C")),
                                ("C", tuple("&")),
                                ("S", ("a", "a", "D")),
                                ("S", ("c", "D")),
                                ("D", ("c", "D")),
                                ("D", ("a", "a", "D")),
                                ("D", ("c", "C", "b", "a", "D")),
                                ("D", tuple("&"))
                                }

        for _ in range(10000):
            aux_grammar = copy(grammar)
            aux_grammar._eliminate_left_recursion()
            self.assertEqual(aux_grammar.get_transitions(), expected_productions)

        return None

    # @unittest.skip("")
    def test_first(self) -> None:
        # grammar_input = "S -> A B \n"\
        #                 "A -> a B A \n"\
        #                 "A -> & \n"\
        #                 "B -> C D \n"\
        #                 "C -> b D C \n"\
        #                 "C -> & \n"\
        #                 "D -> c S c \n"\
        #                 "D -> d"
        # grammar = NonContextGrammar(grammar_input)
        # expected_first = {"S": {"a", "b", "c", "d"},
        #                   "A": {"a", "&"},
        #                   "B": {"b", "c", "d"},
        #                   "C": {"b", "&"},
        #                   "D": {"c", "d"}}
        # grammar._convert_grammar()
        # self.assertEqual(grammar.get_first(), expected_first)
        self.default_grammar1._set_first()
        expected_first = {"P": {"c", "v", "f", "b", "com", "&"},
                          "K": {"c", "&"},
                          "V": {"v", "f", "&"},
                          "F": {"f", "&"},
                          "C": {"b", "com", "&"}
                          }
        self.assertEqual(self.default_grammar1.get_first(), expected_first)
        expected_first = {"S": {"a", "b", "c", "d"},
                          "A": {"a", "&"},
                          "B": {"b", "c", "d"},
                          "C": {"b", "&"},
                          "D": {"c", "d"}
                          }
        self.default_grammar2._set_first()
        self.assertEqual(self.default_grammar2.get_first(), expected_first)

        return None

    # @unittest.skip("")
    def test_follow(self) -> None:
        expected_follow = {"S": {"$", "c"},
                           "A": {"b", "c", "d"},
                           "B": {"$", "a", "b", "c", "d"},
                           "C": {"c", "d"},
                           "D": {"$", "a", "b", "c", "d"}}
        self.default_grammar2._set_first()
        self.default_grammar2._set_follow()
        self.assertEqual(self.default_grammar2.get_follow(), expected_follow)

        self.default_grammar1._set_first()
        self.default_grammar1._set_follow()
        expected_follow = {"P": {"$", ";"},
                           "K": {"v", "f", "b", ";", "com", "$"},
                           "V": {"b", "e", ";", "com", "$"},
                           "F": {"b", "e", ";", "com", "$"},
                           "C": {";", "e", "$"}
                           }
        self.assertEqual(self.default_grammar1.get_follow(), expected_follow)
        return None

    # @unittest.skip("")
    def test_get_first_of_production(self) -> None:
        expected_first = {"i"}
        self.assertEqual(self.default_grammar0._get_first_of_production(("i", "E", "t", "S")),
                         expected_first)

        return None

    @unittest.skip("")
    def test_table(self) -> None:
        self.default_grammar1._set_first()
        self.default_grammar1._set_follow()
        table = self.default_grammar1.construct_analysis_table()
        # for non_terminal in self.default_grammar1.get_non_terminals():
        #     for terminal in self.default_grammar1.get_terminals():
        #         try:
        #             print(f"table[{non_terminal}][{terminal}] = {table[non_terminal][terminal]}")
        #         except KeyError:
        #             pass
        return None
    """
    Left Factoring Tests
    """

    # @unittest.skip("")
    def test_get_productions_with_same_terminals(self) -> None:
        grammar_input = "S -> A C\n"\
                        "S -> B C\n"\
                        "A -> a D\n"\
                        "A -> c C\n"\
                        "B -> a B\n"\
                        "B -> d D\n"\
                        "C -> e C\n"\
                        "C -> e A\n"\
                        "D -> f D\n"\
                        "D -> C B"
        grammar = NonContextGrammar(grammar_input)
        expected = {"a": {"A", "B"}}
        actual = grammar._get_productions_with_same_terminals()
        self.assertEqual(expected, actual)

        grammar_input = "S -> z\n"\
                        "A -> z\n"\
                        "B -> x C D\n"\
                        "C -> x A B"
        grammar = NonContextGrammar(grammar_input)
        expected = {"z": {"S", "A"}, "x": {"B", "C"}}
        actual = grammar._get_productions_with_same_terminals()
        self.assertEqual(expected, actual)
        return None

    @unittest.skip("")
    def test_replace_indirect_nd_transitions(self) -> None:
        grammar_input = "S -> A C\n"\
                        "S -> B C\n"\
                        "A -> a D\n"\
                        "A -> c C\n"\
                        "B -> a B\n"\
                        "B -> d D\n"\
                        "C -> e C\n"\
                        "C -> e A\n"\
                        "D -> f D\n"\
                        "D -> C B"
        grammar = NonContextGrammar(grammar_input)
        grammar._replace_indirect_nd_transitions("S", "A")
        expected = {
            ("S", ("a", "D", "C")),
            ("S", ("c", "C", "C")),
            ("S", ("B", "C")),
            ("A", ("a", "D")),
            ("A", ("c", "C")),
            ("B", ("a", "B")),
            ("B", ("d", "D")),
            ("C", ("e", "C")),
            ("C", ("e", "A")),
            ("D", ("f", "D")),
            ("D", ("C", "B"))
        }
        actual = grammar.get_transitions()
        self.assertEqual(expected, actual)
        return None

    @unittest.skip("")
    def test_replace_indirect_with_direct_non_determinism(self) -> None:
        grammar_input = "S -> A C\n"\
                        "S -> B C\n"\
                        "A -> a D\n"\
                        "A -> c C\n"\
                        "B -> a B\n"\
                        "B -> d D\n"\
                        "C -> e C\n"\
                        "C -> e A\n"\
                        "D -> f D\n"\
                        "D -> C B"
        grammar = NonContextGrammar(grammar_input)
        grammar._replace_indirect_with_direct_non_determinism()
        expected = {
            ("S", ("a", "D", "C")),
            ("S", ("c", "C", "C")),
            ("S", ("a", "B", "C")),
            ("S", ("d", "D", "C")),
            ("A", ("a", "D")),
            ("A", ("c", "C")),
            ("B", ("a", "B")),
            ("B", ("d", "D")),
            ("C", ("e", "C")),
            ("C", ("e", "A")),
            ("D", ("f", "D")),
            ("D", ("C", "B"))
        }
        actual = grammar.get_transitions()
        self.assertEqual(expected, actual)
        return None

    # @unittest.skip("")
    def test_remove_direct_non_determinism(self) -> None:
        grammar_input = "S -> i E t S \n"\
                        "S -> i E t S e S \n"\
                        "S -> a \n"\
                        "E -> b"
        grammar = NonContextGrammar(grammar_input)
        expected = {
            ("S", ("i", "E", "t", "S", "F")),
            ("S", tuple("a")),
            ("F", ("e", "S")),
            ("F", tuple("&")),
            ("E", tuple("b"))
        }
        grammar._remove_direct_non_determinism()
        actual = grammar.get_transitions()
        self.assertEqual(actual, expected)

        grammar_input = "S -> a D C\n"\
                        "S -> c C C\n"\
                        "S -> a B C\n"\
                        "S -> d D C\n"\
                        "A -> a D\n"\
                        "A -> c C\n"\
                        "B -> a B\n"\
                        "B -> d D\n"\
                        "C -> e C\n"\
                        "C -> e A\n"\
                        "D -> f D\n"\
                        "D -> C B"
        grammar = NonContextGrammar(grammar_input)
        grammar._remove_direct_non_determinism()
        expected = {
            ("S", ("a", "F")),
            ("S", ("c", "C", "C")),
            ("S", ("d", "D", "C")),
            ("F", ("D", "C")),
            ("F", ("B", "C")),
            ("A", ("a", "D")),
            ("A", ("c", "C")),
            ("B", ("a", "B")),
            ("B", ("d", "D")),
            ("C", ("e", "E")),
            ("E", tuple("C")),
            ("E", tuple("A")),
            ("D", ("f", "D")),
            ("D", ("C", "B")),
        }
        grammar._remove_direct_non_determinism()
        actual = grammar.get_transitions()
        self.assertEqual(expected, actual)
        return None

    @unittest.skip("")
    def test_left_factoring(self) -> None:
        # grammar_input = "S -> i E t S \n"\
                        # "S -> i E t S e S \n"\
                        # "S -> a \n"\
                        # "E -> b"
        # grammar = NonContextGrammar(grammar_input)
        # expected = {
            # ("S", ("i", "E", "t", "S", "F")),
            # ("S", tuple("a")),
            # ("F", ("e", "S")),
            # ("F", tuple("&")),
            # ("E", tuple("b"))
        # }
        # grammar._left_factoring()
        # actual = grammar.get_transitions()
        # self.assertEqual(expected, actual)

        grammar_input = "S -> A C\n"\
                        "S -> B C\n"\
                        "A -> a D\n"\
                        "A -> c C\n"\
                        "B -> a B\n"\
                        "B -> d D\n"\
                        "C -> e C\n"\
                        "C -> e A\n"\
                        "D -> f D\n"\
                        "D -> C B"
        grammar = NonContextGrammar(grammar_input)
        expected = {
            ("S", ("a", "F")),
            ("S", ("c", "C", "C")),
            ("S", ("d", "D", "C")),
            ("F", ("D", "C")),
            ("F", ("B", "C")),
            ("A", ("a", "D")),
            ("A", ("c", "C")),
            ("B", ("a", "B")),
            ("B", ("d", "D")),
            ("C", ("e", "E")),
            ("E", tuple("C")),
            ("E", tuple("A")),
            ("D", ("f", "D")),
            ("D", ("C", "B"))
        }
        for _ in range(10000):
            grammar = NonContextGrammar(grammar_input)
            grammar._left_factoring()
            actual = grammar.get_transitions()
            self.assertEqual(expected, actual)
        return None

    # @unittest.skip("")
    def test_replace_transitions(self) -> None:
        grammar_input = "S -> A C \n"\
                        "S -> B C \n"\
                        "A -> a D \n"\
                        "A -> c C"

        grammar = NonContextGrammar(grammar_input)
        grammar._replace_indirect_nd_transitions("S", "A")

        expected = {
            ("S", ("a", "D", "C")),
            ("S", ("c", "C", "C")),
            ("S", ("B", "C")),
            ("A", ("a", "D")),
            ("A", ("c", "C"))
        }
        actual = grammar.get_transitions()
        self.assertEqual(expected, actual)

        return None

    @unittest.skip("")
    def test_recursion_and_factoring(self) -> None:
        grammar_input = "S -> S c \n" \
                        "S -> A a \n" \
                        "S -> c \n" \
                        "A -> S a \n" \
                        "A -> B b \n" \
                        "A -> a \n" \
                        "B -> S c \n" \
                        "B -> B b"

        grammar = NonContextGrammar(grammar_input)
        grammar._eliminate_left_recursion()
        expected_productions = {("A", ("S", "a")),
                                ("A", ("B", "b")),
                                ("A", tuple("a")),
                                ("B", ("S", "c", "C")),
                                ("C", ("b", "C")),
                                ("C", tuple("&")),
                                ("S", ("a", "a", "D")),
                                ("S", ("c", "D")),
                                ("D", ("c", "D")),
                                ("D", ("a", "a", "D")),
                                ("D", ("c", "C", "b", "a", "D")),
                                ("D", tuple("&"))
                                }
        actual = grammar.get_transitions()
        self.assertEqual(expected_productions, actual)
        grammar._left_factoring()
        expected_productions = {("A", ("S", "a")),
                                ("A", ("B", "b")),
                                ("A", tuple("a")),
                                ("B", ("S", "c", "C")),
                                ("C", ("b", "C")),
                                ("C", tuple("&")),
                                ("S", ("a", "a", "D")),
                                ("S", ("c", "D")),
                                ("D", ("c", "E")),
                                ("D", ("a", "a", "D")),
                                ("D", tuple("&")),
                                ("E", tuple("D")),
                                ("E", ("C", "b", "a", "D"))
                                }
        actual = grammar.get_transitions()
        self.assertEqual(expected_productions, actual)

        return None

    def test_is_ll1(self) -> None:
        self.default_grammar1.convert_grammar()
        self.assertTrue(self.default_grammar1.is_ll1())
        return None
