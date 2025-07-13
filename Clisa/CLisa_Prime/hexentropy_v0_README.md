# hexentropy_v0

Ce programme expérimente une génération récursive et multithreadée d'une chaîne hexadécimale de longueur `n`. On vise surtout la vitesse brute sur des machines très dotées en cœurs CPU.

## 7 points de réflexion (et tâches associées)
1. **Contrôle de la profondeur** –
   Limiter `MAX_DEPTH` évite une explosion de threads.
   *Tâche : ajuster cette constante selon le matériel.*
2. **Granularité minimum** –
   Passer en mode séquentiel pour les petits blocs (`SMALL_CHUNK`).
   *Tâche : mesurer l'impact sur la performance et ajuster.*
3. **Pile ou face systématique** –
   Chaque niveau insère un octet tiré au sort (`0x00` ou `0x07`) avant de
   répartir le reste.
   *Tâche : tester l'impact sur la répartition en équilibrant `n-1`.*
4. **Risque de contention mémoire** –
   Plusieurs threads écrivent dans un même buffer.
   *Tâche : profiler l'impact sur de grandes tailles.*
5. **Compatibilité système** –
   `getrandom` n'existe pas partout.
   *Tâche : prévoir une alternative (ex. `/dev/urandom`).*
6. **Rapport avec Miller-Rabin** –
   On vise une génération plus rapide que la vérification de primalité.
   *Tâche : mesurer le temps par rapport à une implémentation de Miller-Rabin.*
7. **C vs C++** –
   Le C est minimaliste, C++ offre plus d'abstractions (threads plus simples, RAII).
   *Tâche : tester une version C++ pour comparer la latence et le confort de code.*

## Fonctions principales
- `random_bit` : récupère un bit aléatoire via `getrandom`.
- `fill_random` : remplit séquentiellement un morceau du buffer.
- `hexentropy_worker` : fonction récursive appelée par chaque thread.
- `main` : parse la taille, alloue le buffer et lance la génération.

## Explications par blocs
1. **Inclusions** – on embarque `stdio.h`, `stdlib.h`, `pthread.h`,
   `sys/random.h` et `string.h` pour avoir les appels système et les threads.
2. **Structure WorkerCtx** – trois champs pour passer le buffer, la taille
   courante et la profondeur aux threads.
3. **Constantes** – `MAX_DEPTH` limite la récursivité, `SMALL_CHUNK` évite de
   créer trop de threads pour des broutilles.
4. **random_bit** – un appel `getrandom` d'un octet, on ne garde que le bit de
   poids faible pour le tirage pile ou face.
5. **fill_random** – lecture séquentielle de `len` octets aléatoires.
6. **hexentropy_worker** – coeur récursif : décision pair/impair, lancement de
   deux threads et écriture du byte central.
7. **main** – allocation du buffer, déclenchement du premier appel et affichage
   final sous forme hexadécimale.

## Compilation
```bash
gcc -pthread hexentropy_v0.c -o hexentropy_v0
```

## Un mot sur C vs C++
Le C permet un contrôle très direct (pas de surprise côté allocation), ce qui peut être un avantage en latence pure. C++ apporte toutefois des abstractions utiles (std::thread, containers, RAII) qui simplifient l'écriture et peuvent éviter des fuites ou des erreurs. La surcharge en performance est généralement négligeable pour ce type de tâches, surtout avec un code bien optimisé.

---
Bon courage, tu vas en avoir besoin.
