def parse_input(input, part_2=False):
    start = []

    # replace nonsense words
    for repl in ['The ', 'floor ', 'first ', 'second ', 'third ', 'fourth ', 'contains ', 'a ', 'and ', '.', ',']:
        input = input.replace(repl, '')

    # replace microchip and generator with shortened name
    input = input.replace('-compatible microchip', 'M')
    input = input.replace(' generator', 'G')

    # create our start state
    input = input.split('\n')
    for line in input:
        if line == 'nothing relevant':
            start.append(set())
        else:
            start.append(set(line.split(' ')))

    # if part 2, add additional items
    if part_2:
        start[0].add('eleriumG')
        start[0].add('eleriumM')
        start[0].add('dilithiumG')
        start[0].add('dilithiumM')

    return (0, tuple(start))

def deep_copy_items(items):
    return [x.copy() for x in items]

def all_okay(floor):
    # check nothing fries nothing else
    gens = [x for x in floor if x.endswith('G')]
    if not gens:
        return True
    
    for x in floor:
        if x.endswith('M') and x[:-1] + 'G' not in floor:
            return False
    return True

def neighbours(node):
    pos, items = node[0], list(node[1])
    cur_floor = items[pos]
    cur_floor_copy = list(cur_floor.copy())
    neighbours = []

    for nxt_pos in [pos - 1, pos + 1]:
        # not a valid floor
        if not 0 <= nxt_pos < 4: continue
        other_floor = items[nxt_pos]

        # brute force moving all items
        for i, x in enumerate(cur_floor_copy):
            # try moving only x
            other_floor.add(x)
            cur_floor.discard(x)
            if all_okay(other_floor) and all_okay(cur_floor):
                nxt_items = tuple(deep_copy_items(items))
                neighbours.append((nxt_pos, nxt_items))

            for y in cur_floor_copy[i+1:]:
                # try additionally moving y
                other_floor.add(y)
                cur_floor.discard(y)
                if all_okay(other_floor) and all_okay(cur_floor):
                    nxt_items = tuple(deep_copy_items(items))
                    neighbours.append((nxt_pos, nxt_items))
                other_floor.discard(y)
                cur_floor.add(y)

            other_floor.discard(x)
            cur_floor.add(x)

    return neighbours

def hash_node(node):
    # sort each floors content for standard representation
    pos, items = node[0], node[1]
    items = [sorted(s) for s in items]

    # formulate mapping name -> int for collapsing equivalent states
    conv = {}
    for i in range(4):
        for j, x in enumerate(items[i]):
            if x[:-1] not in conv:
                conv[x[:-1]] = str(len(conv))
            items[i][j] = f'{conv[x[:-1]]}{x[-1]}'

    return f'({pos},{tuple(items)})'.replace(']', '])').replace('[', 'set([')

def unhash_node(node):
    return eval(node)

def bfs(start):
    vis = set()
    depth = 0
    queue = [hash_node(start)]

    while queue:
        new_queue = []
        print(depth, len(queue))

        for hashed_node in queue:
            # ignore if visited
            if hashed_node in vis:
                continue
            vis.add(hashed_node)

            # ending condition
            node = unhash_node(hashed_node)
            items = node[1]
            if sum(len(x) for x in items[:-1]) == 0:
                return depth
            
            # deal with neighbours
            for nxt in neighbours(node):
                if hash_node(nxt) in vis: continue
                new_queue.append(hash_node(nxt))

        depth += 1
        queue = new_queue
    return -1

def day11_part1(input):
    start = parse_input(input)
    res = bfs(start)
    return res

def day11_part2(input):
    start = parse_input(input, True)
    res = bfs(start)
    return res

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day11_part1(example_input) ==  11
    print(day11_part1(test_input))

    print(day11_part2(test_input))