import sys
from functools import reduce

with open(sys.argv[1]) as f:
    lines = [l for l in f.readlines() if len(l) > 1]

# generally: i indexes lines and j indexes characters of a line

class Symbol:
    def __init__(self, character, i, j):
        self.character = character
        self.i = i
        self.j = j
        self.adjacent_numbers = []
    def is_symbol(character):
        return character not in ['.', '\n', '\r'] and not character.isdigit()

class Number:
    def __init__(self, character, i, j_start):
        self.string = character
        self.i = i
        self.j_start = j_start
        self.j_end = j_start
    def append(self, character):
        self.string += character
        self.j_end += 1

symbols = []
numbers = []
for i in range(0, len(lines)):
    line = lines[i]
    current_number = None
    for j in range(0, len(line)):
        if Symbol.is_symbol(line[j]):
            if current_number:
                numbers.append(current_number)
                current_number = None
            symbols.append(Symbol(line[j], i, j))
        elif line[j].isdigit():
            if current_number:
                current_number.append(line[j])
            else:
                current_number = Number(line[j], i, j)
        else:
            if current_number:
                numbers.append(current_number)
                current_number = None
    if current_number:
        numbers.append(current_number)
        current_number = None
        
# for number in numbers:
#     print(str(number.__dict__))
# for symbol in symbols:
#     print(str(symbol.__dict__))

def has_adjacent_symbol(number, symbols):
    for symbol in symbols:
        if symbol.i in range(number.i - 1, number.i + 2) \
            and symbol.j in range(number.j_start - 1, number.j_end + 2):
            # print(str(number.__dict__), " adjacent to ", str(symbol.__dict__))
            return True
        else:
            pass
            # print(str(number.__dict__), " is not adjacent to ", str(symbol.__dict__))
    return False

def collect_adjacent_numbers(number, stars):
    for symbol in stars:
        if symbol.i in range(number.i - 1, number.i + 2) \
            and symbol.j in range(number.j_start - 1, number.j_end + 2):
            symbol.adjacent_numbers.append(number)


sum_of_matching_numbers = 0
stars = [symbol for symbol in symbols if symbol.character == '*']
for number in numbers:
    if has_adjacent_symbol(number, symbols):
        sum_of_matching_numbers += int(number.string)
    collect_adjacent_numbers(number, stars)


sum_of_stars_adjacent_numbers = 0
for star in stars:
    if len(star.adjacent_numbers) == 2:
        sum_of_stars_adjacent_numbers += int(star.adjacent_numbers[0].string) * int(star.adjacent_numbers[1].string)

#sum_of_stars_adjacent_numbers = reduce(lambda x, y: x + y, [star.adjacent_numbers[0] * star.adjacent_numbers[1] for star in stars if len(star.adjacent_numbers) == 2])

print("part 1: ", sum_of_matching_numbers)
print("part 2: ", sum_of_stars_adjacent_numbers)