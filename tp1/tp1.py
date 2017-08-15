import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import seaborn as sns

atleta, sol, nublado, lluvia = np.loadtxt("tiempos.txt", skiprows = 1, unpack = True)

plt.scatter(atleta, sol, label = 'sol')
plt.scatter(atleta, nublado, label = 'nublado')
plt.scatter(atleta, lluvia, label = 'lluvia')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

t, p = sc.stats.ttest_rel(sol, nublado)
print 't-test apareados sol-nublado'
print t
print p

t, p = sc.stats.ttest_rel(sol, lluvia)
print 't-test apareados sol-lluvia'
print t
print p

t, p = sc.stats.ttest_rel(lluvia, nublado)
print 't-test apareados lluvia-nublado'
print t
print p

t, p = sc.stats.wilcoxon(sol, nublado)
print 'wilcoxon sol-nublado'
print t
print p

t, p = sc.stats.wilcoxon(sol, lluvia)
print 'wilcoxon sol-lluvia'
print t
print p

t, p = sc.stats.wilcoxon(lluvia, nublado)
print 'wilcoxon lluvia-nublado'
print t
print p

t, p = sc.stats.ttest_1samp(lluvia, np.mean(lluvia))
print 't-test unica lluvia'
print t
print p


# NO SIRVE
# t, p = sc.stats.ttest_1samp(sol, np.mean(sol))
# print 't-test unica sol'
# print t
# print p

# t, p = sc.stats.ttest_1samp(nublado, np.mean(nublado))
# print 't-test unica nublado'
# print t
# print p

# t, p = sc.stats.pearsonr(sol, nublado)
# print 'pearsonr sol-nublado'
# print t
# print p

# print atleta
# print sol
# print nublado
# print lluvia
