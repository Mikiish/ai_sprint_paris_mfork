# BrochetCore - Mode Lundie : Activation 7h00

Ce mini-projet illustre une approche « diviser pour mieux régner » en C, où chaque cœur du CPU manipule un morceau de buffer.

## 1. Points de réflexion et tâches associées

1. **Affinité CPU** – bien isoler les threads pour éviter la préemption sauvage.  
   _Tâche :_ tester sur différents processeurs pour vérifier l'efficacité.
2. **Récursivité contrôlée** – la pile peut vite gonfler.  
   _Tâche :_ surveiller l'utilisation mémoire et fixer une profondeur limite.
3. **Génération aléatoire** – `getrandom()` puise directement dans l'entropie du noyau.
   _Tâche :_ vérifier les performances par rapport à `rand()`.
4. **Synchronisation** – ici, on `join` systématiquement.  
   _Tâche :_ envisager une file de tâches pour réutiliser les threads.
5. **Taille du buffer** – que se passe-t-il si l'utilisateur demande 10^9 paires ?  
   _Tâche :_ ajouter des vérifications de limites.
6. **Gestion des erreurs** – on affiche un message, mais on pourrait retourner un code clair.  
   _Tâche :_ factoriser la gestion des retours `pthread_*`.
7. **Portabilité** – `pthread_setaffinity_np` est spécifique à Linux.  
   _Tâche :_ prévoir un fallback pour d’autres OS.

## 2. Rôle des fonctions

- **`assign_thread_to_core`** : fixe l’affinité du thread courant à un cœur précis.
- **`fill_buffer_worker`** : gère la portion de buffer confiée à un thread.
- **`recursive_buffer_fill`** : divise le travail en deux, lance deux threads et recommence.
- **`main`** : point d’entrée, alloue le buffer et enclenche la récursion.

## 3. Bibliothèques utilisées

- `pthread.h` : pour la gestion de threads POSIX.
- `sched.h` : pour l’affinité CPU.
- `stdint.h` : types entiers précis (uint8_t).
- `sys/random.h` : accès à `getrandom()` pour des octets sûrs.
- `unistd.h` : `sysconf` pour connaître le nombre de cœurs.

## 4. Compilation

```bash
gcc brochetcore.c -o brochetcore -lpthread
./brochetcore 8
```

## 5. Explication des blocs de code

Chaque fonction est commentée dans le fichier source pour éviter toute surprise à la lecture. Les étapes principales sont :

1. Initialisation et allocation du buffer.
2. Placement des threads sur des cœurs distincts.
3. Lecture d’octets aléatoires via `getrandom()`.
4. Appel récursif jusqu’à traiter la dernière paire.
5. Nettoyage et message de succès.

## 6. Mot de la fin

> *"Bon courage, tu vas en avoir besoin. Les threads, c’est magique, jusqu’à ce qu’ils se rebellent."*

