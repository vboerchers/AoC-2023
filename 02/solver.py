import re
import sys
from functools import reduce

class Game:
    # parse Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    def __init__(self, line):
        m = re.compile(r'Game (\d+): (.*)').match(line)
        self.is_valid = True if m else False
        self.id = int(m.group(1))
        self.scores = {}
        for score in re.split('[,;] ', m.group(2)):
            n_color = score.split()
            self.scores.setdefault(n_color[1], []).append(int(n_color[0]))
    
    def has_greater_than(self, color, maxx):
        return color in self.scores and max(self.scores[color]) > maxx
    
    def get_power(self):
        return reduce(lambda x, y: x * y, [max(self.scores[color]) for color in self.scores])
            

with open(sys.argv[1]) as f:
    games = [Game(line) for line in f.readlines()]

max_counts = {'red':12, 'green':13, 'blue':14}

matching_id_sum = 0
power_sum = 0
for game in games:
    power_sum += game.get_power()
    game_matches = game.is_valid
    for color, maxx in max_counts.items():
        if game.has_greater_than(color, maxx):
            game_matches = False
    if game_matches:
        matching_id_sum += game.id

print("part 1: ", matching_id_sum)
print("part 2: ", power_sum)
