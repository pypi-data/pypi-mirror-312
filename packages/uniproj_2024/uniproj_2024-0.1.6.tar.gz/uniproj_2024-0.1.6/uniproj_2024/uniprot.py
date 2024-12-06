class Uniprot: 
    
    """
    Représente une entrée Uniprot. La classe prend le contenu textuel d'une fiche Uniprot,
    analyse le contenu et initialise des attributs représentant l'identifiant, le numéro AC,
    l'organisme, le nom du gène, la séquence peptidique et les identifiants GO de la protéine.
    
    Attributs:
    id (str) : Identifiant Uniprot de la protéine.
    ac (str) : Numéro AC de la protéine.
    org (str) : Organisme associé à la protéine.
    gene (str) : Nom du gène de la protéine.
    seq (str) : Séquence peptidique de la protéine.
    go (list) : Liste d'identifiants GO associés à la protéine.

    """

    def __init__(self, contenu_fichier): 

        """
        Initialise l'objet Uniprot en analysant le contenu textuel d'une fiche Uniprot.

        Arguments:
        contenu_fichier (str) : Contenu textuel d'une fiche Uniprot.

        Raises :
        ValueError : Si le fichier est vide ou mal formaté.

        """

        self.id = "" 
        self.ac = "" 
        self.org = ""
        self.gene = "" 
        self.seq = "" 
        self.go = []

        if not contenu_fichier:
            raise ValueError("Le fichier d'entrée est vide ou invalide.")

        lines = contenu_fichier.splitlines()
        ac_found = False
    
        for line in lines:
            line.strip()
            
            try:
                if line.startswith("ID"):
                    self.id = line.split()[1]
                
                elif line.startswith("AC"):
                    if not ac_found:
                        ac_numbers = line.split()[1].split(";")
                        self.ac = ac_numbers[0]
                        ac_found = True
                
                elif line.startswith("OS"):
                    OS_line = line.split(maxsplit=1)
                    self.org = OS_line[1].strip(".\n")
                
                elif line.startswith("GN"):
                    gene_info = line.split()
                    for element in gene_info:
                        if element.startswith("Name="):
                            self.gene = element[5:].rstrip(";")
                elif line.startswith("  "):
                    self.seq += line.replace(" ","")

                elif line.startswith("DR"):
                    if 'GO:' in line :
                        dr_line = line.split('GO:')[1]
                        self.go.append(dr_line) 
    
            except IndexError as e:
                raise ValueError(f"Erreur dans la ligne : {line}. Détails : {str(e)}")
            except ValueError as e:
                    print(f"Warning : {e}")

    def fasta_dump(self):

        """
        Exporte la séquence peptidique dans un fichier au format FASTA.

        Le fichier est nommé en utilisant le numéro AC de la protéine et contient l'identifiant,
        l'organisme et le nom du gène dans l'en-tête. La séquence est divisée en lignes de 60 caractères.

        Raises :
        IOError : Si une erreur survient lors de l'écriture du fichier.
        ValueError : Si la séquence est vide.

        """

        fichier_fasta = f"{self.ac}.fasta"
        fasta_header = f">{self.id.strip()} {self.org.strip()} {self.gene.strip()}\n"
        sequence = "\n".join([self.seq[i:i+60] for i in range(0, len(self.seq), 60)])

        try:
            with open(fichier_fasta, 'w') as fasta_file:
                fasta_file.write(fasta_header)
                fasta_file.write(sequence)
        except IOError as e:
            raise IOError(f"Erreur lors de la création du fichier FASTA : {str(e)}")

    # Table des acides aminés
    amino_acids = {
        "Alanine": {"3_letter": "Ala", "1_letter": "A", "mol_weight": "89Da", "class": "A", "hydrophobicity": 0.33},
        "Arginine": {"3_letter": "Arg", "1_letter": "R", "mol_weight": "174Da", "class": "+", "hydrophobicity": 1.00},
        "Asparagine": {"3_letter": "Asn", "1_letter": "N", "mol_weight": "132Da", "class": "P", "hydrophobicity": 0.43},
        "Aspartic acid": {"3_letter": "Asp", "1_letter": "D", "mol_weight": "133Da", "class": "-", "hydrophobicity": 2.41},
        "Asparagine or aspartic acid": {"3_letter": "Asx", "1_letter": "B", "mol_weight": "133Da", "class": "n/a", "hydrophobicity": "n/a"},
        "Cysteine": {"3_letter": "Cys", "1_letter": "C", "mol_weight": "121Da", "class": "A or P", "hydrophobicity": 0.22},
        "Glutamine": {"3_letter": "Gln", "1_letter": "Q", "mol_weight": "146Da", "class": "P", "hydrophobicity": 0.19},
        "Glutamic acid": {"3_letter": "Glu", "1_letter": "E", "mol_weight": "147Da", "class": "-", "hydrophobicity": 1.61},
        "Glutamine or glutamic acid": {"3_letter": "Glx", "1_letter": "Z", "mol_weight": "147Da", "class": "n/a", "hydrophobicity": "n/a"},
        "Glycine": {"3_letter": "Gly", "1_letter": "G", "mol_weight": "75Da", "class": "P", "hydrophobicity": 1.14},
        "Histidine": {"3_letter": "His", "1_letter": "H", "mol_weight": "155Da", "class": "P or +", "hydrophobicity": -0.06},
        "Isoleucine": {"3_letter": "Ile", "1_letter": "I", "mol_weight": "131Da", "class": "A", "hydrophobicity": -0.81},
        "Leucine": {"3_letter": "Leu", "1_letter": "L", "mol_weight": "131Da", "class": "A", "hydrophobicity": -0.69},
        "Lysine": {"3_letter": "Lys", "1_letter": "K", "mol_weight": "146Da", "class": "+", "hydrophobicity": 1.81},
        "Methionine": {"3_letter": "Met", "1_letter": "M", "mol_weight": "149Da", "class": "A", "hydrophobicity": -0.44},
        "Phenylalanine": {"3_letter": "Phe", "1_letter": "F", "mol_weight": "165Da", "class": "A", "hydrophobicity": -0.58},
        "Proline": {"3_letter": "Pro", "1_letter": "P", "mol_weight": "115Da", "class": "A", "hydrophobicity": -0.31},
        "Serine": {"3_letter": "Ser", "1_letter": "S", "mol_weight": "105Da", "class": "P", "hydrophobicity": 0.33},
        "Threonine": {"3_letter": "Thr", "1_letter": "T", "mol_weight": "119Da", "class": "P", "hydrophobicity": 0.11},
        "Tryptophan": {"3_letter": "Trp", "1_letter": "W", "mol_weight": "204Da", "class": "A", "hydrophobicity": -0.24},
        "Tyrosine": {"3_letter": "Tyr", "1_letter": "Y", "mol_weight": "181Da", "class": "P", "hydrophobicity": 0.23},
        "Valine": {"3_letter": "Val", "1_letter": "V", "mol_weight": "117Da", "class": "A", "hydrophobicity": -0.53}
    }
    
    def molecular_weight(self):

        """
        Calcule le poids moléculaire total de la protéine à partir de sa séquence.

        Chaque acide aminé de la séquence est utilisé pour calculer son poids moléculaire en 
        fonction de la table des acides aminés. Le poids total est retourné en Da (Daltons).

        Returns:
        int : Poids moléculaire total de la protéine en Dalton.

        Raises :
        ValueError : Si la séquence est vide.
        
        """

        weight = 0
        weight_dict = {aa_info["1_letter"]: int(aa_info["mol_weight"].replace("Da", "")) for aa_info in self.amino_acids.values()}

        for amino_acid in self.seq:
            weight += weight_dict.get(amino_acid, 0)
        return weight
    
    def average_hydrophobicity(self):

        """
        Calcule l'hydrophobicité moyenne de la séquence de la protéine.

        L'hydrophobicité de chaque acide aminé est utilisée pour calculer une valeur moyenne 
        pour la séquence entière.

        Returns:
        float : Hydrophobicité moyenne de la protéine.

        Raises :
        ValueError : Si la séquence est vide.
        """

        hydrophobicity = 0
        hydrophobicty_dict = {aa_info["1_letter"]: (aa_info["hydrophobicity"]) for aa_info in self.amino_acids.values()}

        for amino_acid in self.seq:
            hydrophobicity += hydrophobicty_dict.get(amino_acid, 0)
        return hydrophobicity / len(self.seq) if len(self.seq) > 0 else 0
    
    def occurence_prot(self):

        """
        Calcule la fréquence relative des acides aminés dans la séquence de la protéine.

        La fréquence relative de chaque acide aminé est calculée en divisant le nombre
        d'occurrences de cet acide aminé par la longueur totale de la séquence. 

        Returns:
        dict : Dictionnaire des fréquences relatives des acides aminés dans la séquence de la protéine.

        Raises :
        ValueError : Si la séquence est vide.
        
        """
        
        dict_occurence_prot = {}

        for aa in self.seq:
            if aa not in dict_occurence_prot:
                dict_occurence_prot[aa] = 1
            else : 
                dict_occurence_prot[aa] += 1
        total_length = len(self.seq)
        for aa in dict_occurence_prot:
            dict_occurence_prot[aa] /= total_length

        return dict_occurence_prot