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

        path = finder.find('car', 'cat')
        self.assertEquals(path, ['car', 'cat'])

        path = finder.find('hot', 'car')
        self.assertEquals(path, ['hot', 'hat', 'cat', 'car'])

        path = finder.find('hot', 'cut')
        self.assertEquals(path, ['hot', 'hat', 'cat', 'cut'])

        path = finder.find('hot', 'put')
        self.assertEquals(path, ['hot', 'pot', 'put'])

        path = finder.find('hot', 'fit')
        self.assertEquals(path, None)


if __name__ == '__main__':
    unittest.main()

