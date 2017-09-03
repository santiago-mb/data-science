import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import seaborn as sns

atleta, sol, nublado, lluvia = np.loadtxt('tiempos.txt', skiprows = 1, unpack = True)

# Primera vista de los datos
colors = plt.cm.rainbow(np.linspace(0, 1, 10))
ax = plt.subplot(111)
ax.scatter(atleta, sol, label = 'sol', color=colors[2])
ax.scatter(atleta, nublado, label = 'nublado', color=colors[8])
ax.scatter(atleta, lluvia, label = 'lluvia', color=colors[7])
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.savefig('scatter_clean.png')
plt.close()

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
FLluviaSol = np.var(lluvia) / np.var(sol)
FNubladoLluvia = np.var(nublado) / np.var(lluvia)
FLluviaNublado = np.var(lluvia) / np.var(nublado)
FSolNublado = np.var(sol) / np.var(nublado)
FNubladoSol = np.var(nublado) / np.var(sol)

dfSol = len(sol) - 1
dfLluvia = len(lluvia) - 1
dfNublado = len(nublado) - 1

# F-Test
# H0 = Igual varianza sol lluvia
# Rechazo
p = sc.stats.f.sf(FSolLluvia, dfSol, dfLluvia)
p += sc.stats.f.cdf(FLluviaSol, dfLluvia, dfSol)
print 'f-test sol-lluvia dos colas'
print p
# F-Test
# H0 = Igual varianza nublado lluvia
# Rechazo
p = sc.stats.f.sf(FNubladoLluvia, dfNublado, dfLluvia)
p += sc.stats.f.cdf(FLluviaNublado, dfLluvia, dfNublado)
print 'f-test nublado-lluvia dos colas'
print p
# F-Test
# H0 = Igual varianza nublado sol
# No rechazo
p = sc.stats.f.sf(FSolNublado, dfSol, dfNublado)
p += sc.stats.f.cdf(FNubladoSol, dfNublado, dfSol)
print 'f-test sol-nublado dos colas'
print p


# T-Test Welch (independiente sin varianzas iguales)
# H0 = Distribucion sol lluvia con igual media
# Rechazo
t, p = sc.stats.ttest_ind(sol, lluvia, equal_var = False)
print 't-test welch sol-lluvia'
print t, p

# # H0 = Distribucion sol nublado con igual media
# # No rechazo
# t, p = sc.stats.ttest_ind(sol, nublado, equal_var = False)
# print 't-test welch sol-nublado'
# print t, p

# H0 = Distribucion lluvia nublado con igual media
# Rechazo
t, p = sc.stats.ttest_ind(lluvia, nublado, equal_var = False)
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

# # Permutation Test!!!
# # Si resta > 0 entonces lluvia > sol
# # Si resta < 0 entonces lluvia < sol
# delta0 = np.mean(lluvia) - np.mean(sol)
# deltas = [delta0]
# lluviaAndSol = np.append(sol, lluvia)
# labels = [True for i in range(len(sol))] + [False for i in range(len(lluvia))]

# for _ in range(1001):
#   np.random.shuffle(labels)
#   solC = 0
#   lluviaC = 0
#   for i in range(len(labels)):
#     if labels[i]:
#       solC += lluviaAndSol[i]
#     else:
#       lluviaC += lluviaAndSol[i]
#   solC /= float(len(sol))
#   lluviaC /= float(len(lluvia))
#   deltas.append(lluviaC - solC)

# values, bins, _ = plt.hist(deltas)
# areaTotal = sum(np.diff(bins)*values)
# indice = next(i for i in range(len(bins)) if (lambda y : y >= delta0)(bins[i]))

# newBins = [delta0]
# newBins += bins[indice:]
# newValues = values[indice-1:]

# areaDerecha = sum(np.diff(newBins)*newValues)

# print areaDerecha / areaTotal
# # plt.hist(deltas)
# plt.axvline(delta0, color='red', linestyle='dashed', linewidth=2)
# plt.show()

# Permutation Test!!!
# Si resta > 0 entonces lluvia > sol
# Si resta < 0 entonces lluvia < sol
delta0 = np.mean(lluvia) - np.mean(sol)
deltas = [delta0]

for _ in range(1001):
  flips = np.random.choice([True, False], len(sol))
  solC = 0
  lluviaC = 0
  for i in range(len(flips)):
    if flips[i]:
      solC += lluvia[i]
      lluviaC += sol[i]
    else:
      solC += sol[i]
      lluviaC += lluvia[i]
  solC /= float(len(sol))
  lluviaC /= float(len(lluvia))
  deltas.append(lluviaC - solC)

ax = plt.subplot(111)
values, bins, _ = ax.hist(deltas)
areaTotal = sum(np.diff(bins)*values)
indice = next(i for i in range(len(bins)) if (lambda y : y >= delta0)(bins[i]))

newBins = [delta0]
newBins += bins[indice:]
newValues = values[indice:]

areaDerecha = sum(np.diff(newBins)*newValues)

print areaDerecha / areaTotal

box = ax.get_position()
plt.axvline(delta0, color='red', linestyle='dashed', linewidth=2, label = 'p-value')
ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
plt.xlabel('delta')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.savefig('permutation.png')
plt.show()
# plt.close()
