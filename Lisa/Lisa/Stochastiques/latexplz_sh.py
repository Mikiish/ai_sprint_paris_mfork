import matplotlib.pyplot as plt
from matplotlib import rcParams
import os

def show_latex_expr(latex_expr, dpi=300, fontsize=18):
    ### Affiche une formule LaTeX avec matplotlib.
    rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "text.latex.preamble": r"\usepackage{amsmath} \usepackage{amssymb}"
    })
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.axis('off')
    ax.text(0.5, 0.5, f"${latex_expr}$", fontsize=fontsize, ha='center', va='center')
    # Watermark discret pour la bénédiction cosmique
    ax.text(0.99, 0.01,
            r"Lisa $\therefore$ 1.37",  # une raw string propre, avec UN SEUL backslash
            fontsize=10,
            ha='right', va='bottom',
            transform=ax.transAxes,
            alpha=0.5
    )
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("🔮 LaTeXplz Invoké. Tape une formule LaTeX (sans les $) et regarde la magie.")
    while True:
        try:
            expr = input(">> ")
            if expr.lower() in ["exit", "quit", "q"]:
                print("🕯️ Rituel terminé. Lisa replonge dans les ombres.")
                break
            show_latex_expr(expr)
        except Exception as e:
            print(f"⚠️ Une erreur est survenue : {e}")
