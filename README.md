# 🧠 AI Sprint Paris — Zeph to Triton Project

Bienvenue dans le projet **ai_sprint_paris**, un joyeux chaos d’optimisation, de portage, et de curiosité algorithmique.

## 📦 Objectif

Porter progressivement un code existant (actuellement en Python/Zeph) vers un backend **C** intermédiaire, en vue d'une réécriture **complète en Triton** pour tirer parti de l’accélération GPU MI300X.

Ce projet vise à :
- Nettoyer, structurer et rationaliser le code original (Lisa, Clisa, etc.)
- Traduire les modules critiques en C, pour un contrôle plus fin
- Évaluer la faisabilité d’un portage vers **Triton** (langage de programmation pour GPU par OpenAI)
- Optimiser les kernels et explorer leur exécution dans un espace mémoire non-euclidien (oui, c’est sérieux)

## 🔧 Stack actuelle

- Python 3.10+
- Triton (à intégrer)
- C (pour les modules traduits à la main)
- GitHub Copilot / Codex (pour test de génération Triton assistée)
- MI300X (quand on a accès 🙏)

## 🔀 Forks inclus

Ce dépôt inclut plusieurs **forks personnalisés** des projets suivants :

- [`Triton`](https://github.com/mikiish/triton) — pour modifier la compilation GPU au plus bas niveau
- [`Popcorn CLI`](https://github.com/mikiish/popcorn-cli) — utilisé pour le benchmarking et le profiling
- [`VLLM`](https://github.com/mikiish/vllm) — fork du hackathon AMD, modifié pour nos tests

> **Note :** Ces forks doivent être **mis à jour manuellement** depuis les projets upstream.  
> L’objectif est de pouvoir modifier librement sans dépendre d’un cycle de release officiel.

### 🔄 Mettre à jour un fork :

```bash
cd vllm/
git remote add upstream https://github.com/vllm-project/vllm.git
git fetch upstream
git merge upstream/main



