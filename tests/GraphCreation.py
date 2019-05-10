import unittest
from classes.Graph import *

class GraphCreation(unittest.TestCase):

	def test_new_instance(self):
		graph = new Graph()
		assertTrue(graph.nodes)

	def test_new_edge(self):
		graph = new Graph()

		node1 = 'prev'
		node2 = 'next'
		graph.add_edge(node1, node2, weight=1)