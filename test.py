list1 = [[1, 7, 8], [9, 7, 102], [102, 106, 105], [100, 99, 98, 103], [1, 2, 3]]
total = 0
counter = 0
for i in list1:
    for num in i:
        total += num

for li in list1:
    counter += len(li)

print(total / counter)
