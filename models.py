# models.py
# This file contains all the classes for the FarmCare project.
# It follows OOP principles: Encapsulation, Abstraction, Inheritance, Polymorphism.

import json
from datetime import date


# ─── Parent Class ─────────────────────────────────────────────────────────────

class Enregistrement:
    """Parent class representing a general record in the system.

    All elements in the system (animals, vaccines, treatments)
    inherit from this base class.
    """

    def __init__(self, nom: str, date_creation: str):
        """Initialize a record with a name and a date.

        Args:
            nom (str): The name of the record.
            date_creation (str): The creation date (format YYYY-MM-DD).
        """
        self.__nom = nom                    # private attribute (encapsulation)
        self.__date_creation = date_creation

    def get_nom(self) -> str:
        """Return the name of the record (getter)."""
        return self.__nom

    def get_date_creation(self) -> str:
        """Return the creation date (getter)."""
        return self.__date_creation

    def set_nom(self, nouveau_nom: str):
        """Update the name of the record (setter)."""
        self.__nom = nouveau_nom

    def afficher_info(self) -> str:
        """Display basic information. Overridden in child classes (polymorphism)."""
        return f"Name: {self.__nom} | Date: {self.__date_creation}"

    def to_dict(self) -> dict:
        """Convert the object to a dictionary for JSON saving."""
        return {
            "nom": self.__nom,
            "date_creation": self.__date_creation
        }


# ─── Vaccin class (inherits from Enregistrement) ─────────────────────────────

class Vaccin(Enregistrement):
    """Represents a vaccine administered to an animal.

    Inherits from Enregistrement and adds the notion of next dose date.
    """

    def __init__(self, nom: str, date_vaccin: str, prochaine_dose: str):
        """Initialize a vaccine record.

        Args:
            nom (str): Vaccine name.
            date_vaccin (str): Date of administration.
            prochaine_dose (str): Scheduled date for the next dose.
        """
        super().__init__(nom, date_vaccin)   # call parent constructor
        self.prochaine_dose = prochaine_dose

    def afficher_info(self) -> str:
        """Override afficher_info for vaccines (polymorphism)."""
        return f"💉 Vaccine: {self.get_nom()} | Date: {self.get_date_creation()} | Next dose: {self.prochaine_dose}"

    def to_dict(self) -> dict:
        """Convert the vaccine to a dictionary."""
        data = super().to_dict()
        data["prochaine_dose"] = self.prochaine_dose
        data["type"] = "vaccin"
        return data


# ─── Traitement class (inherits from Enregistrement) ─────────────────────────

class Traitement(Enregistrement):
    """Represents a medical treatment (tablet, antibiotic, vitamin, etc).

    Inherits from Enregistrement and adds type and dosage information.
    """

    # Tuple of valid treatment types (used for validation)
    TYPES_VALIDES: tuple = ("Comprimé", "Vitamine", "Antibiotique", "Autre")

    def __init__(self, nom: str, date_traitement: str, type_traitement: str, dose: str):
        """Initialize a treatment record.

        Args:
            nom (str): Name of the medicine or treatment.
            date_traitement (str): Date of the treatment.
            type_traitement (str): Type of treatment (Tablet, Vitamin, etc).
            dose (str): Quantity or dose administered.
        """
        super().__init__(nom, date_traitement)
        self.type_traitement = type_traitement
        self.dose = dose

    def afficher_info(self) -> str:
        """Override afficher_info for treatments (polymorphism)."""
        return f"💊 {self.type_traitement}: {self.get_nom()} | Dose: {self.dose} | Date: {self.get_date_creation()}"

    def to_dict(self) -> dict:
        """Convert the treatment to a dictionary."""
        data = super().to_dict()
        data["type_traitement"] = self.type_traitement
        data["dose"] = self.dose
        data["type"] = "traitement"
        return data


# ─── Animal class (main class) ────────────────────────────────────────────────

class Animal:
    """Represents a livestock cycle for a given animal type.

    Manages statistics, births, deaths, vaccines, and treatments.
    """

    def __init__(self, type_animal: str, nombre_initial: int, duree_cycle: int, date_debut: str):
        """Initialize a livestock cycle.

        Args:
            type_animal (str): The type of animal (e.g. Chicken, Sheep...).
            nombre_initial (int): Number of animals at the start.
            duree_cycle (int): Duration of the cycle in days.
            date_debut (str): Start date of the cycle.
        """
        self.__type_animal = type_animal        # encapsulation
        self.__nombre_initial = nombre_initial
        self.__duree_cycle = duree_cycle
        self.__date_debut = date_debut
        self.__deces: int = 0
        self.__naissances: int = 0
        self.__vaccins: list = []        # list of vaccines
        self.__traitements: list = []    # list of treatments

    # ── Getters ───────────────────────────────────────────────────────────────

    def get_type_animal(self) -> str:
        """Return the animal type."""
        return self.__type_animal

    def get_nombre_initial(self) -> int:
        """Return the initial number of animals."""
        return self.__nombre_initial

    def get_duree_cycle(self) -> int:
        """Return the cycle duration in days."""
        return self.__duree_cycle

    def get_date_debut(self) -> str:
        """Return the cycle start date."""
        return self.__date_debut

    def get_deces(self) -> int:
        """Return the total number of deaths."""
        return self.__deces

    def get_naissances(self) -> int:
        """Return the total number of births."""
        return self.__naissances

    def get_vaccins(self) -> list:
        """Return the list of vaccines."""
        return self.__vaccins

    def get_traitements(self) -> list:
        """Return the list of treatments."""
        return self.__traitements

    # ── Automatic calculations ────────────────────────────────────────────────

    def get_nombre_restant(self) -> int:
        """Calculate and return the number of remaining animals.

        Formula: Initial number + Births - Deaths
        """
        return self.__nombre_initial + self.__naissances - self.__deces

    def get_taux_mortalite(self) -> float:
        """Calculate and return the mortality rate as a percentage.

        Formula: (Deaths / Initial number) × 100
        """
        if self.__nombre_initial == 0:
            return 0.0
        return (self.__deces / self.__nombre_initial) * 100

    def get_taux_natalite(self) -> float:
        """Calculate and return the birth rate as a percentage.

        Formula: (Births / Initial number) × 100
        """
        if self.__nombre_initial == 0:
            return 0.0
        return (self.__naissances / self.__nombre_initial) * 100

    # ── Update methods ────────────────────────────────────────────────────────

    def ajouter_deces(self, nombre: int) -> bool:
        """Add deaths to the counter.

        Args:
            nombre (int): Number of deaths to add.

        Returns:
            bool: True if successful, False if the number is invalid.
        """
        if nombre <= 0:
            return False
        if self.__deces + nombre > self.get_nombre_restant() + nombre:
            return False
        self.__deces += nombre
        return True

    def ajouter_naissance(self, nombre: int) -> bool:
        """Add births to the counter.

        Args:
            nombre (int): Number of births to add.

        Returns:
            bool: True if successful, False otherwise.
        """
        if nombre <= 0:
            return False
        self.__naissances += nombre
        return True

    def ajouter_vaccin(self, vaccin: Vaccin):
        """Add a vaccine to the vaccine list.

        Args:
            vaccin (Vaccin): The Vaccin object to add.
        """
        self.__vaccins.append(vaccin)

    def ajouter_traitement(self, traitement: Traitement):
        """Add a treatment to the treatment list.

        Args:
            traitement (Traitement): The Traitement object to add.
        """
        self.__traitements.append(traitement)

    # ── Alerts ────────────────────────────────────────────────────────────────

    def get_alertes(self) -> list:
        """Check and return alerts for important upcoming dates.

        Returns a list of alert messages for vaccines whose next
        dose date has passed or is due today.

        Returns:
            list: List of alert strings.
        """
        alertes = []
        aujourd_hui = str(date.today())

        # Loop through all vaccines and check their next dose date
        for vaccin in self.__vaccins:
            if vaccin.prochaine_dose <= aujourd_hui:
                alertes.append(f"⚠️ Vaccine reminder '{vaccin.get_nom()}' was due on {vaccin.prochaine_dose}!")

        return alertes

    # ── Serialization ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Convert the animal cycle to a dictionary for JSON saving."""
        return {
            "type_animal": self.__type_animal,
            "nombre_initial": self.__nombre_initial,
            "duree_cycle": self.__duree_cycle,
            "date_debut": self.__date_debut,
            "deces": self.__deces,
            "naissances": self.__naissances,
            "vaccins": [v.to_dict() for v in self.__vaccins],
            "traitements": [t.to_dict() for t in self.__traitements]
        }

    @staticmethod
    def from_dict(data: dict):
        """Create an Animal object from a dictionary (JSON loading).

        Args:
            data (dict): Dictionary containing the animal cycle data.

        Returns:
            Animal: The reconstructed Animal object.
        """
        animal = Animal(
            data["type_animal"],
            data["nombre_initial"],
            data["duree_cycle"],
            data["date_debut"]
        )
        # Restore deaths and births counts
        animal._Animal__deces = data["deces"]
        animal._Animal__naissances = data["naissances"]

        # Restore vaccines
        for v in data.get("vaccins", []):
            vaccin = Vaccin(v["nom"], v["date_creation"], v["prochaine_dose"])
            animal._Animal__vaccins.append(vaccin)

        # Restore treatments
        for t in data.get("traitements", []):
            traitement = Traitement(t["nom"], t["date_creation"], t["type_traitement"], t["dose"])
            animal._Animal__traitements.append(traitement)

        return animal
