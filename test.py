import numpy as np
number = [81, 165, 97, 134, 92, 87, 14]

sum = 0
for i in number:
    sum += i
x_bar = sum / len(number)

s_2 = 0.0
for i in number:
    s_2 += (i - x_bar)**2
s_2 /= (len(number) - 1)

print(f"x_bar = {x_bar}\ns_2 = {s_2}\n")    

number1 = [102, 86, 98, 109, 92]

sum1 = 0
for i in number1:
    sum1 += i
x_bar1 = sum1 / len(number1)

s_21 = 0.0
for i in number1:
    s_21 += (i - x_bar1)**2
s_21 /= (len(number1) - 1)

print(f"x_bar = {x_bar1}\ns_2 = {s_21}\n")    

sigma_2 = (6 * s_2 / 10 + 4 * s_21) / 10
sigma_1 = 10 * sigma_2

result = (x_bar - x_bar1 - 10) / np.sqrt(sigma_1 / 7 + sigma_2 / 5)
print(f"result = {result}\n")