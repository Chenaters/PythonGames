A = [100,10,10,100]

prev2, prev, cur = 0, 0, 0
for i in A:
    cur = max(prev, i + prev2)
    prev2 = prev
    prev = cur
print(cur)