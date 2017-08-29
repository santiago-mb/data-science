import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import seaborn as sns

atleta, sol, nublado, lluvia = np.loadtxt('tiempos.txt', skiprows = 1, unpack = True)

# Primera vista de los datos
# colors = plt.cm.rainbow(np.linspace(0, 1, 3))
# plt.scatter(atleta, sol, label = 'sol', color=colors[0])
# plt.scatter(atleta, nublado, label = 'nublado', color=colors[1])
# plt.scatter(atleta, lluvia, label = 'lluvia', color=colors[2])
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.show()

# Shapiro test for normality
# H0 = Distribucion normal de sol
# No rechazo
w, p = sc.stats.shapiro(sol)
print 'shapiro sol'
print w, p

# H0 = Distribucion normal de nublado
# No rechazo
w, p = sc.stats.shapiro(nublado)
print 'shapiro nublado'
print w, p

# H0 = Distribucion normal de lluvia
# No rechazo
w, p = sc.stats.shapiro(lluvia)
print 'shapiro lluvia'
print w, p

# Como hacer el F-Test???

FSolLluvia = np.var(sol) / np.var(lluvia)
FNubladoLluvia = np.var(nublado) / np.var(lluvia)
FSolNublado = np.var(sol) / np.var(nublado)

dfSol = len(sol) - 1
dfLluvia = len(lluvia) - 1
dfNublado = len(nublado) - 1

pSL = sc.stats.f.sf(FSolLluvia, dfSol, dfLluvia)
pNL = sc.stats.f.sf(FNubladoLluvia, dfNublado, dfLluvia)
pSN = sc.stats.f.sf(FSolNublado, dfSol, dfNublado)

print 'f-test sol-lluvia'
print pSL
print 'f-test nublado-lluvia'
print pNL
print 'f-test sol-nublado'
print pSN

# T-Test Welch (independiente sin varianzas iguales)
# H0 = Distribucion sol lluvia con igual media
# Rechazo
t, p = sc.stats.ttest_ind(sol, lluvia, False)
print 't-test welch sol-lluvia'
print t, p

# # H0 = Distribucion sol nublado con igual media
# # No rechazo
# t, p = sc.stats.ttest_ind(sol, nublado, False)
# print 't-test welch sol-nublado'
# print t, p

# H0 = Distribucion lluvia nublado con igual media
# Rechazo
t, p = sc.stats.ttest_ind(lluvia, nublado, False)
print 't-test welch lluvia-nublado'
print t, p

# T-Test apareados
# H0 = Distribucion sol nublado con igual media
# No rechazo
t, p = sc.stats.ttest_rel(sol, nublado)
print 't-test apareados sol-nublado'
print t, p

# # H0 = Distribucion sol lluvia con igual media
# # Rechazo
# t, p = sc.stats.ttest_rel(sol, lluvia)
# print 't-test apareados sol-lluvia'
# print t, p

# # H0 = Distribucion lluvia nublado con igual media
# # Rechazo
# t, p = sc.stats.ttest_rel(lluvia, nublado)
# print 't-test apareados lluvia-nublado'
# print t, p

# Si no valen las hipotesis, corremos WILCOXON
# t, p = sc.stats.wilcoxon(sol, nublado)
# print 'wilcoxon sol-nublado'
# print t, p

t, p = sc.stats.wilcoxon(sol, lluvia)
print 'wilcoxon sol-lluvia'
print t, p

t, p = sc.stats.wilcoxon(lluvia, nublado)
print 'wilcoxon lluvia-nublado'
print t, p

# Test de correlacion Pearson
# Coeficiente de correlacion
# Correlacion alta
t, p = sc.stats.pearsonr(sol, nublado)
print 'pearsonr sol-nublado'
print t, p

# Coeficiente de correlacion
# Correlacion nula
t, p = sc.stats.pearsonr(sol, lluvia)
print 'pearsonr sol-lluvia'
print t, p

# Coeficiente de correlacion
# Correlacion nula
t, p = sc.stats.pearsonr(lluvia, nublado)
print 'pearsonr lluvia-nublado'
print t, p

# Varianza en dias de lluvia
print 'varianza sol'
print np.var(sol)
print 'varianza nublado'
print np.var(nublado)
print 'varianza lluvia'
print np.var(lluvia)

# Permutation Test!!!
# Si resta > 0 entonces lluvia > sol
# Si resta < 0 entonces lluvia < sol
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
