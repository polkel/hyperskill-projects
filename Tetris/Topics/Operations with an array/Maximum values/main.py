import numpy as np


list_array = list()
NUM_INPUT = 3
for _ in range(NUM_INPUT):
    list_array.append(int(input()))
array = np.array(list_array)
print(array.max())
print(array.argmax())
