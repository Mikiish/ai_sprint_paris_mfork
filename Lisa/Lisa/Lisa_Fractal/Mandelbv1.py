import numpy as np
import matplotlib.pyplot as plt

def plot_mandelbrot(center=(-0.75, 0.1), zoom=1, size=800, max_iter=500):

    # Taille du zoom
    scale = 3.5 / zoom
    xmin, xmax = center[0] - scale/2, center[0] + scale/2
    ymin, ymax = center[1] - scale/2, center[1] + scale/2

    # Création du plan complexe
    x = np.linspace(xmin, xmax, size)
    y = np.linspace(ymin, ymax, size)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros(C.shape, complex)
    divergence = np.zeros(Z.shape, dtype=int)

    # Itération
    for i in range(max_iter):
        Z = Z**2 + C
        diverge = np.abs(Z) > 2
        divergence[diverge & (divergence == 0)] = i
        Z[diverge] = 2

    # Affichage
    plt.figure(figsize=(8,8))
    plt.imshow(divergence, extent=[xmin, xmax, ymin, ymax], cmap='twilight_shifted')
    plt.colorbar(label='Itérations avant divergence')
    plt.title(f"Zoom x{zoom} vers {center}")
    plt.xlabel("Re")
    plt.ylabel("Im")
    plt.show()

# Exemple d'utilisation :
plot_mandelbrot(center=(-0.743643887037158704752191506114774, 0.131825904205311970493132056385139), zoom=1000, max_iter=1000)
