# hexentropy_v1

Cette version expérimente une stratégie légèrement différente pour générer une chaîne hexadécimale en remplissant un buffer partagé via plusieurs threads.

## 7 points de réflexion (et tâches associées)
1. **Division équilibrée** – Les longueurs paires sont coupées en deux segments identiques récursifs.
   *Tâche : mesurer la profondeur optimale en fonction du nombre de cœurs.*
2. **Cas impair** – On place un nibble aléatoire au centre puis on lance la récursion sur les deux moitiés.
   *Tâche : vérifier si ce choix réduit réellement la contention.*
3. **Gestion du milieu** – Le byte central provient de `rand_hexbit` (valeur 0‑15).
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
- `rand_hexbit` : génère une valeur aléatoire sur 4 bits.
- `hexentropy_worker` : coeur récursif qui applique la stratégie pair/impair uniquement via la récursion.
- `main` : prépare le buffer, lance la première tâche et affiche le résultat.

## Explications par blocs de code
1. **Inclusions & structure** – on importe les bibliothèques de base et on définit `WorkerCtx` pour partager les paramètres.
2. **Constantes** – `MAX_DEPTH` et `SMALL_CHUNK` bornent respectivement la profondeur et la granularité minimum.
3. **random_bit** – lit un octet via `getrandom` et renvoie son bit de poids faible.
4. **fill_random** – remplissage linéaire utilisé dans les cas de base.
5. **rand_hexbit** – renvoie un demi‑octet aléatoire.
6. **hexentropy_worker** – applique la division paire/impair entièrement via la récursion.
7. **main** – parse l’argument `n`, alloue la mémoire et affiche la chaîne finale au format hexadécimal.

## Compilation
```bash
gcc -pthread hexentropy_v1.c -o hexentropy_v1
```

---
Bon courage, tu vas en avoir besoin.
