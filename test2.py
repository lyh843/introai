import numpy as np

number1 = [81, 165, 97, 134, 92, 87, 14]
number2 = [102, 86, 98, 109, 92]

x_bar = np.mean(number1)
y_bar = np.mean(number2)

s_x2 = 0.0
for i in number1:
    s_x2 += (i - x_bar) ** 2
s_x2 /= (len(number1) - 1)

s_y2 = 0.0

for i in number2:
    s_y2 += (i - y_bar) ** 2
s_y2 /= (len(number2) - 1)

result = (x_bar - y_bar - 10) / np.sqrt(
    ((len(number1) - 1) * s_x2 + 10 * (len(number2) - 1) * s_y2) / (10 * (len(number1) + len(number2) - 2))
    ) / np.sqrt(10 / len(number1) + 1 / len(number2))
print(result)