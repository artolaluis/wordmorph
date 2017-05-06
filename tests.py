#!/usr/bin/env python

import unittest

import wordmorph


class TestGraph(unittest.TestCase):

    def test_basics(self):
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
        finder = wordmorph.PathFinder(graph)

        distance, path = finder.find('car', 'cat')
        self.assertEquals(distance, 1)
        self.assertEquals(path, ['car', 'cat'])

        distance, path = finder.find('hot', 'car')
        self.assertEquals(distance, 3)
        self.assertEquals(path, ['hot', 'hat', 'cat', 'car'])

        distance, path = finder.find('hot', 'cut')
        self.assertEquals(distance, 3)
        self.assertEquals(path, ['hot', 'hat', 'cat', 'cut'])

        distance, path = finder.find('hot', 'put')
        self.assertEquals(distance, 2)
        self.assertEquals(path, ['hot', 'pot', 'put'])

        distance, path = finder.find('hot', 'fit')
        self.assertEquals(distance, None)
        self.assertEquals(path, None)

        distance, path = finder.find('hot', 'hot')
        self.assertEquals(distance, 0)
        self.assertEquals(path, [])

if __name__ == '__main__':
    unittest.main()

