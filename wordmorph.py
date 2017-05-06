#!/usr/bin/env python

import argparse
import sys
from Queue import PriorityQueue


class Graph(object):
    nodes = dict()
    buckets = dict()

    def add(self, word):
        word = word.strip().lower() if word else word
        if not word:
            return
        patterns = self.patterns(word)
        self.nodes[word] = patterns
        for pattern in patterns:
            try:
                self.buckets[pattern].add(word)
            except KeyError:
                self.buckets[pattern] = set([word])

    def patterns(self, word):
        patterns = []
        for index in xrange(len(word)):
            pattern = word[:index] + '.' + word[index+1:]
            patterns.append(pattern)
        return patterns

    def adjacent(self, word):
        all_adjacent = set()
        patterns = self.nodes.get(word, [])
        for pattern in patterns:
            nodes = self.buckets[pattern]
            all_adjacent = all_adjacent.union(nodes)
        all_adjacent.remove(word)
        return all_adjacent

    @classmethod
    def build_from_file(class_type, file_name, word_length):
        graph = class_type()
        with open(file_name, 'r') as input_file:
            for word in input_file:
                word = word.strip() if word else word
                if not word or len(word) != word_length:
                    continue
                graph.add(word)
        return graph

    @classmethod
    def build_from_words(class_type, words):
        graph = class_type()
        for word in words:
            graph.add(word)
        return graph

    def print_contents(self):
        print 'Graph:'
        for pattern, words in sorted(self.buckets.items()):
            print '{pattern}: {words}'.format(
                pattern=pattern,
                words=' '.join(sorted(list(words))),
            )
        print

    def print_adjacent(self, word):
        print 'Word    :', word
        if word not in self.nodes:
            print 'Not found'
            return
        print 'Adjacent:', ' '.join(sorted(list(self.adjacent(word))))
        print


class PathFinder(object):

    def __init__(self, graph):
        self.graph = graph
        self.trail = dict()
        distances = dict()

    def find(self, start, end):
        if start == end:
            return 0, []
        self.measure(start, end)
        distance, path = self.build_path(start, end)
        return distance, path

    def measure(self, start, end):
        to_visit = PriorityQueue()
        self.trail = dict()
        self.distances = dict()

        to_visit.put((0, start))
        self.trail[start] = None
        self.distances[start] = 0

        while not to_visit.empty():
            current_distance, current_word = to_visit.get()
            if current_word == end:
                break
            nodes = self.graph.adjacent(current_word)
            for node in nodes:
                new_distance = self.distances[current_word] + 1
                if node not in self.distances or new_distance < self.distances[node]:
                    self.distances[node] = new_distance
                    to_visit.put((new_distance, node))
                    self.trail[node] = current_word

    def build_path(self, start, end):
        if end not in self.distances:
            return None, None

        path = [end]
        current = end
        while current != start:
            previous = self.trail[current]
            path.append(previous)
            current = previous
        path.reverse()

        return self.distances[end], path


def main():
    parser = argparse.ArgumentParser(description='Shortest steps to morph one word into another one letter at a time.')
    parser.add_argument('file_name', type=str, help='text file with list of words')
    parser.add_argument('word_length', type=int, help='number of letters per word')
    parser.add_argument('start', type=str, help='start word')
    parser.add_argument('end', type=str, help='end word')
    parser.add_argument('--verbose', dest='verbose', action='store_true', help='show debug information')
    arguments = parser.parse_args()

    graph = Graph.build_from_file(arguments.file_name, arguments.word_length)

    if arguments.verbose:
        graph.print_contents()
        graph.print_adjacent(arguments.start)
        graph.print_adjacent(arguments.end)

    finder = PathFinder(graph)
    distance, path = finder.find(arguments.start, arguments.end)
    print 'Morph: {start} to {end}'.format(start=arguments.start, end=arguments.end)
    if path is not None:
        print 'Path : {steps} steps'.format(steps=distance)
        print '\n'.join(path)
    else:
        print 'No solution.'


if __name__ == '__main__':
    main()

