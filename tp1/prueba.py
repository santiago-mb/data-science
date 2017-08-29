import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import seaborn as sns

sol = [162, 171, 157]
lluvia = [181, 187, 161, 165, 174]

delta0 = np.mean(lluvia) - np.mean(sol)
deltas = [delta0]
lluviaAndSol = np.append(sol, lluvia)
labels = [True for i in range(len(sol))] + [False for i in range(len(lluvia))]

for _ in range(1001):
  np.random.shuffle(labels)
  solC = 0
  lluviaC = 0
  for i in range(len(labels)):
    if labels[i]:
      solC += lluviaAndSol[i]
    else:
      lluviaC += lluviaAndSol[i]
  solC /= float(len(sol))
  lluviaC /= float(len(lluvia))
  deltas.append(lluviaC - solC)

values, bins, _ = plt.hist(deltas)
areaTotal = sum(np.diff(bins)*values)
indice = next(i for i in range(len(bins)) if (lambda y : y >= delta0)(bins[i]))

newBins = [delta0]
newBins += bins[indice:]
newValues = values[indice-1:]

areaDerecha = sum(np.diff(newBins)*newValues)

print areaDerecha / areaTotal
# plt.hist(deltas)
plt.axvline(delta0, color='red', linestyle='dashed', linewidth=2)
plt.show()
