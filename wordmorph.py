#!/usr/bin/env python

import argparse
import sys


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


if __name__ == '__main__':
    main()

