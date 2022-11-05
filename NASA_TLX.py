
Categories = ["MD", "PD", "TD", "P", "E", "F"]

freq = [0, 0, 0, 0, 0, 0]

scores = [4,5,4,4,4,7]


for i in range(6):
    for j in range( i+1, 6):
        if scores[i] > scores[j]:
            freq[i] += 1
        else:
            freq[j] += 1    


print(freq)            

total_freq = sum(freq)

score = 0

for i in range(6):
    score += ( scores[i] * 10 * ( freq[i] / total_freq ) )

print(score)    