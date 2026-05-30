# data_manager.py
# This file handles saving and loading data to and from a JSON file.
# It acts as the data persistence layer for the FarmCare project.

import json
import os
from models import Animal

# Constant: name of the save file
FICHIER_DONNEES: str = "farmcare_data.json"


class DataManager:
    """Manages data persistence for the FarmCare project.

    Allows saving and loading the list of livestock cycles
    to and from a local JSON file.
    """

    def __init__(self, chemin_fichier: str = FICHIER_DONNEES):
        """Initialize the data manager.

        Args:
            chemin_fichier (str): Path to the JSON save file.
        """
        self.chemin_fichier = chemin_fichier

    def sauvegarder(self, animaux: list) -> bool:
        """Save the list of animal cycles to the JSON file.

        Args:
            animaux (list): List of Animal objects to save.

        Returns:
            bool: True if saving was successful, False otherwise.
        """
        try:
            # Convert each Animal object to a dictionary
            donnees = [animal.to_dict() for animal in animaux]

            # Write to the JSON file with indentation for readability
            with open(self.chemin_fichier, "w", encoding="utf-8") as fichier:
                json.dump(donnees, fichier, indent=4, ensure_ascii=False)

            return True

        except Exception as erreur:
            print(f"Error while saving: {erreur}")
            return False

    def charger(self) -> list:
        """Load the list of animal cycles from the JSON file.

        Returns:
            list: List of Animal objects loaded. Empty list if the file does not exist.
        """
        animaux = []

        # Check if the file exists before opening it
        if not os.path.exists(self.chemin_fichier):
            return animaux

        try:
            with open(self.chemin_fichier, "r", encoding="utf-8") as fichier:
                donnees = json.load(fichier)

            # Rebuild each Animal object from its dictionary
            for data in donnees:
                animal = Animal.from_dict(data)
                animaux.append(animal)

        except Exception as erreur:
            print(f"Error while loading: {erreur}")

        return animaux

    def fichier_existe(self) -> bool:
        """Check whether the data file exists.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return os.path.exists(self.chemin_fichier)
