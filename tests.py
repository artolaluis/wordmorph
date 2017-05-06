#!/usr/bin/env python

import unittest

import wordmorph


class TestGraph(unittest.TestCase):

    def setUp(self):
        words = '''
        car
        cat
        cut
        fit
        hat
        hot
        par
        pat
        pot
        put
        '''.strip().split()
        graph = wordmorph.Graph.build_from_words(words)
        self.finder = wordmorph.PathFinder(graph)

    def test_normal_cases(self):
        distance, path = self.finder.find('car', 'cat')
        self.assertEquals(distance, 1)
        self.assertEquals(path, ['car', 'cat'])

        distance, path = self.finder.find('hot', 'car')
        self.assertEquals(distance, 3)
        self.assertEquals(path, ['hot', 'hat', 'cat', 'car'])

        distance, path = self.finder.find('hot', 'cut')
        self.assertEquals(distance, 3)
        self.assertEquals(path, ['hot', 'hat', 'cat', 'cut'])

        distance, path = self.finder.find('hot', 'put')
        self.assertEquals(distance, 2)
        self.assertEquals(path, ['hot', 'pot', 'put'])

        distance, path = self.finder.find('hot', 'fit')
        self.assertEquals(distance, None)
        self.assertEquals(path, None)

        distance, path = self.finder.find('hot', 'hot')
        self.assertEquals(distance, 0)
        self.assertEquals(path, [])

    def test_edge_cases(self):
        distance, path = self.finder.find(None, None)
        self.assertEquals(distance, None)
        self.assertEquals(path, None)

        distance, path = self.finder.find('hot', None)
        self.assertEquals(distance, None)
        self.assertEquals(path, None)

        distance, path = self.finder.find(None, 'hot')
        self.assertEquals(distance, None)
        self.assertEquals(path, None)

        distance, path = self.finder.find('hot', '')
        self.assertEquals(distance, None)
        self.assertEquals(path, None)

        distance, path = self.finder.find('', 'hot')
        self.assertEquals(distance, None)
        self.assertEquals(path, None)

if __name__ == '__main__':
    unittest.main()

