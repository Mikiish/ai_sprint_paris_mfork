# prime_pipeline

Cette expérimentation reprend l'idée de `hexentropy_v1.c` pour la pousser vers un petit générateur de nombres premiers. On reste raisonnable : tout est en C avec `pthread` et `getrandom`.

## 7 points de réflexion et tâches associées
1. **Recursion à deux branches** – chaque appel divise le buffer en deux moitiés.
   *Tâche : mesurer l'impact sur la consommation CPU en fonction de `MAX_DEPTH`.*
2. **Seuil `SMALL_CHUNK`** – en dessous, on arrête de créer des threads.
   *Tâche : ajuster ce seuil pour optimiser les petites tailles de nombre.*
3. **Pipeline simplifié** – après génération, on applique directement Miller‑Rabin.
   *Tâche : comparer le temps passé en génération vs. en test de primalité.*
4. **Parallélisme en lot** – `main` lance plusieurs `prime_worker` en parallèle.
   *Tâche : jouer sur le nombre de workers pour saturer le CPU.*
5. **Conversion en entier** – on lit les octets sous forme little-endian.
   *Tâche : vérifier l'endianess si on change de plateforme.*
6. **Miller‑Rabin déterministe 64 bits** – bases fixes pour éviter les faux positifs.
   *Tâche : étendre la fonction pour des entiers plus grands si nécessaire.*
7. **Allocation et libération** – chaque worker alloue son propre buffer.
   *Tâche : mettre en place un pool mémoire pour limiter les malloc/free.*

## Rôle global des fonctions
- **random_byte / fill_random** : obtiennent de l'entropie système.
- **fill_random_thread** : minuscule wrapper pour `pthread_create`.
- **entropy_worker** : coeur récursif qui divise le travail en deux.
- **buf_to_u64** : transforme un tableau d'octets en entier 64 bits.
- **mod_pow** : exponentiation modulaire via `__uint128_t`.
- **is_probably_prime** : test de primalité de Miller‑Rabin.
- **prime_worker** : génère un nombre, l'affiche et indique s'il est premier.

## Explications par blocs
Chaque bloc du fichier source est précédé d'un commentaire décrivant son objectif. On retrouve : la définition du contexte, les constantes de contrôle, la génération aléatoire, le découpage récursif, la partie mathématique et enfin la boucle principale qui orchestre plusieurs threads.

## Bibliothèques utilisées
- `pthread.h` pour le multithreading.
- `sys/random.h` pour `getrandom`.
- `stdint.h` et `stdio.h` pour les types entiers et l'affichage.

## Compilation
```bash
gcc -pthread prime_pipeline.c -o prime_pipeline
```
L'exécutable accepte trois arguments optionnels : `count` (nombres à générer), `workers` (threads parallèles) et `bytes` (taille en octets).

## Fin mot sarcastico‑pédagogique
Bon courage, tu vas en avoir besoin pour atteindre les dix milliards de nombres premiers. Et pense à surveiller la température de la machine !

