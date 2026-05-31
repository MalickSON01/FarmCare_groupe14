# dialogs.py
# This file contains all the dialog windows (popups) of the application.
# Each dialog corresponds to a specific user action.

import tkinter as tk
from tkinter import ttk, messagebox
from utils import valider_nombre_entier, valider_date, date_aujourd_hui, durees_disponibles, types_animaux_disponibles
from models import Vaccin, Traitement


class DialogueNouveauCycle(tk.Toplevel):
    """Dialog window for creating a new livestock cycle."""

    def __init__(self, parent):
        """Initialize the new cycle creation window.

        Args:
            parent: The parent Tkinter window.
        """
        super().__init__(parent)
        self.title("New Livestock Cycle")
        self.geometry("400x320")
        self.resizable(False, False)
        self.grab_set()  # Block interaction with the parent window

        # Result is None if the user cancels
        self.resultat = None

        self._construire_interface()

    def _construire_interface(self):
        """Build the widgets for this window."""
        # Title label
        tk.Label(self, text="New Cycle", font=("Arial", 14, "bold")).pack(pady=10)

        cadre = tk.Frame(self)
        cadre.pack(padx=20, fill="x")

        # Animal type dropdown
        tk.Label(cadre, text="Animal type:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_animal = ttk.Combobox(cadre, values=types_animaux_disponibles(), state="readonly", width=20)
        self.combo_animal.current(0)
        self.combo_animal.grid(row=0, column=1, pady=5, padx=5)

        # Initial count
        tk.Label(cadre, text="Initial count:").grid(row=1, column=0, sticky="w", pady=5)
        self.entree_nombre = tk.Entry(cadre, width=22)
        self.entree_nombre.insert(0, "100")
        self.entree_nombre.grid(row=1, column=1, pady=5, padx=5)

        # Cycle duration
        tk.Label(cadre, text="Cycle duration (days):").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_duree = ttk.Combobox(cadre, values=list(durees_disponibles()), state="readonly", width=20)
        self.combo_duree.current(0)
        self.combo_duree.grid(row=2, column=1, pady=5, padx=5)

        # Start date
        tk.Label(cadre, text="Start date (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", pady=5)
        self.entree_date = tk.Entry(cadre, width=22)
        self.entree_date.insert(0, date_aujourd_hui())
        self.entree_date.grid(row=3, column=1, pady=5, padx=5)

        # Action buttons
        cadre_boutons = tk.Frame(self)
        cadre_boutons.pack(pady=15)
        tk.Button(cadre_boutons, text="✅ Create", command=self._valider,
                  bg="#4CAF50", fg="white", width=10).pack(side="left", padx=5)
        tk.Button(cadre_boutons, text="❌ Cancel", command=self.destroy,
                  bg="#f44336", fg="white", width=10).pack(side="left", padx=5)

    def _valider(self):
        """Validate the entered data and close the window if everything is correct."""
        nombre_str = self.entree_nombre.get().strip()
        date_str = self.entree_date.get().strip()

        if not valider_nombre_entier(nombre_str, 1):
            messagebox.showerror("Error", "Initial count must be a positive integer.", parent=self)
            return

        if not valider_date(date_str):
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format (e.g. 2025-06-15).", parent=self)
            return

        # Store the result as a dictionary
        self.resultat = {
            "type_animal": self.combo_animal.get(),
            "nombre_initial": int(nombre_str),
            "duree_cycle": int(self.combo_duree.get()),
            "date_debut": date_str
        }
        self.destroy()


class DialogueAjouterDeces(tk.Toplevel):
    """Dialog window for recording deaths."""

    def __init__(self, parent, nom_animal: str):
        """Initialize the death entry window.

        Args:
            parent: Parent window.
            nom_animal (str): Name of the animal cycle concerned.
        """
        super().__init__(parent)
        self.title("Record Deaths")
        self.geometry("320x200")
        self.resizable(False, False)
        self.grab_set()

        self.resultat = None

        self._construire_interface(nom_animal)

    def _construire_interface(self, nom_animal: str):
        """Build the widgets."""
        tk.Label(self, text=f"Animal: {nom_animal}", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(self, text="Number of deaths to record:").pack()

        self.entree = tk.Entry(self, width=15, justify="center")
        self.entree.insert(0, "1")
        self.entree.pack(pady=8)

        cadre = tk.Frame(self)
        cadre.pack(pady=10)
        tk.Button(cadre, text="✅ Confirm", command=self._valider,
                  bg="#FF5722", fg="white", width=10).pack(side="left", padx=5)
        tk.Button(cadre, text="❌ Cancel", command=self.destroy,
                  bg="#9E9E9E", fg="white", width=10).pack(side="left", padx=5)

    def _valider(self):
        """Validate the input."""
        valeur = self.entree.get().strip()
        if not valider_nombre_entier(valeur, 1):
            messagebox.showerror("Error", "Please enter a positive integer.", parent=self)
            return
        self.resultat = int(valeur)
        self.destroy()


class DialogueAjouterNaissance(tk.Toplevel):
    """Dialog window for recording births."""

    def __init__(self, parent, nom_animal: str):
        """Initialize the birth entry window.

        Args:
            parent: Parent window.
            nom_animal (str): Name of the animal cycle concerned.
        """
        super().__init__(parent)
        self.title("Record Births")
        self.geometry("320x200")
        self.resizable(False, False)
        self.grab_set()

        self.resultat = None

        self._construire_interface(nom_animal)

    def _construire_interface(self, nom_animal: str):
        """Build the widgets."""
        tk.Label(self, text=f"Animal: {nom_animal}", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(self, text="Number of births to record:").pack()

        self.entree = tk.Entry(self, width=15, justify="center")
        self.entree.insert(0, "1")
        self.entree.pack(pady=8)

        cadre = tk.Frame(self)
        cadre.pack(pady=10)
        tk.Button(cadre, text="✅ Confirm", command=self._valider,
                  bg="#4CAF50", fg="white", width=10).pack(side="left", padx=5)
        tk.Button(cadre, text="❌ Cancel", command=self.destroy,
                  bg="#9E9E9E", fg="white", width=10).pack(side="left", padx=5)

    def _valider(self):
        """Validate the input."""
        valeur = self.entree.get().strip()
        if not valider_nombre_entier(valeur, 1):
            messagebox.showerror("Error", "Please enter a positive integer.", parent=self)
            return
        self.resultat = int(valeur)
        self.destroy()


class DialogueAjouterVaccin(tk.Toplevel):
    """Dialog window for adding a vaccine."""

    def __init__(self, parent, nom_animal: str):
        """Initialize the vaccine entry window.

        Args:
            parent: Parent window.
            nom_animal (str): Name of the animal cycle concerned.
        """
        super().__init__(parent)
        self.title("Add a Vaccine")
        self.geometry("380x280")
        self.resizable(False, False)
        self.grab_set()

        self.resultat = None

        self._construire_interface(nom_animal)

    def _construire_interface(self, nom_animal: str):
        """Build the widgets."""
        tk.Label(self, text=f"💉 Vaccine for: {nom_animal}", font=("Arial", 12, "bold")).pack(pady=10)

        cadre = tk.Frame(self)
        cadre.pack(padx=20, fill="x")

        # Vaccine name
        tk.Label(cadre, text="Vaccine name:").grid(row=0, column=0, sticky="w", pady=5)
        self.entree_nom = tk.Entry(cadre, width=22)
        self.entree_nom.grid(row=0, column=1, pady=5, padx=5)

        # Vaccine date
        tk.Label(cadre, text="Vaccine date (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", pady=5)
        self.entree_date = tk.Entry(cadre, width=22)
        self.entree_date.insert(0, date_aujourd_hui())
        self.entree_date.grid(row=1, column=1, pady=5, padx=5)

        # Next dose date
        tk.Label(cadre, text="Next dose (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", pady=5)
        self.entree_prochaine = tk.Entry(cadre, width=22)
        self.entree_prochaine.grid(row=2, column=1, pady=5, padx=5)

        cadre_boutons = tk.Frame(self)
        cadre_boutons.pack(pady=15)
        tk.Button(cadre_boutons, text="✅ Add", command=self._valider,
                  bg="#2196F3", fg="white", width=10).pack(side="left", padx=5)
        tk.Button(cadre_boutons, text="❌ Cancel", command=self.destroy,
                  bg="#9E9E9E", fg="white", width=10).pack(side="left", padx=5)

    def _valider(self):
        """Validate the data and create the Vaccin object."""
        nom = self.entree_nom.get().strip()
        date_vaccin = self.entree_date.get().strip()
        prochaine = self.entree_prochaine.get().strip()

        if not nom:
            messagebox.showerror("Error", "Vaccine name is required.", parent=self)
            return
        if not valider_date(date_vaccin):
            messagebox.showerror("Error", "Invalid vaccine date. Format: YYYY-MM-DD", parent=self)
            return
        if prochaine and not valider_date(prochaine):
            messagebox.showerror("Error", "Invalid next dose date. Format: YYYY-MM-DD", parent=self)
            return

        if not prochaine:
            prochaine = "Not defined"

        # Create a Vaccin object (child class of Enregistrement)
        self.resultat = Vaccin(nom, date_vaccin, prochaine)
        self.destroy()


class DialogueAjouterTraitement(tk.Toplevel):
    """Dialog window for adding a medical treatment."""

    def __init__(self, parent, nom_animal: str):
        """Initialize the treatment entry window.

        Args:
            parent: Parent window.
            nom_animal (str): Name of the animal cycle concerned.
        """
        super().__init__(parent)
        self.title("Add a Treatment")
        self.geometry("380x310")
        self.resizable(False, False)
        self.grab_set()

        self.resultat = None

        self._construire_interface(nom_animal)

    def _construire_interface(self, nom_animal: str):
        """Build the widgets."""
        tk.Label(self, text=f"💊 Treatment for: {nom_animal}", font=("Arial", 12, "bold")).pack(pady=10)

        cadre = tk.Frame(self)
        cadre.pack(padx=20, fill="x")

        # Treatment type
        tk.Label(cadre, text="Type:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_type = ttk.Combobox(cadre, values=list(Traitement.TYPES_VALIDES), state="readonly", width=20)
        self.combo_type.current(0)
        self.combo_type.grid(row=0, column=1, pady=5, padx=5)

        # Medicine name
        tk.Label(cadre, text="Medicine name:").grid(row=1, column=0, sticky="w", pady=5)
        self.entree_nom = tk.Entry(cadre, width=22)
        self.entree_nom.grid(row=1, column=1, pady=5, padx=5)

        # Date
        tk.Label(cadre, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", pady=5)
        self.entree_date = tk.Entry(cadre, width=22)
        self.entree_date.insert(0, date_aujourd_hui())
        self.entree_date.grid(row=2, column=1, pady=5, padx=5)

        # Dosage
        tk.Label(cadre, text="Dose / Quantity:").grid(row=3, column=0, sticky="w", pady=5)
        self.entree_dose = tk.Entry(cadre, width=22)
        self.entree_dose.insert(0, "1 tablet")
        self.entree_dose.grid(row=3, column=1, pady=5, padx=5)

        cadre_boutons = tk.Frame(self)
        cadre_boutons.pack(pady=15)
        tk.Button(cadre_boutons, text="✅ Add", command=self._valider,
                  bg="#9C27B0", fg="white", width=10).pack(side="left", padx=5)
        tk.Button(cadre_boutons, text="❌ Cancel", command=self.destroy,
                  bg="#9E9E9E", fg="white", width=10).pack(side="left", padx=5)

    def _valider(self):
        """Validate the data and create the Traitement object."""
        nom = self.entree_nom.get().strip()
        date_str = self.entree_date.get().strip()
        dose = self.entree_dose.get().strip()

        if not nom:
            messagebox.showerror("Error", "Medicine name is required.", parent=self)
            return
        if not valider_date(date_str):
            messagebox.showerror("Error", "Invalid date. Format: YYYY-MM-DD", parent=self)
            return
        if not dose:
            messagebox.showerror("Error", "Dose is required.", parent=self)
            return

        # Create a Traitement object (child class of Enregistrement)
        self.resultat = Traitement(nom, date_str, self.combo_type.get(), dose)
        self.destroy()
