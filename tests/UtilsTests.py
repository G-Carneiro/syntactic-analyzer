from utils.utils import *

import unittest


class UtilsTests(unittest.TestCase):
    # @unittest.skip("")
    def test_common_prefix_size(self) -> None:
        prefix1 = ('i', 'E', 't', 'S')
        prefix2 = ('i', 'E', 't', 'S', 'e', 'S')
        expected = 4
        actual = common_prefix_size(prefix1, prefix2)
        self.assertEqual(expected, actual)

        prefix1 = ('c', 'C')
        prefix2 = ('a', 'D')
        expected = 0
        actual = common_prefix_size(prefix1, prefix2)
        self.assertEqual(expected, actual)

        prefix1 = ('e', 'C')
        prefix2 = ('e', 'A')
        expected = 1
        actual = common_prefix_size(prefix1, prefix2)
        self.assertEqual(expected, actual)
        return None

    # @unittest.skip("")
    def test_find_longest_prefix(self) -> None:
        productions = [('a',), ('i', 'E', 't', 'S', 'e', 'S'), ('i', 'E', 't', 'S')]
        expected = ('i', 'E', 't', 'S')
        actual = find_longest_common_prefix(productions)
        self.assertEqual(expected, actual)

        productions = [('a', 'D'), ('c', 'C')]
        expected = tuple()
        actual = find_longest_common_prefix(productions)
        self.assertEqual(expected, actual)

        productions = [('e', 'A'), ('e', 'C')]
        expected = ('e',)
        actual = find_longest_common_prefix(productions)
        self.assertEqual(expected, actual)

        production = [
            ('f', 'o', 'o'),
            ('f', 'o', 'o', 'b', 'a', 'r'),
            ('f', 'o', 'o', 't', 'b', 'a', 'l', 'l'),
            ('f', 'o', 'o', 't', 'b', 'a', 'g'),
            ('b', 'a', 'r'),
        ]
        expected = ('f', 'o', 'o', 't', 'b', 'a')
        actual = find_longest_common_prefix(production)
        self.assertEqual(expected, actual)
        return None

    # @unittest.skip("")
    def test_add_factored_transition(self) -> None:
        new_transitions = {("S'", ('&',))}
        production = ('i', 'E', 't', 'S', 'e', 'S')
        prefix = ('i', 'E', 't', 'S')
        new_non_terminal = "S'"
        new_transitions = {("S'", ('e', 'S')), ("S'", ('&',))}

        expected = {("S'", ('e', 'S')), ("S'", ('&',))}
        actual = add_factored_transition(
            new_transitions,
            production,
            prefix,
            new_non_terminal,
        )
        self.assertEqual(expected, actual)
        return None

    # @unittest.skip("")
    def test_get_new_body(self) -> None:
        production = ('c', 'C')
        production_to_replace = ('A', 'C')
        nt_to_replace = "A"
        expected = ('c', 'C', 'C')
        actual = get_new_body(production, production_to_replace, nt_to_replace)
        self.assertEqual(expected, actual)

        production = ('a', 'D')
        production_to_replace = ('A', 'C')
        nt_to_replace = "A"
        expected = ('a', 'D', 'C')
        actual = get_new_body(production, production_to_replace, nt_to_replace)
        self.assertEqual(expected, actual)

        production = ('d', 'D')
        production_to_replace = ('B', 'C')
        nt_to_replace = "B"
        expected = ('d', 'D', 'C')
        actual = get_new_body(production, production_to_replace, nt_to_replace)
        self.assertEqual(expected, actual)
        return None

    # @unittest.skip("")
    def test_assemble_new_transition(self) -> None:
        non_terminal = "S"
        new_non_terminal = "F"
        longest_commom_prefix = ('i', 'E', 't', 'S')
        expected = ('S', ('i', 'E', 't', 'S', "F"))
        actual = assemble_new_transition(non_terminal, longest_commom_prefix, new_non_terminal)
        self.assertEqual(expected, actual)

        non_terminal = "C"
        new_non_terminal = "F"
        longest_commom_prefix = ('e',)
        expected = ('C', ('e', "F"))
        actual = assemble_new_transition(non_terminal, longest_commom_prefix, new_non_terminal)
        self.assertEqual(expected, actual)

        non_terminal = "S"
        new_non_terminal = "F"
        longest_commom_prefix = ('a',)
        expected = ('S', ('a', "F"))
        actual = assemble_new_transition(non_terminal, longest_commom_prefix, new_non_terminal)
        self.assertEqual(expected, actual)
        return None

    @unittest.skip("")
    def test_latex_table(self) -> None:
        latex_analysis_table({"S", "A"}, {"a", "b"}, {})

        return None
