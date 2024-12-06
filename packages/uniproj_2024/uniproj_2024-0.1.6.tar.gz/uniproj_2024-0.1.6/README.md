# Mini projet protéomique

Ce projet a pour but la manipulation et l'analyse de données de protéines issues de la base de données Uniprot via l'implémentation de classes Python.

## Classe Uniprot

La classe Uniprot est destinée à représenter une protéine unique avec ses données principales extraites d'un fichier Uniprot au format texte.

### Constructeur

**init(contenu_fichier: str)**
Parse le contenu textuel d'une fiche Uniprot.
Extrait et stocke les informations suivantes sous forme d'attributs :

- id (str) : Identifiant Uniprot de la protéine.
- ac (str) : Numéro AC de la protéine.
- org (str) : Organisme associé à la protéine.
- gene (str) : Nom du gène de la protéine.
- seq (str) : Séquence peptidique de la protéine.
- go (list) : Liste d'identifiants GO associés à la protéine.

### Méthodes

**fasta_dump()**
Exporte la séquence de la protéine au format FASTA dans un fichier nommé [AC].fasta.
La ligne de commentaires commence par > et inclut : l'identification, l'organisme et le nom du gène.

**molecular_weight()** -> float
Calcule et retourne le poids moléculaire de la protéine en Daltons.

**average_hydrophobicity()** -> float
Calcule et retourne l'hydrophobicité moyenne de la séquence de la protéine en utilisant une échelle standardisée.

**occurence_prot()** -> dict
Calcule la fréquence relative des acides aminés dans la séquence de la protéine.
Retourne un dictionnaire où chaque clé est un acide aminé et la valeur associée est la fréquence relative de cet acide aminé.

## Classe Collection

La classe Collection représente un ensemble d'objets Uniprot et fournit des outils pour manipuler, trier et analyser ces objets.

### Constructeur

**init()**
Initialise une collection vide.

### Méthodes

**load_collection(fichier_in: str)**
Charge une collection à partir d'un fichier contenant plusieurs fiches Uniprot séparées par //.

**add(contenu_uniprot: str)**
Crée un objet Uniprot à partir du contenu textuel fourni et l'ajoute à la collection.
Lève une exception si la protéine est déjà présente.

**remove(uniprot_id: str)**
Supprime l'objet Uniprot correspondant à l'identifiant donné.
Lève une exception si l'identifiant est introuvable.

**sort_by_length(reverse=False)**
Trie les objets Uniprot dans la collection par la longueur de leur séquence.

**filter_for_hydrophobic(min_hydro: float)**
Retourne une liste des protéines ayant une hydrophobicité moyenne supérieure à min_hydro.
Ces protéines sont retournées dans un dictionnaire qui permet de pallier aux capacités limitées d'une liste.

Le filtrage expert n'a pas été codé.

**add(other: Collection)** -> Collection
Fusionne deux collections en créant une nouvelle instance sans doublons.

**go_view()** -> dict
Retourne un dictionnaire comptant les occurrences des mots-clés GO dans la collection.

**collX()** -> dict
Calcule et retourne les occurrences globales de chaque acide aminé dans la collection.

**draw_ABRL(uniprot_id: str)**
Génère et sauvegarde un histogramme représentant le log-ratio des occurrences d'acides aminés pour une protéine spécifique par rapport à leur occurrence moyenne dans la collection.
Sauvegarde le fichier sous le nom <uniprot_id>.png.

## Exemples d'utilisation

### 1. Manipulation d'une protéine individuelle avec la classe `Uniprot`

#### Charger une protéine à partir d'une fiche Uniprot
Voici un exemple d'utilisation des principales méthodes de la classe `Uniprot` :

```python
# Charger une fiche Uniprot à partir d'un fichier
protein = Uniprot(open("data/P05067.txt", 'r').read())

# Affichage des informations principales
print("ID:", protein.id)                   # Affiche l'identifiant Uniprot
print("AC:", protein.ac)                   # Affiche le numéro AC
print("Organisme:", protein.org)           # Affiche l'organisme associé
print("Gene:", protein.gene)               # Affiche le gène correspondant
print("Séquence:", protein.seq)            # Affiche la séquence peptidique complète
print("GO:", protein.go)                   # Affiche les identifiants GO associés

# Exporter au format FASTA
protein.fasta_dump()
print("La séquence a été exportée au format FASTA.")

# Calcul du poids moléculaire
molecular_weight = protein.molecular_weight()
print(f"Le poids moléculaire de la protéine est de : {molecular_weight:.2f} Da")

# Calcul de l'hydrophobicité moyenne
average_hydrophobicity = protein.average_hydrophobicity()
print(f"L'hydrophobicité moyenne de la protéine est de : {average_hydrophobicity:.2f}")

# Fréquence relative des acides aminés
occurrences = protein.occurence_prot()
print("Occurrences des acides aminés :")
for aa, freq in occurrences.items():
    print(f"  {aa}: {freq:.4f}")
```
### 2. Manipulation d'une collection de protéines avec la classe `Collection`

#### Charger, ajouter, afficher et supprimer des protéines

```python
from uniprot_collection import Collection 

# Charger la collection à partir d'un fichier
collection = Collection.load_collection("data/five_proteins.txt")

# Exemple de texte Uniprot pour ajouter une nouvelle protéine
uniprot_text = """ID   NEW_PROTEIN_HUMAN           Reviewed;        500 AA.
AC   P12345; Q67890;
DE   RecName: Full=New Protein; Short=NewP;
GN   Name=NewGene;
OS   Homo sapiens (Human).
SQ   SEQUENCE: 500 AA.
   MSKVEALQKSS..."""  # Exemple de texte Uniprot

# Créer une collection et ajouter des fiches Uniprots
collection = Collection()

# Ajouter l'objet Uniprot à la collection
collection.add(uniprot_text)

# Afficher le contenu de la collection
collection.display()

# Supprimer un Uniprot par son ID
collection.remove("NEW_PROTEIN_HUMAN")

# Afficher à nouveau après suppression
collection.display()

# Afficher le contenu initial de la collection
print("=== Contenu initial de la collection ===")
collection.display()

# Tester la méthode sort_by_length
print("\n=== Test de la méthode sort_by_length ===")
sorted_uniprots = collection.sort_by_length()
print("Proteines triées par longueur (croissante) :")
for uniprot in sorted_uniprots:
    print(f"ID: {uniprot.id}, Longueur: {len(uniprot.seq)} AA")

# Tester la méthode filter_for_hydrophobic avec min_hydro=0.4
print("\n=== Test de filter_for_hydrophobic avec retour en dictionnaire ===")
filtered_dict = collection.filter_for_hydrophobic_dict(0.4)
print(f"Protéines filtrées (dictionnaire) : {len(filtered_dict)} trouvées")
for uniprot_id, uniprot in filtered_dict.items():
    print(f"ID: {uniprot_id}, Hydrophobicité moyenne: {uniprot.average_hydrophobicity()}")

# Créer deux collections
collection_1 = Collection()
collection_2 = Collection()

# Ajouter des objets Uniprot fictifs
uniprot_1 = """ID   PROTEIN1_HUMAN           Reviewed;        300 AA.
AC   P12345;
OS   Homo sapiens (Human).
SQ   SEQUENCE: 300 AA.
   MSKVEALQKSS..."""
uniprot_2 = """ID   PROTEIN2_HUMAN           Reviewed;        400 AA.
AC   P67890;
OS   Homo sapiens (Human).
SQ   SEQUENCE: 400 AA.
   MSKVEALQKSS..."""
uniprot_3 = """ID   PROTEIN3_HUMAN           Reviewed;        500 AA.
AC   Q12345;
OS   Homo sapiens (Human).
SQ   SEQUENCE: 500 AA.
   MSKVEALQKSS..."""

# Ajouter les objets à leurs collections respectives
collection_1.add(uniprot_1)
collection_1.add(uniprot_2)

collection_2.add(uniprot_2)  # Doublon
collection_2.add(uniprot_3)

# Fusionner les collections
merged_collection = collection_1 + collection_2

# Afficher la collection fusionnée
print("=== Collection Fusionnée ===")
merged_collection.display()

# Analyser les termes GO dans la collection
print(collection.go_view())

# Calculer les occurrences globales des acides aminés
print(collection.collX())

# Tracer un histogramme des log-ratios pour une protéine spécifique
log_ratios = collection.draw_ABRL("SPRC_BOVIN")
print(log_ratios)
```