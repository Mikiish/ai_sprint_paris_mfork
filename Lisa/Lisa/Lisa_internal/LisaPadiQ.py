import math
import sympy
import pyadic


class PaddicString:
    """
    Représente une chaîne P-ADIC avec un contexte et une valeur entière interprétée en P-ADIC.
    """

    def __init__(self, context="...", value=0):
        self.context = context  # Par défaut, le contexte est "..."
        self.value = value  # Valeur entière associée à la représentation P-ADIC

    def __repr__(self):
        return f"{self.context}{self.value}"  # Affichage sous forme de chaîne P-ADIC


class PADDIC:
    def __init__(self, base=7, precision=10):
        """
        Initialise le convertisseur P-ADIC avec une base donnée et une précision maximale.
        """
        if base < 2 or not sympy.isprime(base):
            raise ValueError("Le module PADDIC doit avoir une base qui est un nombre premier.")

        self.base = base  # Base P-ADIC générique
        self.precision = precision  # Nombre de chiffres à calculer avant d'ajouter "..." pour le contexte
        self.Zp = self.init_Zp()  # Anneau des entiers p-adiques
        self.Qp = self.init_Qp()  # Corps des nombres p-adiques

    def init_Zp(self):
        """
        Initialise l'anneau des entiers p-adiques Zp.
        """
        return {n for n in range(self.base ** self.precision)}  # Approximation finie

    def init_Qp(self):
        """
        Initialise le corps des nombres p-adiques Qp.
        """
        return {n / (self.base ** k) for n in range(1, self.base ** self.precision) for k in range(self.precision)}

    def int_to_padic(self, number):
        """
        Convertit un entier en écriture P-ADIC jusqu'à la précision définie.
        """
        if number == 0:
            return PaddicString("...0", 0)

        digits = []
        context = "..."
        for _ in range(self.precision):
            digits.append(str(number % self.base))
            number //= self.base
            if number == 0:
                context = ""  # Si l'entier est entièrement représenté, pas besoin de "..."
                break

        return PaddicString(context, int(''.join(digits[::-1])))

    def base_p_to_padic(self, base_p_string):
        """
        Convertit une chaîne en base P en écriture P-ADIC.
        """
        if not all(char in map(str, range(self.base)) for char in base_p_string):
            raise ValueError(f"La chaîne doit être en base {self.base}.")

        number = int(base_p_string, self.base)
        return self.int_to_padic(number)

    def token_to_padic(self, token):
        """
        Convertit un token en écriture P-ADIC avec gestion du contexte.
        """
        if not isinstance(token, int) or token < 0:
            raise ValueError("Le token doit être un entier positif.")

        return self.int_to_padic(token)

    def valuation_padic(self, number):
        """
        Retourne la valuation P-ADIC de `number`.
        La valuation p-adique v_p(n) est le plus grand entier k tel que p^k divise n.
        """
        if number == 0:
            return math.inf  # Convention pour la valuation de 0

        k = 0
        while number % self.base == 0:
            number //= self.base
            k += 1
        return k

    def distance_padic(self, x, y):
        """
        Calcule la distance P-ADIC entre x et y.
        d_p(x, y) = base^(-v_p(x - y))
        """
        diff = abs(x - y)
        valuation = self.valuation_padic(diff)
        return self.base ** (-valuation) if valuation != math.inf else 0


# Exemple d'utilisation
if __name__ == "__main__":
    padic_converter = PADDIC(7, 10)

    print(f"Entier 1234 en {padic_converter.base}-ADIC:", padic_converter.int_to_padic(1234))
    print(f"1230321 en Base 7, en {padic_converter.base}-ADIC:", padic_converter.base_p_to_padic("1230321"))
    print(f"Token en {padic_converter.base}-ADIC:", padic_converter.token_to_padic(27))
    print(f"Valuation {padic_converter.base}-ADIC de 64:", padic_converter.valuation_padic(64))
    print(f"Distance {padic_converter.base}-ADIC entre 64 et 68:", padic_converter.distance_padic(64, 68))
    print(f"Anneau des entiers {padic_converter.base}-adiques Zp:", padic_converter.Zp)
    print(f"Corps des nombres {padic_converter.base}-adiques Qp:", padic_converter.Qp)
