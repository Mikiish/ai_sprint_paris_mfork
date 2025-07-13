# Hexentropy Tree — Mode Lundie

Cet examen fictif dissèque `hexentropy_tree.c` et propose un squelette à remplir.
Chaque point ci‑dessous est assorti d’une petite tâche de développement.

## 1. Points de réflexion et tâches associées

1. **L’entropie à la source**
   - *Tâche:* coder `flip_coin` pour renvoyer un bit réel via `getrandom`.
2. **La structure partagée**
   - *Tâche:* définir correctement `ThreadContext` avec profondeur, longueur et offset.
3. **La base de la récursion**
   - *Tâche:* gérer le cas de base dans `binary_mutant_worker` en remplissant le segment de manière aléatoire.
4. **Le cœur mutant**
   - *Tâche:* insérer 0x08 ou 0x07 selon `flip_coin` pour former le motif hexadécimal.
5. **Les embranchements parallèles**
   - *Tâche:* créer deux threads enfants et leur passer les contextes gauche et droit.
6. **La racine de l’arbre**
   - *Tâche:* allouer le buffer principal dans `main` et lancer le premier thread.
7. **L’affichage final**
   - *Tâche:* parcourir le buffer pour afficher les octets en hexadécimal.

## 2. Bibliothèques utilisées
- `<pthread.h>` : gestion des threads POSIX.
- `<sys/random.h>` : accès à l’entropie du noyau.
- `<stdio.h>` / `<stdlib.h>` : classiques entrée–sortie et allocation.

## 3. Rôle global des fonctions
- **`flip_coin`** : fournit un bit aléatoire.
- **`binary_mutant_worker`** : construit l’arbre de manière récursive et parallèle.
- **`main`** : orchestre le lancement du premier thread et imprime le résultat.

## 4. Explication par blocs
1. **Macros et includes** – limitent la profondeur de récursion et définissent la taille du motif.
2. **Structure `ThreadContext`** – transporte les informations nécessaires à chaque thread.
3. **Fonction `flip_coin`** – lit un octet depuis le noyau et renvoie son bit de poids faible.
4. **Fonction `binary_mutant_worker`** – si la taille du segment est trop petite ou la profondeur trop grande, on génère des octets aléatoires; sinon on sépare le segment, insère un motif puis on crée deux threads récursifs.
5. **Fonction `main`** – alloue le buffer, démarre la récursion et affiche le contenu en hexadécimal.

## 5. Compilation rapide
```bash
gcc -Wall -Wextra -pthread hexentropy_tree.c -o hexentropy_tree
./hexentropy_tree
```

---
Bon courage, tu vas en avoir besoin : les threads ont tendance à se rebeller si on les désynchronise.
