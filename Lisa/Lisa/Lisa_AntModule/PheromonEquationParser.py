import re
import numpy as np


class PheromoneEquationParser:
    def __init__(self):
        # Mappage des expressions mathématiques aux émojis
        self.symbol_map = {
            "∇": "↘️↙️↖️↗️",  # Gradient
            "∂": "💥🔄🌀",  # Divergence
            "∆": "🌊🔥💨",  # Laplacien
            "∫": "➰🔄",  # Intégrale
            "d/dt": "⏳⚡",  # Dérivée
            "v": "🏃‍♂️💨",  # Vitesse
            "D": "🌫️↔️",  # Diffusion
            "ρ": "📦⚖️",  # Densité
            "C": "🧪",  # Concentration
            "R": "⚗️🧪",  # Réaction chimique
            "P": "🐜🍯"  # Phéromone produite par les fourmis
        }

    def parse_equation(self, equation: str) -> str:
        """Convertit une équation mathématique en notation emoji."""
        for symbol, emoji in self.symbol_map.items():
            equation = equation.replace(symbol, emoji)
        return equation

    def generate_equation(self, emoji_equation: str) -> str:
        """Convertit une équation en notation emoji vers notation mathématique."""
        reverse_map = {v: k for k, v in self.symbol_map.items()}
        for emoji, symbol in reverse_map.items():
            emoji_equation = emoji_equation.replace(emoji, symbol)
        return emoji_equation

    @staticmethod
    def parse_pheromone_equation(equation: str) -> str:
        """Convertit une équation mathématique en notation enrichie avec des émojis et relations spécifiques."""
        conversion_dict = {
            "ρ": "⚖️", "J": "📡", "C": "🧪", "U": "⚡", "P": "🌀", "t": "⏳", "T": "🌡️", "x": "📍", "y": "📍", "z": "📍",
            "→": "🔄→", "<-": "←", "⤴️": "⤴️", "↺": "↺", "∇": "🏃‍♂️💨", "∆": "🌫️", "R": "🔥⚗️",
            "∂C/∂t": "∂🧪/∂⏳", "v∇C": "🏃‍♂️💨∇🧪", "D∆C": "🌫️∆🧪", "∫C dt": "∫🧪 dt"
        }
        for key, value in conversion_dict.items():
            equation = equation.replace(key, value)
        return equation


# Test du parser
if __name__ == "__main__":
    parser = PheromoneEquationParser()
    math_eq = "∂C/∂t + v∇C = D∆C + R"
    emoji_eq = parser.parse_equation(math_eq)
    print("Notation Emoji:", emoji_eq)

    # Vérification conversion inverse
    restored_eq = parser.generate_equation(emoji_eq)
    print("Notation Mathématique Restaurée:", restored_eq)

    # Exemple d'utilisation
    equation = "∂C/∂t + v∇C = D∆C + R"
    parsed_equation = parser.parse_pheromone_equation(equation)
    print("Equation enrichie:", parsed_equation)
