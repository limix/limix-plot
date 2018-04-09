from matplotlib import pyplot as plt
import limix_plot as lp
from numpy import log10

df = lp.load_dataset('gwas')
print(df.head())
lp.manhattan(df)
ax = plt.gca()
plt.axhline(-log10(1e-7), color='red')
ax.set_ylim(2, ax.get_ylim()[1])
plt.show()
