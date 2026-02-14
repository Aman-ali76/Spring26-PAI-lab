# Water Jug Problem Solver

x = 0
y = 0


x_cap = 7
y_cap = 4
goal = 5

# goal = int(input("Enter the goal amount of water to be measured: "))
# x_cap = int(input("Enter capacity of jug X: "))
# y_cap = int(input("Enter capacity of jug Y: "))

print(f"Jug X capacity: {x_cap}, Jug Y capacity: {y_cap}, Goal: {goal}")
print("\nRules:")
print("1: Fill X")
print("2: Fill Y")
print("3: Empty X")
print("4: Empty Y")
print("5: Pour X -> Y until X is empty")
print("6: Pour X -> Y until Y is filled")
print("7: Pour Y -> X until Y is empty")
print("8: Pour Y -> X until X is filled")

while x != goal and y != goal:
    print(f"Current State: X = {x} , Y = {y}")
    r = int(input("Enter your choice (1-8): "))

    if r==1:
        x = x_cap
    elif r==2:
        y = y_cap
    elif r==3:
        x = 0
    elif r==4:
        y = 0

    elif r == 5:  
        if x + y >= y_cap:
            y = y_cap
            x = 0
        else:
            y = x + y
            x = 0

    elif r==6:
        if x+y >= y_cap:
            y = y_cap
            x = x - (y_cap - y)
        else:
            y += x
            x = 0

    elif r == 7: 
        if x + y >= x_cap:
            x = x_cap
            y = 0
        else:
            x = x + y
            y = 0

    elif r==8:
        if x+y >= x_cap:
            x = x_cap
            y = y - (x_cap - x)
        else:
            x += y
            y = 0


print(f"Goal achieved! Current State: X = {x} , Y = {y}")