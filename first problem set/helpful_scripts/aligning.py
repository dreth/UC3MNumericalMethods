# plot the feasible region
d = np.linspace(-2, 16, 300)
x, y = np.meshgrid(d, d)
plt.imshow(((y >= 2) & (2*y <= 25-x) & (4*y >= 2*x-8) & (y <= 2*x-5)).astype(int),
           extent=(x.min(), x.max(), y.min(), y.max()), origin="lower", cmap="Greys", alpha=0.3)
