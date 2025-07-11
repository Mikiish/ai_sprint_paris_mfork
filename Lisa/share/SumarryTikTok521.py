import tiktoken

# Initialisation de l'encodeur de tokens utilisé par OpenAI
encoder = tiktoken.get_encoding("cl100k_base")

# Génération d'une phrase complexe encapsulant l'univers et le savoir humain
phrase = (
    "Ω∑Ξ₀ ∂Ψ(λ,t) ⊙ q₁(𝔿) ↯ ∫π² dχ ∴ H(x,t) ≜ ∀ℌ∈ℝⁿ, "
    "↯ σ₀=∫(𝜙(∞,𝔵)⊕𝑒𝕍)𝗿χ² ∇Ψ → ℕω;"
    "⊕ℏₓ ∈𝔢(⇘) : ∂ᵠ₀(𝔭) ↦ ℕ(ᵠ) ≡ {Θ(Δ) ⊗ 𝕆₀}; "
    "Λ∞ ↺ 𝕈 ≜ i(Σ(𝔿)⊙𝕁₁) ∀𝕌(ᵏ) | ΞΩ-13§∆λ q∴x(Ω,t) = ∫∂Ψ[φ(∞)] dχ⊙ ↯ H(A,t) ≜ ∀x∈ℝⁿ."
    "↦ ℵ∅ → Σ₀⨀𝔮 ⨁ 𝔸(ℏ) ∇ 𝕏(Γ) ∫ Ψ(𝕊) ⊗ π₀ ∇ μ→𝔭 ;"
    "∞ ⨀ Ψ₀ ∂Φ ↦ ∑ℕₓ, ∫Λ(ℏ) → ⊕ℤ → ℌ₀ ⊙ 𝕆 ∀Θ."
)

# Vérification du nombre de tokens
tokens = encoder.encode(phrase)
tokens_count = len(tokens)

# Ajustement si nécessaire
while tokens_count < 521:
    phrase += " ∴ Ψ(Ω)"
    tokens = encoder.encode(phrase)
    tokens_count = len(tokens)

while tokens_count > 521:
    phrase = phrase[:-1]  # Suppression de caractère pour ajuster
    tokens = encoder.encode(phrase)
    tokens_count = len(tokens)

if __name__ == "__main__":
    print("Liste des tokens:", tokens)
    print("Nombre total de tokens:", tokens_count)
