import unittest
from prettytable import PrettyTable

class TerminalInteraction(unittest.TestCase):

	def test_print(self):
		print('test_print')

	def test_print_table(self):
		table = PrettyTable(['col1', 'col2', 'col3'])

		row1 = ['Hello', 1, 3.14159]
		row2 = ['World', 5, 1.567]
		table.add_row(row1)
		table.add_row(row2)
		print(table)

	def test_user_input(self):
		input = input('Test any key:')

		