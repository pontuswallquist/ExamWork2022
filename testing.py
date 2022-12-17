from collections import deque

arr = deque([1,2,3], maxlen=3)

arr2 = deque([], maxlen=3)


if arr:
    print("arr is not empty")
else:
    print("arr is empty")

if arr2:
    print("arr2 is not empty")
else:
    print("arr2 is empty")