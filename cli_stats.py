# cli_stats.py
# Command-line companion tool for FarmCare.
# Lets the user check cycle statistics and create a quick cycle directly from the terminal.
# This file demonstrates: input(), while loop, tuple indexing, elif, logical operators.

from data_manager import DataManager
from models import Animal
from utils import (durees_disponibles, types_animaux_disponibles,
                   valider_nombre_entier, valider_date,
                   formater_pourcentage, date_aujourd_hui)


# Constant: menu options stored in a tuple (accessed by index below)
MENU_OPTIONS: tuple = (
    "View all cycles",
    "Add a new cycle",
    "View statistics for a cycle",
    "Exit"
)


def afficher_menu():
    """Display the main menu options from the MENU_OPTIONS tuple."""
    print("\n" + "=" * 40)
    print("   FarmCare — Command-Line Tool")
    print("=" * 40)

    # Iterate over the tuple using its index (meaningful tuple usage)
    for i in range(len(MENU_OPTIONS)):
        print(f"  {i + 1}. {MENU_OPTIONS[i]}")   # tuple accessed by index

    print("=" * 40)


def afficher_tous_les_cycles(animaux: list):
    """Display a summary of all loaded livestock cycles.

    Args:
        animaux (list): List of Animal objects to display.
    """
    if not animaux:
        print("\n  No cycles found. Add one first.")
        return

    print(f"\n  Found {len(animaux)} cycle(s):\n")

    # for loop to display each cycle
    for i, animal in enumerate(animaux):
        print(f"  [{i + 1}] {animal.get_type_animal()}"
              f" | Initial: {animal.get_nombre_initial()}"
              f" | Remaining: {animal.get_nombre_restant()}"
              f" | Mortality: {formater_pourcentage(animal.get_taux_mortalite())}")


def saisir_nouveau_cycle() -> Animal:
    """Ask the user to enter details for a new cycle using input().

    Uses a while loop to keep asking until valid data is entered.

    Returns:
        Animal: The newly created Animal object.
    """
    print("\n  --- New Livestock Cycle ---")

    # Show available animal types (list used meaningfully)
    types = types_animaux_disponibles()
    print("\n  Available animal types:")
    for i, t in enumerate(types):
        print(f"    {i + 1}. {t}")

    # while loop: keep asking until the user picks a valid number
    type_animal: str = ""
    while type_animal == "":
        choix = input("\n  Enter the number for your animal type: ").strip()
        if valider_nombre_entier(choix, 1) and int(choix) <= len(types):
            type_animal = types[int(choix) - 1]
        else:
            print(f"  Invalid choice. Enter a number between 1 and {len(types)}.")

    # while loop: keep asking until a valid initial count is entered
    nombre_initial: int = 0
    while nombre_initial == 0:
        saisie = input("  Initial number of animals: ").strip()
        if valider_nombre_entier(saisie, 1):
            nombre_initial = int(saisie)   # type conversion: str -> int
        else:
            print("  Please enter a positive integer.")

    # Show available durations from the tuple
    durees = durees_disponibles()
    print("\n  Available cycle durations (days):")
    for i in range(len(durees)):
        print(f"    {i + 1}. {durees[i]} days")   # tuple accessed by index

    # while loop: keep asking until a valid duration is chosen
    duree_cycle: int = 0
    while duree_cycle == 0:
        choix = input("\n  Enter the number for the cycle duration: ").strip()
        if valider_nombre_entier(choix, 1) and int(choix) <= len(durees):
            duree_cycle = durees[int(choix) - 1]   # tuple accessed by index
        else:
            print(f"  Invalid choice. Enter a number between 1 and {len(durees)}.")

    # while loop: keep asking until a valid date is entered
    date_debut: str = ""
    while date_debut == "":
        saisie = input(f"  Start date (YYYY-MM-DD) [default: {date_aujourd_hui()}]: ").strip()
        if saisie == "":
            date_debut = date_aujourd_hui()   # use today if blank
        elif valider_date(saisie):
            date_debut = saisie
        else:
            print("  Invalid date format. Use YYYY-MM-DD (e.g. 2025-06-15).")

    # Create and return the Animal object
    nouvel_animal = Animal(type_animal, nombre_initial, duree_cycle, date_debut)
    print(f"\n  ✅ Cycle created: {type_animal} | {nombre_initial} animals | {duree_cycle} days")
    return nouvel_animal


def afficher_statistiques(animaux: list):
    """Show detailed statistics for a chosen cycle.

    Args:
        animaux (list): List of Animal objects.
    """
    if not animaux:
        print("\n  No cycles available.")
        return

    afficher_tous_les_cycles(animaux)

    # while loop: keep asking until a valid index is entered
    choix: int = 0
    while choix == 0:
        saisie = input("\n  Enter the cycle number to inspect: ").strip()
        if valider_nombre_entier(saisie, 1) and int(saisie) <= len(animaux):
            choix = int(saisie)
        else:
            print(f"  Enter a number between 1 and {len(animaux)}.")

    animal = animaux[choix - 1]

    # Display a formatted statistics block using f-strings
    print("\n" + "-" * 40)
    print(f"  Animal       : {animal.get_type_animal()}")
    print(f"  Start date   : {animal.get_date_debut()}")
    print(f"  Cycle        : {animal.get_duree_cycle()} days")
    print(f"  Initial      : {animal.get_nombre_initial()}")
    print(f"  Deaths       : {animal.get_deces()}")
    print(f"  Births       : {animal.get_naissances()}")
    print(f"  Remaining    : {animal.get_nombre_restant()}")
    print(f"  Mortality    : {formater_pourcentage(animal.get_taux_mortalite())}")
    print(f"  Birth rate   : {formater_pourcentage(animal.get_taux_natalite())}")

    # Show active alerts if any
    alertes = animal.get_alertes()
    if alertes:
        print("\n  ⚠️  Active alerts:")
        for alerte in alertes:
            print(f"     {alerte}")
    else:
        print("\n  ✅ No active alerts.")
    print("-" * 40)


def lancer_cli():
    """Launch the command-line interface for FarmCare.

    Uses a while loop to keep the menu running until the user exits.
    """
    print("\n  Welcome to FarmCare CLI!")

    # Load existing data
    dm = DataManager()
    animaux: list = dm.charger()
    print(f"  Loaded {len(animaux)} cycle(s) from file.")

    # Main application loop — while loop runs until user selects "Exit"
    continuer: bool = True
    while continuer:
        afficher_menu()

        # Read the user's menu choice using input() with type conversion
        saisie = input("  Your choice (1-4): ").strip()

        if not valider_nombre_entier(saisie, 1) or int(saisie) > 4:
            print("  Invalid choice. Enter a number between 1 and 4.")
            continue   # go back to the top of the while loop

        choix: int = int(saisie)   # str -> int conversion

        if choix == 1:
            afficher_tous_les_cycles(animaux)

        elif choix == 2:
            nouvel_animal = saisir_nouveau_cycle()
            animaux.append(nouvel_animal)
            dm.sauvegarder(animaux)
            print("  Data saved.")

        elif choix == 3:
            afficher_statistiques(animaux)

        elif choix == 4:
            print("\n  Goodbye! 🌿\n")
            continuer = False   # exit the while loop


# Entry point: only run when this file is executed directly
if __name__ == "__main__":
    lancer_cli()
