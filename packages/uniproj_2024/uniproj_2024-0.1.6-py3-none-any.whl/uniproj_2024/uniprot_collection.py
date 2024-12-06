from .uniprot import Uniprot
import math
from matplotlib import figure


class Collection:
    """
    Classe pour gérer une collection d'objets Uniprot.
    Permet de charger, ajouter, supprimer, afficher, trier, filtrer et analyser les objets Uniprot.
    """
    def __init__(self):
        self.uniprots = []
    """
    Initialise une collection vide d'objets Uniprot.
    """

    def load_collection(fichier_in):
        """
        Charge une collection d'objets Uniprot à partir d'un fichier texte.
        
        Arguments:
            fichier_in (str): Chemin du fichier contenant les données des objets Uniprot.
        
        Raises:
            ValueError: Si `fichier_in` n'est pas une chaîne valide.
            FileNotFoundError: Si le fichier n'est pas trouvé.
            RuntimeError: Pour toute autre erreur lors du chargement.
        Returns:
            Collection: Une collection contenant les objets Uniprot extraits du fichier.
        """
        if not isinstance(fichier_in, str) or not fichier_in.strip():
            raise ValueError("Le chemin du fichier doit être une chaîne non vide.")
        try :
            with open(fichier_in, 'r') as file:
                collection = Collection()  
                entry = []
                for line in file:
                    if line.strip() == "//":
                        if entry:
                            collection.add("".join(entry))
                            entry = []
                    else:
                        entry.append(line)
                if entry:
                    collection.add("".join(entry))
        except FileNotFoundError:
            raise FileNotFoundError(f"Le fichier '{fichier_in}' est introuvable.")
        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement du fichier : {e}")
        return collection

    def add(self, contenu_uniprot: str):
        """
        Ajoute un objet Uniprot à la collection après vérification des doublons.
        
        Arguments:
            contenu_uniprot (str): Contenu d'un objet Uniprot au format texte.
        
        Raises :
            ValueError: Si le contenu est vide ou invalide.
            ValueError: Si un objet avec le même ID existe déjà dans la collection.
        """
        if not contenu_uniprot or not isinstance(contenu_uniprot, str):
            raise ValueError("Le contenu d'un objet Uniprot doit être une chaîne non vide.")
        try:
            uniprot_objet = Uniprot(contenu_uniprot)
        except Exception as e:
            raise ValueError(f"Erreur lors de la création de l'objet Uniprot : {e}")
        if not uniprot_objet.id:
            raise ValueError("L'objet Uniprot ajouté doit avoir un ID valide.")
        for u in self.uniprots:
            if u.id == uniprot_objet.id:
                raise ValueError(f"La fiche Uniprot avec ID {uniprot_objet.id} est déjà présente dans la collection.")

        
        self.uniprots.append(uniprot_objet)

    def remove(self, uniprot_id: str):
        """
        Supprime un objet Uniprot de la collection selon son ID.
        
        Arguments:
            uniprot_id (str): Identifiant unique de l'objet Uniprot à supprimer.
        
        Raises:
            ValueError: Si l'ID est vide ou invalide.
            ValueError: Si aucun objet Uniprot avec cet ID n'est trouvé.
        """
        if not uniprot_id or not isinstance(uniprot_id, str):
            raise ValueError("L'ID à supprimer doit être une chaîne non vide.")
        
        uniprot_to_remove = None
        for uniprot in self.uniprots:
            if uniprot.id == uniprot_id:
                uniprot_to_remove = uniprot
                break
        
        if uniprot_to_remove is None:
            raise ValueError(f"Aucun Uniprot trouvé avec l'ID {uniprot_id}.")
        
        self.uniprots.remove(uniprot_to_remove)

    def display(self):
        """
        Affiche les informations de tous les objets Uniprot dans la collection.
        """
        if not self.uniprots:
            print("La collection est vide.")
            return
        
        for i, uniprot in enumerate(self.uniprots, start=1):
            print(f"Protéine {i}:")
            print(f"  ID: {uniprot.id}")
            print(f"  AC: {uniprot.ac}")
            print(f"  Organisme: {uniprot.org}")
            print(f"  Gène: {uniprot.gene}")
            print(f"  Séquence (début): {uniprot.seq[:30]}...")
            print()

    def sort_by_length(self, reverse=False):
        """
        Trie les objets Uniprot par longueur de leur séquence.
        
        Arguments:
            reverse (bool): Si True, trie par ordre décroissant. Sinon, par ordre croissant.
        
        Returns:
            list: Liste triée d'objets Uniprot.
        """
        return sorted(self.uniprots, key=lambda u: len(u.seq), reverse=reverse)

    def filter_for_hydrophobic_dict(self, min_hydro:int):   
        """
        Filtre les objets Uniprot et retourne un dictionnaire des résultats.
        
        Arguments:
            min_hydro (int): Valeur minimale d'hydrophobicité.
        
        Returns:
            dict: Dictionnaire des objets Uniprot répondant au critère, indexés par leur ID.
        """
        if not isinstance(min_hydro, (int, float)):
            raise ValueError("La valeur minimale d'hydrophobicité doit être un nombre.")
        
        filtered_dict = {}
        for uniprot in self.uniprots:
            if uniprot.average_hydrophobicity() > min_hydro:
                filtered_dict[uniprot.id] = uniprot

        return filtered_dict
    
    def __add__(self, other):
        """
        Fusionne deux collections d'objets Uniprot sans doublons d'ID.
        
        Arguments:
            other (Collection): Une autre collection d'objets Uniprot.
        
        Returns:
            Collection: Une nouvelle collection fusionnée.
        
        Raises:
            TypeError: Si l'objet `other` n'est pas une instance de Collection.
            ValueError: Si l'une des collections est vide ou invalide.
        """
        if not isinstance(other, Collection):
            raise TypeError("L'opération d'addition est uniquement supportée entre deux objets Collection.")
        if not self.uniprots and not other.uniprots:
            raise ValueError("Les deux collections sont vides. Impossible de les fusionner.")
        
        new_collection = Collection()

        for uniprot in self.uniprots:
            if uniprot.id not in [u.id for u in new_collection.uniprots]:
                new_collection.uniprots.append(uniprot)

        for uniprot in other.uniprots:
            if uniprot.id not in [u.id for u in new_collection.uniprots]:
                new_collection.uniprots.append(uniprot)

        return new_collection
    
    def go_view(self):
        """
        Compte les occurrences des termes GO dans la collection.
        
        Returns:
            dict: Dictionnaire des termes GO et leur nombre d'occurrences.
        Raises:
            ValueError: Si la collection est vide.
        """
        if not self.uniprots:
            raise ValueError("La collection est vide. Aucune donnée GO à analyser.")
        
        go_dict = {}
        for uniprot in self.uniprots:
            if not uniprot.go:
                continue
            for element in uniprot.go:
                if element not in go_dict.keys():
                    go_dict[element] = 1
                else :
                    go_dict[element] += 1
        return go_dict


    def collX(self):
        """
        Calcule les occurrences globales des acides aminés dans la collection.
        
        Returns:
            dict: Dictionnaire des acides aminés et leur nombre total d'occurrences.
        Raises:
            ValueError: Si la collection est vide.
        """
        if not self.uniprots:
            raise ValueError("La collection est vide. Impossible de calculer les occurrences d'acides aminés.")
        
        dict_collX = {}
        for uniprot in self.uniprots:
            dict_uniprot = Uniprot.occurence_prot(uniprot)
            for aa, count in dict_uniprot.items():
                if aa in dict_collX:
                    dict_collX[aa] += count
                else:
                    dict_collX[aa] = count

        return dict_collX


    def draw_ABRL (self, uniprot_id:str):
        """
        Calcule les log-ratios des occurrences d'acides aminés pour une protéine spécifique, 
        et trace l'histogramme de l'abondance relative des acides aminés dans un fichier <uniprot.id>.png
        
        Args:
            uniprot_id (str): Identifiant de l'objet Uniprot étudié.
        
        Returns:
            dict: Dictionnaire des log-ratios des acides aminés pour la protéine spécifiée.
        
        Raises:
            ValueError: Si l'ID de la protéine est invalide ou si aucun objet Uniprot avec cet ID n'est trouvé.
            ValueError: Si la collection est vide.
        """                  
        if not uniprot_id or not isinstance(uniprot_id, str):
            raise ValueError("L'ID de la protéine doit être une chaîne non vide.")
        
        if not self.uniprots:
            raise ValueError("La collection est vide. Impossible de calculer les log-ratios.")

        uniprot = next((u for u in self.uniprots if u.id == uniprot_id), None)
        if not uniprot:
            raise ValueError(f"Aucune protéine trouvée avec l'ID {uniprot_id}.")
        
        dict_uniprot = uniprot.occurence_prot()  
                    
        coll_occurrences = self.collX() 
                
        amino_acids = "ACDEFGHIKLMNPQRSTVWY"  
        log_ratios = {}
        
        for aa in amino_acids:
            prot_X = dict_uniprot.get(aa, 0)
            coll_X = coll_occurrences.get(aa, 1e-6)
                    
            if prot_X > 0:
                log_ratios[aa] = math.log(prot_X / (coll_X/len(self.uniprots)) )
            else:
                log_ratios[aa] = -math.inf

        fig = figure.Figure(figsize=(10, 6))
        ax = fig.subplots(1, 1)
        aa_labels = list(log_ratios.keys())
        log_values = list(log_ratios.values())

        ax.bar(aa_labels, log_values, color='blue', alpha=0.7)
        ax.set_title(f"Log-Ratios des acides aminés pour {uniprot_id}")
        ax.set_xlabel("Acides aminés")
        ax.set_ylabel("Log-Ratio")
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        filename = f"{uniprot_id}.png"
        fig.savefig(filename)

        return log_ratios



