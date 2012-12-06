wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
VerC = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
def check(num):
    if len(num) < 17:
        raise 'too short'
    i = 0
    total = 0
    for x in num[:17]:
        total += int(x) * wi[i]
        i += 1
    print total
    y = total%11
    return VerC[y]

print check('')
