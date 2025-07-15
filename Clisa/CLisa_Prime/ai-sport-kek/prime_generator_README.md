# prime_generator

Ce dossier rassemble une petite démonstration en C d'un pipeline "corcellique" pour générer des nombres premiers en parallèle.

## 1. Points de réflexion imaginaires
1. **Montée exponentielle** – doubler les threads à chaque appel finit par saturer la machine.
   *Tâche : limiter la profondeur (`MAX_DEPTH`) pour rester sous 128 threads.*
2. **Granularité minimale** – inutile de lancer un thread pour un seul octet.
   *Tâche : ajuster `MIN_CHUNK` selon la taille voulue des nombres.*
3. **Uniformité de l'entropie** – `getrandom` fournit des bytes sûrs mais bloquants.
   *Tâche : prévoir une option non bloquante pour les tests rapides.*
4. **Miller‑Rabin déterministe** – avec les bases prédéfinies, on couvre tout l'espace 64 bits.
   *Tâche : valider le code sur plusieurs plateformes (ARM, x86).* 
5. **Affichage en hexadécimal** – plus lisible qu'un entier brut.
   *Tâche : ajouter un mode `--quiet` pour benchmarker sans sorties inutiles.*
6. **Boucle infinie** – on pourrait continuer tant qu'un signal externe n'arrive pas.
   *Tâche : intégrer une interruption propre (Ctrl+C) avec `sigaction`.*
7. **Extension GPU** – un futur module pourrait analyser les motifs trouvés.
   *Tâche : esquisser une API pour transmettre les candidats vers un GPU.*

## 2. Rôle global des fonctions
- `fill_random` : lit des octets aléatoires depuis le noyau.
- `worker_func` : répartit récursivement le remplissage du buffer sur plusieurs threads.
- `mod_mul` et `mod_pow` : outils arithmétiques pour le test de primalité.
- `is_probable_prime` : implémente Miller‑Rabin pour 64 bits.
- `to_hex` : transforme un tableau d'octets en chaîne hexadécimale.
- `main` : boucle de génération et d'affichage des nombres premiers.

## 3. Bibliothèques utilisées
- `pthread.h` : threads POSIX.
- `sys/random.h` : accès à `getrandom`.
- `stdint.h` : types entiers précis.
- `stdio.h`, `stdlib.h`, `string.h` : classiques de la libc.

## 4. Compilation
```bash
gcc -pthread prime_generator.c -o prime_generator
```

## 5. Explications par blocs de code
Chaque section du fichier source est précédée d'un commentaire décrivant sa fonction : structure `Worker`, helpers arithmétiques, puis boucle principale. Suivez-les pour comprendre la logique pas à pas.

---
*Bon courage, tu vas en avoir besoin.*
