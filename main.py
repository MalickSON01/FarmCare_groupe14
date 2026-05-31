# main.py
# Main entry point of the FarmCare application.
# Launches the Tkinter graphical interface and coordinates all features.

import tkinter as tk
from tkinter import messagebox

from models import Animal
from data_manager import DataManager
from views import VueListeCycles, VueDetailCycle, VueAlertes
from dialogs import DialogueNouveauCycle


# ─── Application constants ────────────────────────────────────────────────────
TITRE_APPLICATION: str = "FarmCare - Livestock Management"
VERSION: str = "1.0"


class ApplicationFarmCare:
    """Main class of the FarmCare application.

    Coordinates the graphical interface, data management, and user interactions.
    """

    def __init__(self, fenetre_principale: tk.Tk):
        """Initialize the FarmCare application.

        Args:
            fenetre_principale (tk.Tk): The root Tkinter window.
        """
        self.fenetre = fenetre_principale
        self.fenetre.title(f"{TITRE_APPLICATION} v{VERSION}")
        self.fenetre.geometry("780x540")
        self.fenetre.resizable(True, True)
        self.fenetre.configure(bg="#F1F8E9")

        # Data manager instance for saving and loading
        self.data_manager = DataManager()

        # In-memory list of animal cycles
        self.animaux: list = []

        # Load existing data from the JSON file
        self.animaux = self.data_manager.charger()

        # Build the interface
        self._construire_interface()

        # Display the loaded data in the table
        self.vue_liste.mettre_a_jour(self.animaux)

        # Check for alerts on startup if data exists
        if self.animaux:
            self._verifier_alertes_silencieuses()

    def _construire_interface(self):
        """Build the main interface of the application."""
        # ── Title bar ─────────────────────────────────────────────────────────
        cadre_titre = tk.Frame(self.fenetre, bg="#33691E", pady=8)
        cadre_titre.pack(fill="x")

        tk.Label(cadre_titre,
                 text="🌿 FarmCare — Livestock Management",
                 font=("Arial", 16, "bold"),
                 bg="#33691E", fg="white").pack(side="left", padx=15)

        tk.Label(cadre_titre,
                 text=f"v{VERSION}",
                 font=("Arial", 10),
                 bg="#33691E", fg="#CCFF90").pack(side="right", padx=15)

        # ── Toolbar (main action buttons) ─────────────────────────────────────
        cadre_outils = tk.Frame(self.fenetre, bg="#DCEDC8", pady=6)
        cadre_outils.pack(fill="x")

        boutons_barre = [
            ("➕ New Cycle", self._nouveau_cycle, "#4CAF50"),
            ("🔍 View Detail", self._voir_detail, "#1976D2"),
            ("⚠️ Alerts", self._afficher_alertes, "#FF6F00"),
            ("🗑️ Delete", self._supprimer_cycle, "#E53935"),
            ("💾 Save", self._sauvegarder, "#5D4037"),
        ]

        for texte, commande, couleur in boutons_barre:
            tk.Button(cadre_outils, text=texte, command=commande,
                      bg=couleur, fg="white", padx=8, pady=4,
                      font=("Arial", 9, "bold")).pack(side="left", padx=5, pady=2)

        # ── Main area: list of cycles ──────────────────────────────────────────
        cadre_principal = tk.Frame(self.fenetre, bg="#F1F8E9")
        cadre_principal.pack(fill="both", expand=True, padx=10, pady=5)

        # Create and embed the list view
        self.vue_liste = VueListeCycles(cadre_principal, self._selectionner_cycle)
        self.vue_liste.pack(fill="both", expand=True)

        # ── Status bar ────────────────────────────────────────────────────────
        self.label_statut = tk.Label(self.fenetre,
                                     text="Ready. Double-click a cycle to view details.",
                                     anchor="w", bg="#C8E6C9", font=("Arial", 9), pady=4)
        self.label_statut.pack(fill="x", side="bottom")

    def _mettre_a_jour_statut(self, message: str):
        """Update the status bar message.

        Args:
            message (str): The message to display.
        """
        self.label_statut.config(text=f"  {message}")

    def _nouveau_cycle(self):
        """Open the dialog to create a new livestock cycle."""
        dialogue = DialogueNouveauCycle(self.fenetre)
        self.fenetre.wait_window(dialogue)

        if dialogue.resultat is not None:
            # Create a new Animal object from the form data
            nouvel_animal = Animal(
                dialogue.resultat["type_animal"],
                dialogue.resultat["nombre_initial"],
                dialogue.resultat["duree_cycle"],
                dialogue.resultat["date_debut"]
            )
            self.animaux.append(nouvel_animal)
            self.vue_liste.mettre_a_jour(self.animaux)
            self._sauvegarder()
            self._mettre_a_jour_statut(f"Cycle '{nouvel_animal.get_type_animal()}' created successfully.")

    def _selectionner_cycle(self, index: int):
        """Open the detail window for the selected cycle.

        Args:
            index (int): Index of the animal in the list.
        """
        if 0 <= index < len(self.animaux):
            animal = self.animaux[index]
            VueDetailCycle(self.fenetre, animal, self._apres_modification)

    def _voir_detail(self):
        """Open the detail view for the currently selected cycle via the toolbar button."""
        selection = self.vue_liste.tableau.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a cycle from the list.")
            return
        index = self.vue_liste.tableau.index(selection[0])
        self._selectionner_cycle(index)

    def _supprimer_cycle(self):
        """Delete the selected cycle after user confirmation."""
        selection = self.vue_liste.tableau.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a cycle to delete.")
            return

        index = self.vue_liste.tableau.index(selection[0])
        animal = self.animaux[index]

        # Ask the user to confirm before deleting
        confirme = messagebox.askyesno(
            "Confirm Deletion",
            f"Permanently delete the cycle '{animal.get_type_animal()}'?\n"
            f"This action cannot be undone."
        )

        if confirme:
            del self.animaux[index]
            self.vue_liste.mettre_a_jour(self.animaux)
            self._sauvegarder()
            self._mettre_a_jour_statut("Cycle deleted.")

    def _afficher_alertes(self):
        """Open the alerts window."""
        if not self.animaux:
            messagebox.showinfo("Alerts", "No livestock cycles recorded yet.")
            return
        VueAlertes(self.fenetre, self.animaux)

    def _sauvegarder(self):
        """Save all data to the JSON file."""
        succes = self.data_manager.sauvegarder(self.animaux)
        if succes:
            self._mettre_a_jour_statut(f"Data saved ({len(self.animaux)} cycle(s)).")
        else:
            messagebox.showerror("Error", "Saving failed.")

    def _apres_modification(self):
        """Callback triggered after any modification to an animal cycle.

        Refreshes the list view and auto-saves the data.
        """
        self.vue_liste.mettre_a_jour(self.animaux)
        self._sauvegarder()

    def _verifier_alertes_silencieuses(self):
        """Check for urgent alerts on startup and notify the user via the status bar."""
        total_alertes = 0
        for animal in self.animaux:
            total_alertes += len(animal.get_alertes())

        if total_alertes > 0:
            self._mettre_a_jour_statut(
                f"⚠️ {total_alertes} active alert(s)! Click 'Alerts' to view them."
            )


# ─── Entry point ──────────────────────────────────────────────────────────────

def lancer_application():
    """Create and launch the FarmCare application."""
    # Create the root Tkinter window
    fenetre = tk.Tk()

    # Instantiate the main application class
    app = ApplicationFarmCare(fenetre)

    # Start the Tkinter main event loop
    fenetre.mainloop()


# This block only runs when the file is executed directly
if __name__ == "__main__":
    lancer_application()
