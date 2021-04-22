import copy
a = [1,2]
b = copy.deepcopy(a)
b.append(3)
print(a)