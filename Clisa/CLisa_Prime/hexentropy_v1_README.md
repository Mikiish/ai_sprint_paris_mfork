# hexentropy_v1

Cette version expérimente une stratégie légèrement différente pour générer une chaîne hexadécimale en remplissant un buffer partagé via plusieurs threads.

## 7 points de réflexion (et tâches associées)
1. **Recursion invariable** – Chaque appel scinde le segment en deux et relance deux workers jusqu’à `MAX_DEPTH`.
   *Tâche : mesurer la profondeur maximale supportable selon la machine.*
2. **Motif central aléatoire** – `rand_hexbit` choisit `0x07` ou `0x08` et l’insère à chaque niveau.
   *Tâche : vérifier la distribution obtenue sur de gros volumes.*
3. **Granularité minimum** – Passer en mode séquentiel pour les petits blocs (`SMALL_CHUNK`).
   *Tâche : ajuster ce seuil pour éviter les threads inutiles.*
4. **Risque de contention mémoire** – Plusieurs threads écrivent dans un même buffer.
   *Tâche : profiler l’impact sur de grandes tailles.*
5. **Compatibilité système** – `getrandom` n’existe pas partout.
   *Tâche : prévoir une alternative (ex. `/dev/urandom`).*
6. **Rapport avec Miller-Rabin** – On vise une génération plus rapide que la vérification de primalité.
   *Tâche : comparer les temps avec une implémentation de Miller-Rabin.*
7. **C vs C++** – Le C offre un contrôle fin tandis que C++ facilite la gestion des threads.
   *Tâche : coder une variante C++ pour jauger la latence et le confort.*

## Rôle global des fonctions
- `rand_hexbit` : renvoie `0x07` ou `0x08` de façon uniforme.
- `fill_random` : lecture séquentielle de `len` octets aléatoires.
- `fill_random_thread` : simple enveloppe pour lancer `fill_random` dans un thread.
- `hexentropy_worker` : scinde toujours le segment en deux, insère un octet choisi par `rand_hexbit` puis lance deux nouvelles tâches.
- `main` : prépare le buffer, lance la première tâche et affiche le résultat.

## Explications par blocs de code
1. **Inclusions & structure** – on importe les bibliothèques de base et on définit `WorkerCtx` pour partager les paramètres.
2. **Constantes** – `MAX_DEPTH` et `SMALL_CHUNK` bornent respectivement la profondeur et la granularité minimum.
3. **rand_hexbit** – lit un octet via `getrandom` et renvoie `0x07` ou `0x08`.
4. **fill_random** – remplissage linéaire utilisé dans les cas de base.
5. **fill_random_thread** – petite fonction pour lancer `fill_random` en thread.
6. **hexentropy_worker** – scinde toujours le segment en deux, insère un octet choisi par `rand_hexbit` puis appelle récursivement deux nouveaux workers.
7. **main** – parse l’argument `n`, alloue la mémoire et affiche la chaîne finale au format hexadécimal.

## Compilation
```bash
gcc -std=c11 -pthread hexentropy_v1.c -o hexentropy_v1
```

---
Bon courage, tu vas en avoir besoin.
