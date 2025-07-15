# hexentropy_v1

Cette version expérimente une stratégie légèrement différente pour générer une chaîne hexadécimale en remplissant un buffer partagé via plusieurs threads.

## 7 points de réflexion (et tâches associées)
1. **Recursion contrôlée** – Seuls les cas pairs repartent récursivement sur `(n-1)/2`.
   *Tâche : mesurer la profondeur optimale en fonction du nombre de cœurs.*
2. **Cas impair simplifié** – On se contente de deux threads de remplissage plus le tirage central.
   *Tâche : vérifier si ce choix réduit réellement la contention.*
3. **Gestion du milieu** – Le byte central est tiré avec `random_bit` (`0x00` ou `0x07`).
   *Tâche : observer la distribution obtenue sur de grands volumes.*
4. **Limites de tailles** – `SMALL_CHUNK` impose un seuil sous lequel on évite les threads.
   *Tâche : ajuster ce seuil pour ne pas gaspiller de ressources.*
5. **Surcharge des threads** – Multiplier les cœurs peut épuiser la machine.
   *Tâche : prévoir un mécanisme de quota ou de thread pool.*
6. **Portabilité de getrandom** – Certains systèmes ne l’implémentent pas.
   *Tâche : proposer une alternative basée sur `/dev/urandom` le cas échéant.*
7. **Comparaison C vs C++** – C++ offrirait `std::thread` mais peut générer un peu de surcoût.
   *Tâche : développer une variante C++ pour juger sur pièce.*

## Rôle global des fonctions
- `random_bit` : renvoie un bit aléatoire.
- `fill_random` : lecture séquentielle de `len` octets aléatoires.
- `fill_random_thread` : simple enveloppe pour lancer `fill_random` dans un thread.
- `hexentropy_worker` : coeur récursif qui applique la stratégie pair/impair.
- `main` : prépare le buffer, lance la première tâche et affiche le résultat.

## Explications par blocs de code
1. **Inclusions & structure** – on importe les bibliothèques de base et on définit `WorkerCtx` pour partager les paramètres.
2. **Constantes** – `MAX_DEPTH` et `SMALL_CHUNK` bornent respectivement la profondeur et la granularité minimum.
3. **random_bit** – lit un octet via `getrandom` et renvoie son bit de poids faible.
4. **fill_random** – remplissage linéaire utilisé dans les cas de base.
5. **fill_random_thread** – petite fonction pour lancer `fill_random` en thread.
6. **hexentropy_worker** – selon la parité, lance soit de nouveaux workers (pair), soit des threads simples (impair) après avoir écrit le byte central.
7. **main** – parse l’argument `n`, alloue la mémoire et affiche la chaîne finale au format hexadécimal.

## Compilation
```bash
gcc -pthread hexentropy_v1.c -o hexentropy_v1
```

---
Bon courage, tu vas en avoir besoin.
