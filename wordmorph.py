#!/usr/bin/env python

import argparse
import multiprocessing
import sys
import threading
from Queue import PriorityQueue


class Graph(object):
    """Organize words of the same length in buckets using simple globbing
    patterns. All words in the same bucket are just one letter apart. Each
    word points to a list of patterns that can be used as hashes to index
    other words in buckets. This effectively represents a graph.

    Consider the following words:
        car
        cat
        hat
        hot

    The word "car" will be indexed in the following buckets:
        .ar: car
        c.r: car
        ca.: car

    The word "cat" will be indexed in the following buckets:
        .at: cat
        c.t: cat
        ca.: car cat

    And so on. The graph for the 4 words above will look like this:
        .ar: car
        .at: cat hat
        .ot: hot
        c.r: car
        c.t: cat
        ca.: car cat
        h.t: hat hot
        ha.: hat
        ho.: hot

    Finding all words one letter app for any given word is the result of
    the union of all words in the buckets where the word is indexed.
    For example, adjancent words for "cat" are:

        cat
        hat
    """
    nodes = dict()
    buckets = dict()

    def add(self, word):
        """Index word in buckets with words one letter apart."""
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
        """Return one-letter globbing patterns for given word. For example,
        the word 'cat' will return:
        ['.at', 'c.t', 'ca.']
        """
        patterns = []
        for index in xrange(len(word)):
            pattern = word[:index] + '.' + word[index+1:]
            patterns.append(pattern)
        return patterns

    def adjacent(self, word):
        """Return all words one letter apart for given word by combining the
        words where its indexed."""
        all_adjacent = set()
        patterns = self.nodes.get(word, [])
        for pattern in patterns:
            nodes = self.buckets[pattern]
            all_adjacent = all_adjacent.union(nodes)
        all_adjacent.remove(word)
        return all_adjacent

    @classmethod
    def build_from_file(class_type, file_name, word_length):
        """Initialize graph from words of the specified length stored in the
        given text file."""
        graph = class_type()
        lines = []
        with open(file_name, 'r') as input_file:
            lines = input_file.read()
        lines = lines.split()
        cpus = multiprocessing.cpu_count()
        total_lines = len(lines)
        lines_per_process = total_lines/cpus
        remaining_lines = total_lines%cpus
        threads = []
        for index in xrange(cpus):
            start = index*lines_per_process
            end = start+lines_per_process
            if index == (cpus-1):
                end += remaining_lines
            thread = threading.Thread(target=graph.build_from_lines, args=(lines, start, end, word_length))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return graph

    def build_from_lines(self, lines, start, end, word_length):
        for index in xrange(start, end):
            word = lines[index]
            word = word.strip() if word else word
            if not word or len(word) != word_length:
                continue
            self.add(word)

    @classmethod
    def build_from_words(class_type, words):
        graph = class_type()
        for word in words:
            graph.add(word)
        return graph

    def print_contents(self):
        """Print words indexed per globbing pattern bucket."""
        print 'Graph:'
        for pattern, words in sorted(self.buckets.items()):
            print '{pattern}: {words}'.format(
                pattern=pattern,
                words=' '.join(sorted(list(words))),
            )
        print

    def print_adjacent(self, word):
        """Print all words one-letter apart from given word"""
        print 'Word    :', word
        if word not in self.nodes:
            print 'Not found'
            return
        print 'Adjacent:', ' '.join(sorted(list(self.adjacent(word))))
        print


class PathFinder(object):
    """Find shortest path between two words - if any - using Dijkstra's
    algorithm."""

    def __init__(self, graph):
        self.graph = graph
        self.trail = dict()
        self.distances = dict()

    def find(self, start, end):
        """Find shortest path between two words, if any.
        Returns
        (distance, list) indicating the shortest path found.
        (0, []) if start and end are the same word.
        (None, None) if not valid transformation is found.
        """
        if not start or not end:
            return None, None
        if start == end:
            return 0, []
        self.measure(start, end)
        distance, path = self.build_path(start, end)
        return distance, path

    def measure(self, start, end):
        """Find shortest path using Dijkstra's algorithm."""
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
        """Return distance and list of nodes representing the shortest path
        from start to end, if any.

        Returns
        (distance, list) if path found.
        (None, None) if not valid transformation is found.
        """
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
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Shortest steps to morph one word into another one letter at a time.')
    parser.add_argument('file_name', type=str, help='text file with list of words')
    parser.add_argument('word_length', type=int, help='number of letters per word')
    parser.add_argument('start', type=str, help='start word')
    parser.add_argument('end', type=str, help='end word')
    parser.add_argument('--verbose', dest='verbose', action='store_true', help='show debug information')
    arguments = parser.parse_args()

    # Build graph
    graph = Graph.build_from_file(arguments.file_name, arguments.word_length)

    if arguments.verbose:
        graph.print_contents()
        graph.print_adjacent(arguments.start)
        graph.print_adjacent(arguments.end)

    # Find path between give start and end words.
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

