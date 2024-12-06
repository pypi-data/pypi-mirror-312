# Import du package `unipack` et guide utilisation basique

```python
import unipack

# Pour travailler avec un fichier contenant une seule entrée UniProt
uniprot_objet = unipack.from_file_to_uniprot('chemin_fichier.txt')

# Pour travailler avec un fichier contenant plusieurs entrées UniProt
collection_objet = unipack.from_file_to_collection('chemin_fichier.txt')
```

---

## Description

Le package `unipack` fournit des outils pour manipuler des données UniProt au format texte. Il inclut deux classes principales :  
- **`Uniprot`** : Représente une entrée individuelle.
- **`Collection`** : Représente une collection d'entrées UniProt.

---

## Fonctionnalités principales

### Création d'objets

#### À partir d'un fichier contenant une seule entrée UniProt
Utilisez la fonction `from_file_to_uniprot` pour créer un objet `Uniprot` :

```python
uniprot_objet = unipack.from_file_to_uniprot("chemin_fichier.txt")
```

#### À partir d'un fichier contenant plusieurs entrées UniProt
Utilisez la fonction `from_file_to_collection` pour créer un objet `Collection` :

```python
collection_objet = unipack.from_file_to_collection("chemin_fichier_collection.txt")
```

---

### Détails des classes, méthodes, et exemples d'utilisation

#### **Classe `Uniprot`**
Représente une entrée UniProt individuelle.

| Méthode                  | Entrée                         | Description                                                                                  | Exemple d'utilisation et sortie                                                                                                                                              |
|--------------------------|---------------------------------|----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `fasta_dump()`           | Aucun                         | Génère un fichier FASTA contenant l'ID, l'organisme, le nom du gène et la séquence.          | **Entrée :** `uniprot_obj.fasta_dump()` <br> **Sortie :** Fichier `AC12345.fasta` créé avec les données de l'objet.                                                          |
| `molecular_weight()`     | Aucun                         | Retourne la masse moléculaire de la protéine en fonction de sa séquence.                     | **Entrée :** `uniprot_obj.molecular_weight()` <br> **Sortie :** `50289.0` (masse moléculaire calculée).                                                                     |
| `average_hydrophobicity()` | Aucun                        | Retourne l'hydrophobicité moyenne de la protéine.                                            | **Entrée :** `uniprot_obj.average_hydrophobicity()` <br> **Sortie :** `0.23` (hydrophobicité moyenne).                                                                       |
| `print_attributes()`     | Aucun                         | Affiche les attributs (ID, séquence, etc.) de l'objet.                                       | **Entrée :** `uniprot_obj.print_attributes()` <br> **Sortie :** Affiche dans la console :<br>`ID: P12345`<br>`AC Number: AC12345`<br>`Organisme: Homo sapiens`... |

---

#### **Classe `Collection`**
Représente une collection d'objets UniProt.

| Méthode                     | Entrée                                  | Description                                                                                     | Exemple d'utilisation et sortie                                                                                                                                                  |
|-----------------------------|------------------------------------------|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `add(arg)`                  | `str` (chemin vers un fichier) ou `Uniprot` | Ajoute un nouvel objet `Uniprot` à la collection.                                              | **Entrée :** `collection.add(uniprot_obj)` <br> **Sortie :** L'objet `uniprot_obj` est ajouté à la collection.                                                                    |
| `delet(uniprot_id)`         | `str` (ID d'un objet Uniprot)            | Supprime un objet `Uniprot` de la collection à partir de son ID.                               | **Entrée :** `collection.delet("P12345")` <br> **Sortie :** L'objet avec l'ID `"P12345"` est supprimé de la collection.                                                           |
| `sort_by_lenght()`          | Aucun                                   | Trie les objets `Uniprot` par longueur de séquence.                                            | **Entrée :** `collection.sort_by_lenght()` <br> **Sortie :** La collection est triée, du plus court au plus long.                                                                |
| `filter_for_hydrophobic(min_hydro)` | `int` (seuil d'hydrophobicité)         | Retourne les objets dont l'hydrophobicité moyenne dépasse un seuil donné.                      | **Entrée :** `collection.filter_for_hydrophobic(0.5)` <br> **Sortie :** Une liste des objets respectant le critère d'hydrophobicité moyenne.                                      |
| `__add__(collection_2)`     | `Collection`                            | Combine deux collections, en éliminant les doublons, pour en créer une nouvelle.               | **Entrée :** `new_collection = collection1 + collection2` <br> **Sortie :** Une nouvelle collection contenant les objets uniques des deux collections.                            |
| `go_view()`                 | Aucun                                   | Retourne une liste unique des termes GO (Gene Ontology) présents dans la collection.            | **Entrée :** `collection.go_view()` <br> **Sortie :** `{ "GO:0008150": 3, "GO:0003674": 5 }` (termes GO avec leur fréquence).                                                    |
| `draw_ABRL(uniprot_id)`     | `str` (ID d'un objet Uniprot)            | Génère un histogramme de l'abondance relative des acides aminés pour un objet donné.           | **Entrée :** `collection.draw_ABRL("P12345")` <br> **Sortie :** Histogramme enregistré sous le nom `"P12345.png"`.                                                              |
| `print_attributes()`        | Aucun                                   | Affiche les attributs de chaque objet `Uniprot` dans la collection.                            | **Entrée :** `collection.print_attributes()` <br> **Sortie :** Affiche dans la console les attributs de chaque objet `Uniprot` de la collection.                                 |
