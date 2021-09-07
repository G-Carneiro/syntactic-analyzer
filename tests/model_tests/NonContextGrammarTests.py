import unittest

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
        grammar._eliminate_left_recursion()
        print(grammar.get_transitions())

