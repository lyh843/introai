import math

result = 2 * math.comb(60, 2) * math.comb(40, 1) / math.comb(100, 3) / math.perm(3, 3)
print(result - (236 / 1617))