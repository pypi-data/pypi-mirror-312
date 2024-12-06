from . import uniprot
from matplotlib import figure
import math

# Fonction d'appel a partir d'un path d'un fichier text
def from_file_to_collection(path_input:str) :
    with open(path_input) as file:
        content = file.read()
    return Collection(content)

class Collection : 
    
    def __init__(self,contenu_uniprot_proteins=None):
        # Sépare notre str brut en autant de fiche uniprot et appel uniprot.build 
        self.uniprot = []
        if not contenu_uniprot_proteins is None:
            contenu_uniprot_proteins = contenu_uniprot_proteins.strip()
            self.liste_txt=contenu_uniprot_proteins.split("//\n")
            self.uniprot_build()

    def uniprot_build(self):
        # A partir d'une liste de str créer notre liste d'objet uniprot
        for elem in self.liste_txt :
            objet_uniprot = uniprot.Uniprot(elem)
            self.uniprot.append(objet_uniprot)

    def __iter__(self):
        # Retourne un itérateur sur la liste des objets
        return iter(self.uniprot)

    def add(self, arg:str|uniprot.Uniprot):
        # Utilisé seul pour ajouter un objet uniprot à notre collection
        # Utilisé par la méthode __add__ pour ajouter sequenciellement les objet dans notre nouvelle collection
        if type(arg) == str : 
            object = uniprot.from_file_to_uniprot(arg)
        else :
            object = arg
        if object in self.uniprot : 
            return ValueError
        else :
            self.uniprot.append(object)

    def delet(self,uniprot_id):
        # Retire l'objet uniport donné en argument selon son id
        # Création d'une liste facilement iterable pour les id des objets présents dans notre collection
        liste_id=[]
        for uniprot_object in self.uniprot:
            liste_id.append(uniprot_object.id)
        for uniprot_object in self.uniprot:
            if uniprot_id not in liste_id:
                return ValueError
            else : 
                if uniprot_object.id == uniprot_id:
                    self.uniprot.remove(uniprot_object)
    
    def sort_by_lenght(self):
        # Trier les objet selon la longeur de leur séquence
        objet_taille={}
        for index,objet in enumerate(self.uniprot):
            objet_taille[objet]=len(self.uniprot[index].sequence)
        print(objet_taille)
        self.uniprot = sorted(self.uniprot, key=lambda obj: objet_taille[obj])# key lambda
        return self.uniprot
    
    def filter_for_hydrophobic(self,min_hydro:int):
        # Return les objet uniprot possédant une hydrophibicité global superieur au seil donné en argument
        for uniprot_objet in self.uniprot[:]: # Pour parcourir une copie pas la liste originelle
            if float(uniprot.Uniprot.average_hydrophobicity(uniprot_objet)) < min_hydro:
                self.uniprot.remove(uniprot_objet)
        return self.uniprot
    
    def __add__(self,collection_2):
        #A partir de deux collection créer une nouvelle collection avec tout les objet uniprot unique
        print(self.uniprot)
        print(collection_2.uniprot)
        liste_id = [] # Liste permettant la verifiaction des objets uniques
        new_collection = Collection()
        # Ajout des objet de la collection initial avec la méthode add dans la nouvelle collection vide
        for objet_uniprot in self.uniprot : 
            if objet_uniprot.id not in liste_id :
                liste_id.append(objet_uniprot.id)
                new_collection.add(objet_uniprot)
            else : pass
        # Ajout des objet de la collection 2 avec la méthode add dans la nouvelle collection en evitant les doublons
        for objet_uniprot in collection_2.uniprot : 
            if objet_uniprot.id not in liste_id :
                liste_id.append(objet_uniprot.id)
                new_collection.add(objet_uniprot)
        print(f'La Collection {new_collection} a été créer et contient les objet : \n {new_collection.uniprot}')
        
    def go_view(self):
        # Retourne la liste unique des GO_term au sein de la collection
        go_terms={}
        for uniprot_object in self.uniprot:
            for go in uniprot_object.go_id:
                if go not in go_terms: # Init
                    go_terms[go] = 1
                else: # Incrémentation
                    go_terms[go] += 1 
        return go_terms
    
    def draw_ABRL(self,uniprot_id:str):
        # Créer une représentation graphique de l'abondance relative des AA d'un ojet uniprot au sein de sa collection
        abondance_AA_proteine= {}
        abondance_moyenne_AA = {}
        for uniprot_object in self.uniprot : 
            # Recuperation de l'abondance dans tout les objet
            for AA in uniprot_object.sequence:
                if AA not in abondance_moyenne_AA:
                    abondance_moyenne_AA[AA] = 1
                else:
                    abondance_moyenne_AA[AA] += 1
            # Recuperation de l'abondance dans l'objet en argument
            if uniprot_object.id == uniprot_id:
                for AA in uniprot_object.sequence:
                    if AA not in abondance_AA_proteine:
                        abondance_AA_proteine[AA] = 1
                    else:
                        abondance_AA_proteine[AA] += 1
        abondance_relative={}
        for clé in abondance_AA_proteine:
            abondance_relative[clé]=(abondance_AA_proteine[clé],abondance_moyenne_AA[clé])
        liste_AA=[]
        liste_abondance_relative=[]
        # Calcul de l'abondance relative
        for AA in abondance_relative:
            liste_AA.append(AA)
            liste_abondance_relative.append(math.log(abondance_relative[AA][0]/(abondance_relative[AA][1]/len(self.uniprot))))
        # Création du graphique
        uniprot_id_plot=figure.Figure()
        ax = uniprot_id_plot.subplots(1, 1)
        ax.bar(liste_AA,liste_abondance_relative)
        ax.set_title(f'Histograme de l\'abondance relative des acides aminées de la protéine {uniprot_id} au sein de sa collection',y=-0.2)
        ax.set_ylabel('Abondance relative dans la collection')
        ax.set_xlabel('Acides aminées')
        uniprot_id_plot.savefig(f"{uniprot_id}.png",bbox_inches="tight")
    
    def print_attributes(self):
        # Méthode aditionelle pour tester nos méthode et notre parsage
        for objet_uniprot in self.uniprot :
            print(f"ID: {objet_uniprot.id}")
            print(f"AC Number: {objet_uniprot.ac_number}")
            print(f"Organisme: {objet_uniprot.organisme}")
            print(f"Gene Name: {objet_uniprot.gene_name}")
            print(f"Sequence: {objet_uniprot.sequence}")
            print(f"GO ID: {objet_uniprot.go_id}")
