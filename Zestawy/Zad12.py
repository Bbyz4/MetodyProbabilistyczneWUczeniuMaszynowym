import random

z = int(input("Enter the number of tries:"))

counter = 0

for _ in range(z):
    X = random.betavariate(91,11)
    Y = random.betavariate(3,1)

    if X > Y:
        counter += 1
        
print(f"X was larger in {counter*100/z}% of all tests")
