import matplotlib.pyplot as plt

def translate_latex(latex_str):
    replacements = {
        r'P': "Probabilité de",
        r'\mid': "sachant",
        r'X_n': "X à l'étape n",
        r'X_{n-1}': "X à l'étape n-1",
        r'X_{n-2}': "X à l'étape n-2",
        r'X_0': "X à l'étape zéro",
        r'=': "est égal à",
        r'\to': "tend vers",
        r'\infty': "l'infini",
    }
    readable = latex_str
    for key, value in replacements.items():
        readable = readable.replace(key, value)
    return readable
def render_latex_to_image(latex_str, output_file="latex_output.png", dpi=300):
    """Affiche une formule LaTeX proprement avec matplotlib et l'enregistre si besoin."""
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.axis('off')  # Supprime les axes
    # Affiche le texte LaTeX au centre
    ax.text(0.5, 0.5, f"${latex_str}$", fontsize=18, ha='center', va='center')
    # Sauvegarde dans un fichier image si voulu
    plt.tight_layout()
    plt.savefig(output_file, dpi=dpi)
    plt.show()
# Exemple
if __name__ == '__main__':
    latex = r"P(X_n = x_n \mid X_{n-1} = x_{n-1})"
    print(translate_latex(latex))
    render_latex_to_image(r"P(X(t+\epsilon) \mid X(s), 0 < s < t+\epsilon) = P(X(t+\epsilon) \mid X(t))")