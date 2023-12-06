import sys
import re
from functools import reduce

with open(sys.argv[1]) as f:
    lines = [l for l in f.readlines() if len(l) > 1]

# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11

r = re.compile(r'Card *(\d+): (.*) \| (.*)')
sum_part_1 = 0
counts_part_2 = list([1 for line in lines])
for i in range(0, len(lines)):
    m = r.match(lines[i])
    if (m):
        card = m.group(1)
        winning_numbers = set(m.group(2).split())
        actual_numbers = set(m.group(3).split())
        intersection = actual_numbers.intersection(winning_numbers)
        if (intersection):
            count_matches = len(intersection)
            sum_part_1 += pow(2, count_matches - 1)
            for j in range(1, count_matches + 1):
                counts_part_2[i + j] += counts_part_2[i]
                #print("adding", count_matches, "matches for card", card, "to card", i+j+1, "→", counts_part_2[i + j])
        # print(card, ": winning: ", winning_numbers, ", actual: ", actual_numbers, ", intersection: ", intersection)
    else:
        # print("no match: ", line)
        pass


print("part 1: ", sum_part_1)
print("part 2: ", reduce(lambda x, y: x + y, counts_part_2))
#print(counts_part_2)
