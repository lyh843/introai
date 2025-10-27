num = int(input("请输入一个年份"))
if (num % 4 == 0 and num % 100 != 0) or num % 400 == 0:
    print("这一年是闰年")
else:
    print("这一年不是闰年")
    
    
max_num = 0
for i in range(5):
    temp = int(input(f"请输入第 {i + 1} 个整数： "))
    max_num = max_num if max_num > temp else temp
print("五个数中最大的数是：", max_num) 


num = input("请输入一个整数：")
sum_digits = 0
for digit in num:
    sum_digits += int(digit)
print("这个整数每一位数字的和是：", sum_digits)


power = 20
print(f"初始电量：{power}%")
while power < 100:
    power += 5 if 100 - power > 5 else 100 - power
    print(f"正在充电，当前电量：{power}%")
    if power == 80:
        use_choice = input("电量已达80%，是否要先使用？（输入是或否）：")
        if use_choice == "是":
            print("可先使用设备，使用后可再次充电")
            break
        else:
            print("继续充电")
    if power == 90:
        stop_choice = input("电量已达90%，是否要停止充电？（输入是或否）：")
        if stop_choice == "是":
            print(f"已停止充电，最终电量：{power}%")
            break
if power == 100:
    print("充电已完成，当前电量：100%")