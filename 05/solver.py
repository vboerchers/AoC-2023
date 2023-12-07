import sys
import re
from collections import OrderedDict

with open(sys.argv[1]) as f:
    lines = [l for l in f.readlines() if len(l) > 1]

# seeds: 79 14 55 13
# seed-to-soil map:
# 50 98 2
# soil-to-fertilizer map:
# 0 15 37
# fertilizer-to-water map:
# 49 53 8
# water-to-light map:
# 88 18 7
# light-to-temperature map:
# 45 77 23
# temperature-to-humidity map:
# 0 69 1
# humidity-to-location map:
# 60 56 37

class Mapping:
    def __init__(self, line, target):
        self.target = target
        words = line.split()
        dest_begin = int(words[0])
        source_begin = int(words[1])
        range_length = int(words[2])
        self.range = range(source_begin, range_length)
        self.change = dest_begin - source_begin
        # print("parsed", line[0:-1], "into " + str(self.change), "for[", self.range, "]", target)
    def has_mapping_for(self, number):
        return number in self.range
    def map(self, number):
        return number + self.change if number in self.range else number

# a OrderedDict of list of target mappings
mappings = OrderedDict()
map_re = re.compile(r'.*-to-(.*) map:')
current_target = 'undef'
current_mappings = None
for line in lines:
    if line.startswith("seeds: "):
        seeds = [int(seed) for seed in line[len("seeds: ")::].split()]
    elif line:
        if line[0].isalpha():
            m = map_re.match(line)
            if m:
                current_target = m.group(1)
                current_mappings = []
                mappings[current_target] = current_mappings
            else:
                print("no match for", line)
        elif line[0].isdigit():
            current_mappings.append(Mapping(line, current_target))

def map_seed(seed):
    mapped = seed
    for maps in mappings.values():
        for map in maps:
            if mapped in map.range:
                mapped += map.change
                break
        # relevant_maps = [map for map in maps if map.has_mapping_for(mapped)]
        # if len(relevant_maps) == 1:
        #     mapped = relevant_maps[0].map(mapped)
        # elif len(relevant_maps) > 1:
        #     print("ERROR? overlapping " + relevant_maps)
        # print(seed, "→ [", target, "] ", mapped)
    return mapped

mapped_seeds_part_1 = [map_seed(seed) for seed in seeds]
#print("part 1: from ", seeds, "to", mapped_seeds_part_1)
print("part 1: ", min(mapped_seeds_part_1))

seeds_ranges = [(seeds[i], seeds[i] + seeds[i+1]) for i in range(0, len(seeds), 2)]
total_count = sum([seeds[i+1] for i in range(0, len(seeds), 2)])
min_val = float("inf")
for seeds_range in sorted(seeds_ranges):
    current_count = seeds_range[1] - seeds_range[0]
    print("computing min for ", current_count, "seeds in", seeds_range, ",", 100.*current_count/total_count, "% of all")
    min_val = min(min_val, min((map_seed(seed) for seed in range(seeds_range[0], seeds_range[1]))))
    print("part 2, intermediate result: ", min_val)
print("part 2:", min_val)
#print("part 2: ", min(map_seeds(seeds_part_2)))


# Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
# Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
# Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
# Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.


