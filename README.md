# 🌿 FarmCare — Livestock Management System

## 1. Project Title and Description

**FarmCare** is a desktop application built in Python that helps farmers manage their livestock simply and efficiently. The application allows users to track deaths, births, vaccines, and medical treatments, while automatically calculating key farming statistics such as mortality rate, birth rate, and remaining animal count.

Users can create **livestock cycles** for different animal types (chickens, sheep, goats, etc.), monitor their progress over time, and receive alerts for upcoming or overdue vaccine reminders.

---

## 2. How to Run the Project

### Requirements

- Python **3.8 or higher** — download from [python.org](https://www.python.org/downloads/)
- **Tkinter** is included by default with Python on Windows and macOS

> On Linux (Ubuntu/Debian), install Tkinter if needed:
> ```bash
> sudo apt-get install python3-tk
> ```
> On windows just install tkinter via:
> ```bash
> pip install tk
> ```
### Steps

1. **Clone or download the repository**:
   ```bash
   git clone [https://github.com/MalickSON01/FarmCare_groupe14]
   cd FarmCare_groupe14
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

3. The graphical interface opens automatically. No additional installation is required.

> **Note:** Data is saved automatically to a `farmcare_data.json` file created in the same folder as the program.

---

## 3. Features

- ➕ **Create a livestock cycle** — choose animal type, initial count, cycle duration, and start date
- 💀 **Record deaths** — update the death counter for any cycle
- 🐣 **Record births** — add new births to a cycle
- 📊 **Automatic calculations**:
  - Remaining = Initial count + Births − Deaths
  - Mortality rate = (Deaths / Initial count) × 100
  - Birth rate = (Births / Initial count) × 100
- 💉 **Manage vaccines** — record vaccine name, date administered, and next dose date
- 💊 **Manage treatments** — tablets, vitamins, antibiotics, and other medical treatments
- ⚠️ **Automatic alerts** — notifications for overdue vaccine reminders
- 💾 **Auto-save** — all data is persisted locally in a JSON file
- 🗑️ **Delete a cycle** — with confirmation prompt

---

## 4. Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Main programming language |
| Tkinter | Built-in | Graphical user interface |
| JSON | Built-in | Data persistence |
| os | Built-in | File existence checks |
| datetime | Built-in | Date handling and alert logic |
| re | Built-in | Date format validation |

---

## 5. Project Structure

```
farmcare/
│
├── main.py           # Entry point — launches the app and manages the main window
├── models.py         # Data classes: Enregistrement, Vaccin, Traitement, Animal
├── data_manager.py   # Saves and loads data using JSON
├── utils.py          # Utility functions: validation, formatting, constants
├── dialogs.py        # Tkinter dialog windows for all user actions
├── views.py          # Display panels: cycle list, detail view, alerts window
│
├── farmcare_data.json  # Auto-generated data file (created on first run)
└── README.md           # This documentation file
```

---

## 6. OOP Structure

### Class `Enregistrement` *(Parent class)*
- **Role**: Represents a generic record with a name and a date
- **Inherits from**: nothing (base class)
- **Key attributes**: `__nom` (private), `__date_creation` (private)
- **Key methods**: `get_nom()`, `get_date_creation()`, `set_nom()`, `afficher_info()`, `to_dict()`
- **OOP principle**: Encapsulation — private attributes with getters and setters

### Class `Vaccin` *(Child class)*
- **Role**: Represents a vaccine administered to an animal
- **Inherits from**: `Enregistrement`
- **Additional attributes**: `prochaine_dose`
- **Key methods**: `afficher_info()` *(overridden)*, `to_dict()`
- **OOP principles**: Inheritance + Polymorphism (overrides `afficher_info`)

### Class `Traitement` *(Child class)*
- **Role**: Represents a medical treatment (tablet, antibiotic, vitamin...)
- **Inherits from**: `Enregistrement`
- **Additional attributes**: `type_traitement`, `dose`
- **Key methods**: `afficher_info()` *(overridden)*, `to_dict()`
- **OOP principles**: Inheritance + Polymorphism (overrides `afficher_info`)

### Class `Animal`
- **Role**: Represents a complete livestock cycle with full statistics
- **Key attributes**: all private — `__type_animal`, `__nombre_initial`, `__duree_cycle`, `__date_debut`, `__deces`, `__naissances`, `__vaccins`, `__traitements`
- **Key methods**: `ajouter_deces()`, `ajouter_naissance()`, `get_nombre_restant()`, `get_taux_mortalite()`, `get_taux_natalite()`, `get_alertes()`, `to_dict()`, `from_dict()`
- **OOP principles**: Encapsulation + Abstraction

### Class `DataManager`
- **Role**: Manages saving and loading of JSON data
- **Key methods**: `sauvegarder()`, `charger()`, `fichier_existe()`

### Summary of the 4 OOP Principles

| Principle | Where it is visible |
|-----------|-------------------|
| **Encapsulation** | Private attributes (`__nom`, `__deces`, etc.) in `Enregistrement` and `Animal` |
| **Abstraction** | `get_nombre_restant()` hides the internal formula |
| **Inheritance** | `Vaccin` and `Traitement` inherit from `Enregistrement` |
| **Polymorphism** | `afficher_info()` behaves differently in `Vaccin` vs `Traitement` |

---

## 7. Acknowledgements

- Official Python documentation: [https://docs.python.org/3/](https://docs.python.org/3/)
- Tkinter documentation: [https://docs.python.org/3/library/tkinter.html](https://docs.python.org/3/library/tkinter.html)
- JSON module documentation: [https://docs.python.org/3/library/json.html](https://docs.python.org/3/library/json.html)
- Programming I Course — Burkina Institute of Technology (BIT), 2026
- Lecturer: Ms. Kweyakie Afi Blebo

---

## 8. Group Members

| Full Name | GitHub Profile |
|-----------|---------------|
| Member 1 | [@github_member1](https://github.com/) |
| Member 2 | [@github_member2](https://github.com/) |
| Member 3 | [@github_member3](https://github.com/) |

> ⚠️ Replace the information above with your group's real names and GitHub profile links.
