def day1_part1(input):
    input = [list(map(int, x.split('-'))) for x in input.split('\n')]
    input = sorted(input, key=lambda x: tuple(x))

    cur = 0
    for [strt, end] in input:
        if cur < strt:
            return cur
        elif cur <= end:
            cur = end + 1

    return cur

def day1_part2(input, max_ip = 4294967295):
    input = [list(map(int, x.split('-'))) for x in input.split('\n')]
    input = sorted(input, key=lambda x: tuple(x))

    total, mn, mx = 0, input[0][0], input[0][1]
    for [strt, end] in input:
        if strt > mx + 1:
            total += mx - mn + 1
            mn, mx = strt, end
        else:
            mx = max(mx, end)
    
    return max_ip + 1 - total - (mx - mn + 1)

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day1_part1(example_input) == 3
    print(day1_part1(test_input))

    assert day1_part2(example_input, 9) == 2
    print(day1_part2(test_input))