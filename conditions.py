from cs50 import get_int

x = get_int("x: ")
# get_int : int가 아닌 것을 입력받을 경우 다시 입력받게 함
y = get_int("y: ")

# if x<y:
#     print("x is less than y")
# elif x>y:
#     print("x is greater than y")
# else:
#     print("x is same with y")

# f: 3.6이상만
print(f"{x} plus {y} is {x+y}")
print(f"{x} truly divided by {y} is {x/y}")
print(f"{x} floor-divided by {y} is {x//y}")
print(f"{x} power {y} is {x**y}")
print("{first} power {se} is {third}".format(first=))
# 뒤에 못봄ㅎ
