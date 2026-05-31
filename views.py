# views.py
# This file contains the different panels (views) of the graphical interface.
# Each view corresponds to a section of the FarmCare application.

import tkinter as tk
from tkinter import ttk, messagebox
from models import Animal
from dialogs import (DialogueAjouterDeces, DialogueAjouterNaissance,
                     DialogueAjouterVaccin, DialogueAjouterTraitement)
from utils import formater_pourcentage


class VueListeCycles(tk.Frame):
    """Main view displaying the list of all livestock cycles.

    Inherits from tk.Frame to integrate into the main interface.
    """

    def __init__(self, parent, callback_selectionner):
        """Initialize the list view.

        Args:
            parent: Parent Tkinter widget.
            callback_selectionner: Function called when the user selects a cycle.
        """
        super().__init__(parent)
        self.callback_selectionner = callback_selectionner

        self._construire_interface()

    def _construire_interface(self):
        """Build the visual elements of the list."""
        # Section title
        tk.Label(self, text="📋 My Livestock Cycles", font=("Arial", 13, "bold"),
                 bg="#E8F5E9").pack(fill="x", pady=(0, 5))

        # Table with columns
        colonnes = ("animal", "initial", "restant", "mortalite", "natalite", "duree")
        self.tableau = ttk.Treeview(self, columns=colonnes, show="headings", height=12)

        # Set column headers
        self.tableau.heading("animal", text="Animal")
        self.tableau.heading("initial", text="Initial count")
        self.tableau.heading("restant", text="Remaining")
        self.tableau.heading("mortalite", text="Mortality rate")
        self.tableau.heading("natalite", text="Birth rate")
        self.tableau.heading("duree", text="Duration (d)")

        # Column widths
        self.tableau.column("animal", width=120)
        self.tableau.column("initial", width=90)
        self.tableau.column("restant", width=80)
        self.tableau.column("mortalite", width=110)
        self.tableau.column("natalite", width=100)
        self.tableau.column("duree", width=80)

        # Vertical scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tableau.yview)
        self.tableau.configure(yscrollcommand=scrollbar.set)

        self.tableau.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Double-click event to open the detail view
        self.tableau.bind("<Double-Button-1>", self._sur_double_clic)

    def _sur_double_clic(self, event):
        """Handle double-click on a table row."""
        selection = self.tableau.selection()
        if selection:
            index = self.tableau.index(selection[0])
            self.callback_selectionner(index)

    def mettre_a_jour(self, animaux: list):
        """Refresh the table with the current list of animals.

        Args:
            animaux (list): List of Animal objects.
        """
        # Clear existing rows
        for ligne in self.tableau.get_children():
            self.tableau.delete(ligne)

        # Fill the table with updated data
        for animal in animaux:
            self.tableau.insert("", "end", values=(
                animal.get_type_animal(),
                animal.get_nombre_initial(),
                animal.get_nombre_restant(),
                formater_pourcentage(animal.get_taux_mortalite()),
                formater_pourcentage(animal.get_taux_natalite()),
                f"{animal.get_duree_cycle()} days"
            ))


class VueDetailCycle(tk.Toplevel):
    """Detail window for a single livestock cycle.

    Displays all information about an animal and allows
    actions such as recording deaths, births, vaccines, and treatments.
    """

    def __init__(self, parent, animal: Animal, callback_mise_a_jour):
        """Initialize the detail view.

        Args:
            parent: Parent window.
            animal (Animal): The animal cycle to display.
            callback_mise_a_jour: Function called after any modification.
        """
        super().__init__(parent)
        self.animal = animal
        self.callback_mise_a_jour = callback_mise_a_jour
        self.title(f"Detail - {animal.get_type_animal()}")
        self.geometry("620x600")
        self.resizable(True, True)

        self._construire_interface()
        self._afficher_donnees()

    def _construire_interface(self):
        """Build the interface for the detail window."""
        # Header title label
        self.label_titre = tk.Label(self, text="", font=("Arial", 15, "bold"), fg="#2E7D32")
        self.label_titre.pack(pady=10)

        # ── Statistics section ────────────────────────────────────────────────
        cadre_stats = tk.LabelFrame(self, text="📊 Statistics", padx=10, pady=8)
        cadre_stats.pack(fill="x", padx=15, pady=5)

        # Grid of statistics labels (4 columns)
        self.labels_stats = {}
        stats_infos = [
            ("Initial count", "initial"),
            ("Deaths", "deces"),
            ("Births", "naissances"),
            ("Remaining", "restant"),
            ("Mortality rate", "mortalite"),
            ("Birth rate", "natalite"),
            ("Cycle duration", "duree"),
            ("Start date", "debut"),
        ]

        for i, (texte, cle) in enumerate(stats_infos):
            ligne = i // 4
            colonne = (i % 4) * 2
            tk.Label(cadre_stats, text=f"{texte}:", font=("Arial", 9, "bold")).grid(
                row=ligne, column=colonne, sticky="e", padx=4, pady=3)
            lbl = tk.Label(cadre_stats, text="-", font=("Arial", 9), fg="#1565C0")
            lbl.grid(row=ligne, column=colonne + 1, sticky="w", padx=4, pady=3)
            self.labels_stats[cle] = lbl

        # ── Action buttons ────────────────────────────────────────────────────
        cadre_actions = tk.LabelFrame(self, text="⚙️ Actions", padx=10, pady=8)
        cadre_actions.pack(fill="x", padx=15, pady=5)

        boutons = [
            ("💀 Deaths", self._ajouter_deces, "#E53935"),
            ("🐣 Births", self._ajouter_naissance, "#43A047"),
            ("💉 Vaccine", self._ajouter_vaccin, "#1E88E5"),
            ("💊 Treatment", self._ajouter_traitement, "#8E24AA"),
        ]

        for texte, commande, couleur in boutons:
            tk.Button(cadre_actions, text=texte, command=commande,
                      bg=couleur, fg="white", width=14, padx=5).pack(side="left", padx=5)

        # ── Vaccine / Treatment tabs ──────────────────────────────────────────
        self.onglets = ttk.Notebook(self)
        self.onglets.pack(fill="both", expand=True, padx=15, pady=5)

        # Vaccines tab
        cadre_vaccins = tk.Frame(self.onglets)
        self.onglets.add(cadre_vaccins, text="💉 Vaccines")
        self.liste_vaccins = tk.Listbox(cadre_vaccins, height=6, font=("Courier", 9))
        self.liste_vaccins.pack(fill="both", expand=True, padx=5, pady=5)

        # Treatments tab
        cadre_traitements = tk.Frame(self.onglets)
        self.onglets.add(cadre_traitements, text="💊 Treatments")
        self.liste_traitements = tk.Listbox(cadre_traitements, height=6, font=("Courier", 9))
        self.liste_traitements.pack(fill="both", expand=True, padx=5, pady=5)

    def _afficher_donnees(self):
        """Update the display with the current data for this animal cycle."""
        animal = self.animal

        self.label_titre.config(text=f"🐄 {animal.get_type_animal()} — {animal.get_duree_cycle()}-day cycle")

        # Update statistics labels
        self.labels_stats["initial"].config(text=str(animal.get_nombre_initial()))
        self.labels_stats["deces"].config(text=str(animal.get_deces()))
        self.labels_stats["naissances"].config(text=str(animal.get_naissances()))
        self.labels_stats["restant"].config(text=str(animal.get_nombre_restant()))
        self.labels_stats["mortalite"].config(text=formater_pourcentage(animal.get_taux_mortalite()))
        self.labels_stats["natalite"].config(text=formater_pourcentage(animal.get_taux_natalite()))
        self.labels_stats["duree"].config(text=f"{animal.get_duree_cycle()} days")
        self.labels_stats["debut"].config(text=animal.get_date_debut())

        # Update the vaccine list
        self.liste_vaccins.delete(0, tk.END)
        for vaccin in animal.get_vaccins():
            self.liste_vaccins.insert(tk.END, vaccin.afficher_info())

        # Update the treatment list
        self.liste_traitements.delete(0, tk.END)
        for traitement in animal.get_traitements():
            self.liste_traitements.insert(tk.END, traitement.afficher_info())

    def _ajouter_deces(self):
        """Open the dialog window to record deaths."""
        dialogue = DialogueAjouterDeces(self, self.animal.get_type_animal())
        self.wait_window(dialogue)
        if dialogue.resultat is not None:
            succes = self.animal.ajouter_deces(dialogue.resultat)
            if succes:
                messagebox.showinfo("Success", f"{dialogue.resultat} death(s) recorded.", parent=self)
                self._afficher_donnees()
                self.callback_mise_a_jour()
            else:
                messagebox.showerror("Error", "Invalid number of deaths.", parent=self)

    def _ajouter_naissance(self):
        """Open the dialog window to record births."""
        dialogue = DialogueAjouterNaissance(self, self.animal.get_type_animal())
        self.wait_window(dialogue)
        if dialogue.resultat is not None:
            succes = self.animal.ajouter_naissance(dialogue.resultat)
            if succes:
                messagebox.showinfo("Success", f"{dialogue.resultat} birth(s) recorded.", parent=self)
                self._afficher_donnees()
                self.callback_mise_a_jour()
            else:
                messagebox.showerror("Error", "Invalid number of births.", parent=self)

    def _ajouter_vaccin(self):
        """Open the dialog window to add a vaccine."""
        dialogue = DialogueAjouterVaccin(self, self.animal.get_type_animal())
        self.wait_window(dialogue)
        if dialogue.resultat is not None:
            self.animal.ajouter_vaccin(dialogue.resultat)
            messagebox.showinfo("Success", "Vaccine added successfully.", parent=self)
            self._afficher_donnees()
            self.callback_mise_a_jour()

    def _ajouter_traitement(self):
        """Open the dialog window to add a treatment."""
        dialogue = DialogueAjouterTraitement(self, self.animal.get_type_animal())
        self.wait_window(dialogue)
        if dialogue.resultat is not None:
            self.animal.ajouter_traitement(dialogue.resultat)
            messagebox.showinfo("Success", "Treatment added successfully.", parent=self)
            self._afficher_donnees()
            self.callback_mise_a_jour()


class VueAlertes(tk.Toplevel):
    """Window displaying all active alerts across all livestock cycles."""

    def __init__(self, parent, animaux: list):
        """Initialize the alerts window.

        Args:
            parent: Parent window.
            animaux (list): List of Animal objects to check for alerts.
        """
        super().__init__(parent)
        self.title("⚠️ FarmCare Alerts")
        self.geometry("500x350")
        self.resizable(False, False)

        self._construire_interface(animaux)

    def _construire_interface(self, animaux: list):
        """Build the alert display interface."""
        tk.Label(self, text="⚠️ Active Alerts", font=("Arial", 14, "bold"), fg="#E65100").pack(pady=10)

        # Collect all alerts from all animal cycles
        toutes_alertes = []
        for animal in animaux:
            alertes = animal.get_alertes()
            for alerte in alertes:
                toutes_alertes.append(f"[{animal.get_type_animal()}] {alerte}")

        if not toutes_alertes:
            # No alerts to show
            tk.Label(self, text="✅ No alerts at this time.\nAll your animals are up to date!",
                     font=("Arial", 11), fg="#2E7D32").pack(pady=30)
        else:
            # Display alerts in a scrollable list
            cadre = tk.Frame(self)
            cadre.pack(fill="both", expand=True, padx=15, pady=5)

            liste = tk.Listbox(cadre, font=("Arial", 10), bg="#FFF3E0",
                               selectbackground="#FF8F00", height=10)
            scrollbar = ttk.Scrollbar(cadre, command=liste.yview)
            liste.configure(yscrollcommand=scrollbar.set)

            # Use a for loop to populate the alert list
            for alerte in toutes_alertes:
                liste.insert(tk.END, alerte)

            liste.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            tk.Label(self, text=f"{len(toutes_alertes)} alert(s) found.",
                     font=("Arial", 10, "italic"), fg="#BF360C").pack(pady=5)

        tk.Button(self, text="Close", command=self.destroy,
                  bg="#607D8B", fg="white", width=12).pack(pady=10)
