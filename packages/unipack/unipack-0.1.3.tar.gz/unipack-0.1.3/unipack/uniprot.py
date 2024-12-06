# Fonction d'appel a partir d'un path d'un fichier text
def from_file_to_uniprot(path_input:str) :
    with open(path_input) as file:
        content = file.read()
    return Uniprot(content)

class Uniprot :
	def __init__(self,contenu_text):#Argument
		#Initialisation des atributs
		self.id = None
		self.ac_number = None
		self.organisme = None
		self.gene_name = None
		self.sequence = None
		self.go_id = None
		self.contenu_text = contenu_text
		# Appel de la methode de parsage
		self.parse(contenu_text)

	def parse(self,contenu_text):
		# Splitter en ligne pour itérer sur des lignes et non des caractères
		lignes = contenu_text.split("\n") 
		
		# Parsage du fichier 
		fasta=str("")
		liste_go=[]
		for ligne in lignes :
			# Définition de l'attribut id de l'objet de la classe uniprot, on cherche alors la ligne dans le fichier uniprot.txt qui commence par le code ID
			if ligne.startswith("ID"):
				self.id=str(ligne.split()[1])
			# Définition de l'attribut ac_number de l'objet de la classe uniprot, on cherche alors la ligne dans le fichier uniprot.txt qui commence par AC,
			# On rajoute la condition "==None" car on souhaite seulement sélectionné le premier numero d'accession, ainsi une fois que celui-ci sera défini, l'attribut
			# ac_number ne sera alors pas modifier et le code passera à la définition de l'organisme
			elif ligne.startswith("AC") and self.ac_number==None:
				self.ac_number = str(ligne.split()[1][:-1])
			# Définition de l'attribut organisme de l'objet de la classe uniprot, on cherche alors la ligne dans le fichier uniprot.txt qui commence par OS
			elif ligne.startswith("OS"):
				self.organisme=str(f'{ligne.split()[1]} {ligne.split()[2]}')
			# Définition de l'attribut gene_name de l'objet de la classe uniprot, on cherche alors la ligne dans le fichier uniprot.txt qui commence par GN,
			# Ici aussi, la présence de plusieurs ligne commencant par GN nous pousse à sélectionner celui-ci sur le première ligne
			elif ligne.startswith("GN") and self.gene_name==None:
				self.gene_name=str(ligne.split()[1][5:])
			# Définition de l'attribut sequence de l'objet de la classe uniprot, on cherche alors la ligne dans le fichier uniprot.txt qui commence par SQ
			elif ligne.startswith("SQ") or ligne.startswith(" "):
				fasta+=str(ligne)
				fasta2=fasta.split(";")
				self.sequence=str(fasta2[3].replace(" ",""))
			# Définition de l'attribut go_id de l'objet de la classe uniprot, on cherche alors la ligne dans le fichier uniprot.txt qui commence par "DR   GO",
			# dans chauque ligne commencant par ce code, on récupère l'identifiant GO qu'on ajoute dans une liste dédié nommé liste go
			elif ligne.startswith("DR   GO"):
				go=ligne.split(";")[1].strip()
				liste_go.append(go)
				self.go_id=liste_go
			# Les différents slices et split sont utilisés pour sélectionné uniquement les informations d'intérêts dans les lignes
	
	def fasta_dump(self):
		# Définition du nom du fichier
		file_name = F'{str(self.ac_number)}.fasta'
		# Création d'un Fstring avec 
		# en header l'ID, l'organisme, le nom de gène puis la séquence
		contenue = F'>{self.id}\t{self.organisme}\t{self.gene_name}\n{self.sequence}'
		with open(f"{file_name}", 'w') as file :
			file.write(contenue)
		print(f"Le fichier {file_name} contenant la sequence fasta de la protéine a été créer.")
	
	def molecular_weight(self):
		# Cette fonction retourne la masse moléculaire de la protéine à l'aide de sa séquence extraite du fichier .txt et stocker dans la variable self.sequence
		# Grâce au tableau présent sur le GitLab, on peut créer le dictionaire mol_weight_per_AA qui prend en clé le code à une lettre des AA et en valeurs leur masse
		# moléculaire
		mol_weight_per_AA = {
    	"A": 89,   # Alanine
    	"R": 174,  # Arginine
    	"N": 132,  # Asparagine
    	"D": 133,  # Aspartic acid
    	"B": 133,  # Asparagine or aspartic acid
    	"C": 121,  # Cysteine
    	"Q": 146,  # Glutamine
    	"E": 147,  # Glutamic acid
    	"Z": 147,  # Glutamine or glutamic acid
    	"G": 75,   # Glycine
    	"H": 155,  # Histidine
    	"I": 131,  # Isoleucine
    	"L": 131,  # Leucine
    	"K": 146,  # Lysine
    	"M": 149,  # Methionine
    	"F": 165,  # Phenylalanine
    	"P": 115,  # Proline
    	"S": 105,  # Serine
    	"T": 119,  # Threonine
    	"W": 204,  # Tryptophan
    	"Y": 181,  # Tyrosine
    	"V": 117   # Valine
		}
		# On initie la variable protein_weight qui sera la valeur finale de la masse moléculaire de la protéine
		protein_weight=0
		# On crée une boucle qui parcours la séquence et qui par AA, récupère l'information de sa masse moléculaire (la valeur dans le dictionnaire) et l'ajoute dans
		# la variable protein_weight. Celle ci augmentant au fur et à mesure des cycle jusqu'a obtenir sa valeur finale à la fin du parcours. 
		for AA in self.sequence:
			protein_weight+=float(mol_weight_per_AA[AA])
		return protein_weight

	def average_hydrophobicity(self):
		# Cette fonction retourne l'hydrophobicité moyenne de la protéine à l'aide de sa séquence extraite du fichier .txt et stocker dans la variable self.sequence
		# Grâce au tableau présent sur le GitLab, on peut créer le dictionaire hydrophobicity_per_AA qui prend en clé le code à une lettre des AA et en valeurs leur 
		# hydrophoby scale. Pour les acides aminées ayant une valeur inderterminé d'hydrophobicité (n/a), leur valeur ont arbitrairement été fixé à 0.
		hydrophobicity_per_AA = {
    	"A": 0.33,    # Alanine
    	"R": 1.00,    # Arginine
    	"N": 0.43,    # Asparagine
    	"D": 2.41,    # Aspartic acid
    	"B": 0,       # Asparagine or aspartic acid (n/a)
    	"C": 0.22,    # Cysteine
    	"Q": 0.19,    # Glutamine
    	"E": 1.61,    # Glutamic acid
    	"Z": 0,       # Glutamine or glutamic acid (n/a)
    	"G": 1.14,    # Glycine
    	"H": -0.06,   # Histidine (deux valeurs possibles, choix de la première)
    	"I": -0.81,   # Isoleucine
    	"L": -0.69,   # Leucine
    	"K": 1.81,    # Lysine
    	"M": -0.44,   # Methionine
    	"F": -0.58,   # Phenylalanine
    	"P": -0.31,   # Proline
    	"S": 0.33,    # Serine
    	"T": 0.11,    # Threonine
    	"W": -0.24,   # Tryptophan
    	"Y": 0.23,    # Tyrosine
    	"V": -0.53    # Valine
		}
		# On initie deux variable total_hydrophobicity et protein_lenght dont la rapport permettra l'obtention de l'hydrophobicité moyenne de la protéine.
		total_hydrophobicity=0
		protein_lenght=float(len(self.sequence))
		for AA in self.sequence:
			total_hydrophobicity+=float(hydrophobicity_per_AA[AA])
		average_hydrophobicity=total_hydrophobicity/protein_lenght
		return average_hydrophobicity
	
	def print_attributes(self) :
	# Méthode aditionelle pour tester nos méthode et notre parsage
		print(f"ID: {self.id}")
		print(f"AC Number: {self.ac_number}")
		print(f"Organisme: {self.organisme}")
		print(f"Gene Name: {self.gene_name}")
		print(f"Sequence: {self.sequence}")
		print(f"GO ID: {self.go_id}")

