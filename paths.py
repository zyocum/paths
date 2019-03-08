#!/usr/bin/env python3

"""Find solutions to a graph traversal problem.  The goal is to find the path from 
a start node to an end node where edges between nodes have a cost associated 
with them.  The best path is that which minimizes the maximum cost of the 
highest cost edge along the path.
"""

def ngrams(iterable, n=1):
    """Generate ngrams from an iterable
    
    l = range(5)
    list(l) -> [0, 1, 2, 3, 4, 5]
    list(ngrams(l, n=1)) -> [(0,), (1,), (2,), (3,), (4,)]
    list(ngrams(l, n=2)) -> [(0, 1), (1, 2), (2, 3), (3, 4)]
    list(ngrams(l, n=3)) -> [(0, 1, 2), (1, 2, 3), (2, 3, 4)]
    
    """
    return zip(*(iterable[i:] for i in range(n)))

def load(data):
    """Load graph and costs of edges from serialized data string"""
    lines = data.splitlines()
    graph = {}
    costs = {}
    for line in lines:
        source, dest, cost = map(int, line.split())
        if source not in graph:
            graph[source] = set()
        if dest not in graph:
            graph[dest] = set()
        graph[source].add(dest)
        graph[dest].add(source)
        costs[(source, dest)] = cost
        costs[(dest, source)] = cost
    return graph, costs

def paths(graph, start=None, end=None):
    """From a given graph, generate all possible paths from the start node
    to the end node."""
    if start is None:
        start = min(graph)
    if end is None:
        end = max(graph)
    stack = [(start, [])]
    while stack:
        node, path = stack.pop()
        # normally one would use path.append(node), but we do it this way
        # because it creates a new list, instead of reusing the existing list
        path = path + [node]
        for neighbor in graph[node].difference(set(path)):
            stack.append((neighbor, path))
        if node == end and len(path) > 0:
            yield tuple(path)

def cost(path, costs):
    """Compute the cost of the most costly edge along a given path"""
    most_costly = max(ngrams(path, n=2), key=costs.get)
    return costs[most_costly], len(path)

def main(data, start=None, end=None, verbose=False):
    """Sort each path by cost in ascending order"""
    graph, costs = load(data)
    results = sorted(
        (cost(path, costs), path)
        for path in paths(graph, start=start, end=end)
    )
    print('cost\tpath')
    for result in results:
        (cost_, length), path = result
        print(cost_, path, sep='\t')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__
    )
    parser.add_argument(
        'input',
        type=argparse.FileType('r'),
        help='input data file (use "-" to read from stdin)'
    )
    parser.add_argument(
        '-s', '--start',
        default=None,
        type=int,
        help='start node in the graph'
    )
    parser.add_argument(
        '-e', '--end',
        default=None,
        type=int,
        help='end node in the graph',
    )
    parser.add_argument(
        '-v', '--verbose',
        default=False,
        action='store_true',
        help='show verbose output'
    )
    args = parser.parse_args()
    main(
        args.input.read(),
        start=args.start,
        end=args.end,
        verbose=args.verbose
    )
    if args.input.name != '<stdin>':
        args.input.close()
