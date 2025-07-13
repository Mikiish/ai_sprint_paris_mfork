# hexentropy_v0

Ce programme expérimente une génération récursive et multithreadée d'une chaîne hexadécimale de longueur `n`. On vise surtout la vitesse brute sur des machines très dotées en cœurs CPU.

## 7 points de réflexion (et tâches associées)
1. **Contrôle de la profondeur** –
   Limiter `MAX_DEPTH` évite une explosion de threads.
   *Tâche : ajuster cette constante selon le matériel.*
2. **Granularité minimum** –
   Passer en mode séquentiel pour les petits blocs (`SMALL_CHUNK`).
   *Tâche : mesurer l'impact sur la performance et ajuster.*
3. **Pile ou face hexadécimal** –
   Pour les tailles impaires, un bit aléatoire décide entre `0x00` et `0x07` au centre.
   *Tâche : essayer d'autres valeurs ou un vrai hexadécimal aléatoire.*
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

## Compilation
```bash
gcc -pthread hexentropy_v0.c -o hexentropy_v0
```

## Un mot sur C vs C++
Le C permet un contrôle très direct (pas de surprise côté allocation), ce qui peut être un avantage en latence pure. C++ apporte toutefois des abstractions utiles (std::thread, containers, RAII) qui simplifient l'écriture et peuvent éviter des fuites ou des erreurs. La surcharge en performance est généralement négligeable pour ce type de tâches, surtout avec un code bien optimisé.

---
Bon courage, tu vas en avoir besoin.
