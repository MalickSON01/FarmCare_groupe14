"""
╔══════════════════════════════════════════════╗
║        FarmCare - Gestion d'Élevage          ║
║        Python 3 + Tkinter + JSON             ║
╚══════════════════════════════════════════════╝

Structure :
    farmcare/
    ├── main.py          ← ce fichier (tout-en-un)
    └── data/
        └── elevage.json (créé automatiquement)

Lancer :  python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import date, datetime
import json, os, uuid

# ═══════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "elevage.json")

COULEURS = {
    "bg":        "#010409",
    "surface":   "#0d1117",
    "border":    "#21262d",
    "border2":   "#30363d",
    "text":      "#e6edf3",
    "muted":     "#8b949e",
    "green":     "#4ade80",
    "green_bg":  "#0f2e1a",
    "red":       "#f87171",
    "red_bg":    "#2e0f0f",
    "amber":     "#fbbf24",
    "amber_bg":  "#2e1f0f",
    "blue":      "#60a5fa",
    "blue_bg":   "#0f1e2e",
    "purple":    "#c084fc",
}

ANIMAUX = [
    ("Poulet",  "🐔"),
    ("Vache",   "🐄"),
    ("Cochon",  "🐷"),
    ("Mouton",  "🐑"),
    ("Lapin",   "🐰"),
    ("Poisson", "🐟"),
    ("Chèvre",  "🐐"),
    ("Dinde",   "🦃"),
]

DUREES = [30, 45, 60, 90, 120, 180]

# ═══════════════════════════════════════════════
# STOCKAGE JSON
# ═══════════════════════════════════════════════
def charger():
    if not os.path.exists(DATA_FILE):
        return {"cycles": [], "active_id": None}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def sauvegarder(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ═══════════════════════════════════════════════
# ALERTES
# ═══════════════════════════════════════════════
def get_alertes(cycles):
    alertes = []
    today = date.today()
    for c in cycles:
        debut = datetime.strptime(c["date_debut"], "%Y-%m-%d").date()
        fin_date = date.fromordinal(debut.toordinal() + c["duree_jours"])
        delta_fin = (fin_date - today).days
        if 0 <= delta_fin <= 7:
            niveau = "DANGER" if delta_fin <= 1 else "WARNING"
            alertes.append((niveau, f"🏁 Fin de cycle {c['emoji']} {c['type_animal']} dans {delta_fin}j"))
        for v in c.get("vaccins", []):
            d = datetime.strptime(v["date"], "%Y-%m-%d").date()
            diff = (d - today).days
            if -1 <= diff <= 5:
                alertes.append(("DANGER" if diff <= 0 else "WARNING",
                                 f"💉 Vaccin '{v['nom']}' {'AUJOURD\'HUI' if diff == 0 else f'dans {diff}j'}"))
        for t in c.get("traitements", []):
            d = datetime.strptime(t["date"], "%Y-%m-%d").date()
            diff = (d - today).days
            if -1 <= diff <= 5:
                alertes.append(("DANGER" if diff <= 0 else "WARNING",
                                 f"💊 Traitement '{t['nom']}' {'AUJOURD\'HUI' if diff == 0 else f'dans {diff}j'}"))
        if c["nombre_initial"] > 0:
            taux = (c["deces"] / c["nombre_initial"]) * 100
            if taux >= 10:
                alertes.append(("DANGER" if taux >= 20 else "WARNING",
                                 f"⚠️ Mortalité {taux:.1f}% — {c['emoji']} {c['type_animal']}"))
    return alertes

# ═══════════════════════════════════════════════
# HELPERS UI
# ═══════════════════════════════════════════════
def label(parent, text, size=12, color=None, bold=False, font="Courier"):
    fg = color or COULEURS["text"]
    weight = "bold" if bold else "normal"
    return tk.Label(parent, text=text, bg=COULEURS["surface"],
                    fg=fg, font=(font, size, weight))

def btn(parent, text, command, color="green", padx=16, pady=6):
    bg_map = {"green": COULEURS["green_bg"], "red": COULEURS["red_bg"],
               "amber": COULEURS["amber_bg"], "blue": COULEURS["blue_bg"]}
    fg_map = {"green": COULEURS["green"], "red": COULEURS["red"],
               "amber": COULEURS["amber"], "blue": COULEURS["blue"]}
    b = tk.Button(parent, text=text, command=command,
                  bg=bg_map.get(color, COULEURS["surface"]),
                  fg=fg_map.get(color, COULEURS["text"]),
                  activebackground=COULEURS["border2"],
                  relief="flat", font=("Courier", 11, "bold"),
                  padx=padx, pady=pady, cursor="hand2", bd=0)
    return b

def separator(parent):
    return tk.Frame(parent, height=1, bg=COULEURS["border"])

def card(parent, **kwargs):
    f = tk.Frame(parent, bg=COULEURS["surface"],
                 highlightbackground=COULEURS["border"],
                 highlightthickness=1, **kwargs)
    return f

# ═══════════════════════════════════════════════
# FENÊTRE PRINCIPALE
# ═══════════════════════════════════════════════
class FarmCareApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🐄 FarmCare — Gestion d'Élevage")
        self.configure(bg=COULEURS["bg"])
        self.geometry("960x680")
        self.minsize(800, 580)

        self.data = charger()
        if not self.data.get("cycles"):
            self.data = {"cycles": [], "active_id": None}

        self._build_ui()
        self._refresh_all()

    # ─── BUILD ────────────────────────────────
    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg="#0d1117", pady=12)
        header.pack(fill="x")
        tk.Label(header, text="🐄  FARMCARE", bg="#0d1117",
                 fg=COULEURS["green"], font=("Courier", 16, "bold")).pack(side="left", padx=20)
        tk.Label(header, text="GESTION D'ÉLEVAGE", bg="#0d1117",
                 fg=COULEURS["muted"], font=("Courier", 9)).pack(side="left")
        self.lbl_date = tk.Label(header, text=date.today().strftime("%d/%m/%Y"),
                                  bg="#0d1117", fg=COULEURS["muted"], font=("Courier", 10))
        self.lbl_date.pack(side="right", padx=20)

        separator(self).pack(fill="x")

        # Notebook (onglets)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=COULEURS["bg"], borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=COULEURS["surface"],
                        foreground=COULEURS["muted"],
                        font=("Courier", 11),
                        padding=[16, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", COULEURS["green_bg"])],
                  foreground=[("selected", COULEURS["green"])])

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=0, pady=0)

        # Frames des onglets
        self.tab_dashboard = tk.Frame(self.nb, bg=COULEURS["bg"])
        self.tab_cycles    = tk.Frame(self.nb, bg=COULEURS["bg"])
        self.tab_soins     = tk.Frame(self.nb, bg=COULEURS["bg"])
        self.tab_alertes   = tk.Frame(self.nb, bg=COULEURS["bg"])

        self.nb.add(self.tab_dashboard, text="📊 Dashboard")
        self.nb.add(self.tab_cycles,    text="🔄 Cycles")
        self.nb.add(self.tab_soins,     text="💉 Soins")
        self.nb.add(self.tab_alertes,   text="🔔 Alertes")

    # ─── REFRESH ──────────────────────────────
    def _refresh_all(self):
        for tab in [self.tab_dashboard, self.tab_cycles, self.tab_soins, self.tab_alertes]:
            for w in tab.winfo_children():
                w.destroy()
        self._build_dashboard()
        self._build_cycles()
        self._build_soins()
        self._build_alertes()
        sauvegarder(self.data)

    def _active_cycle(self):
        aid = self.data.get("active_id")
        for c in self.data["cycles"]:
            if c["id"] == aid:
                return c
        return self.data["cycles"][0] if self.data["cycles"] else None

    # ═══════════════════════════════════════════
    # DASHBOARD
    # ═══════════════════════════════════════════
    def _build_dashboard(self):
        frame = self.tab_dashboard
        if not self.data["cycles"]:
            f = tk.Frame(frame, bg=COULEURS["bg"])
            f.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(f, text="🐄", bg=COULEURS["bg"], font=("Courier", 48)).pack()
            tk.Label(f, text="Aucun cycle d'élevage.\nCréez-en un dans l'onglet Cycles.",
                     bg=COULEURS["bg"], fg=COULEURS["muted"],
                     font=("Courier", 12), justify="center").pack(pady=8)
            btn(f, "+ Créer un cycle", lambda: self.nb.select(1)).pack()
            return

        c = self._active_cycle()
        if not c:
            return

        # Sélecteur de cycle
        sel_frame = tk.Frame(frame, bg=COULEURS["bg"], pady=12)
        sel_frame.pack(fill="x", padx=20)
        tk.Label(sel_frame, text="Cycle actif :", bg=COULEURS["bg"],
                 fg=COULEURS["muted"], font=("Courier", 10)).pack(side="left")
        for cy in self.data["cycles"]:
            is_a = cy["id"] == self.data.get("active_id")
            b = tk.Button(sel_frame,
                          text=f"{cy['emoji']} {cy['type_animal']} #{cy['id'][-4:]}",
                          bg=COULEURS["green_bg"] if is_a else COULEURS["surface"],
                          fg=COULEURS["green"] if is_a else COULEURS["muted"],
                          relief="flat", font=("Courier", 10),
                          padx=10, pady=4, cursor="hand2",
                          command=lambda cid=cy["id"]: self._set_active(cid))
            b.pack(side="left", padx=4)

        # Info banner
        banner = tk.Frame(frame, bg=COULEURS["surface"],
                          highlightbackground=COULEURS["border"], highlightthickness=1)
        banner.pack(fill="x", padx=20, pady=4)
        tk.Label(banner, text=c["emoji"], bg=COULEURS["surface"],
                 font=("Courier", 28)).pack(side="left", padx=16, pady=10)
        info = tk.Frame(banner, bg=COULEURS["surface"])
        info.pack(side="left", pady=10)
        tk.Label(info, text=c["type_animal"], bg=COULEURS["surface"],
                 fg=COULEURS["text"], font=("Courier", 13, "bold")).pack(anchor="w")
        debut_fmt = datetime.strptime(c["date_debut"], "%Y-%m-%d").strftime("%d/%m/%Y")
        tk.Label(info, text=f"Début : {debut_fmt}  ·  Durée : {c['duree_jours']} jours",
                 bg=COULEURS["surface"], fg=COULEURS["muted"], font=("Courier", 10)).pack(anchor="w")

        debut = datetime.strptime(c["date_debut"], "%Y-%m-%d").date()
        fin = date.fromordinal(debut.toordinal() + c["duree_jours"])
        jr = (fin - date.today()).days
        jr_color = COULEURS["red"] if jr < 5 else COULEURS["amber"] if jr < 15 else COULEURS["green"]
        jr_text = f"⏳ {jr} jours restants" if jr > 0 else "🏁 Cycle terminé"
        tk.Label(banner, text=jr_text, bg=COULEURS["surface"],
                 fg=jr_color, font=("Courier", 11, "bold")).pack(side="right", padx=16)

        # Cards
        restants = c["nombre_initial"] + c["naissances"] - c["deces"]
        taux_mort = round((c["deces"] / c["nombre_initial"] * 100) if c["nombre_initial"] else 0, 1)
        taux_nat  = round((c["naissances"] / c["nombre_initial"] * 100) if c["nombre_initial"] else 0, 1)

        cards_data = [
            ("Nombre initial",  c["nombre_initial"],   "",  "blue",   "🔵"),
            ("Restants",        restants,               "",  "green",  "🟢"),
            ("Décès",           c["deces"],             f"({taux_mort}%)", "red", "🔴"),
            ("Naissances",      c["naissances"],        f"({taux_nat}%)",  "amber","🟡"),
            ("Vaccins",         len(c.get("vaccins", [])),       "",  "purple","💜"),
            ("Traitements",     len(c.get("traitements", [])),   "",  "blue",  "🔵"),
        ]

        cards_frame = tk.Frame(frame, bg=COULEURS["bg"])
        cards_frame.pack(fill="x", padx=20, pady=12)

        bg_map = {"blue": COULEURS["blue_bg"], "green": COULEURS["green_bg"],
                  "red": COULEURS["red_bg"], "amber": COULEURS["amber_bg"],
                  "purple": "#1e0f2e"}
        fg_map = {"blue": COULEURS["blue"], "green": COULEURS["green"],
                  "red": COULEURS["red"], "amber": COULEURS["amber"],
                  "purple": COULEURS["purple"]}

        for i, (lbl_txt, val, sub, color, dot) in enumerate(cards_data):
            cf = tk.Frame(cards_frame, bg=bg_map[color],
                          highlightbackground=fg_map[color],
                          highlightthickness=1, padx=16, pady=12)
            cf.grid(row=i//3, column=i%3, padx=6, pady=6, sticky="nsew")
            cards_frame.columnconfigure(i%3, weight=1)
            tk.Label(cf, text=lbl_txt.upper(), bg=bg_map[color],
                     fg=fg_map[color], font=("Courier", 9)).pack(anchor="w")
            tk.Label(cf, text=str(val), bg=bg_map[color],
                     fg=fg_map[color], font=("Courier", 28, "bold")).pack(anchor="w")
            if sub:
                tk.Label(cf, text=sub, bg=bg_map[color],
                         fg=COULEURS["muted"], font=("Courier", 10)).pack(anchor="w")

        # Barre de progression
        prog_frame = card(frame, pady=14)
        prog_frame.pack(fill="x", padx=20, pady=4)
        header_p = tk.Frame(prog_frame, bg=COULEURS["surface"])
        header_p.pack(fill="x", padx=16)
        tk.Label(header_p, text="ÉTAT DU TROUPEAU", bg=COULEURS["surface"],
                 fg=COULEURS["muted"], font=("Courier", 9)).pack(side="left")
        total = c["nombre_initial"] + c["naissances"]
        tk.Label(header_p, text=f"{restants} / {total}", bg=COULEURS["surface"],
                 fg=COULEURS["green"], font=("Courier", 10)).pack(side="right")
        pct = (restants / total * 100) if total else 0
        canvas = tk.Canvas(prog_frame, height=10, bg=COULEURS["border"],
                           highlightthickness=0)
        canvas.pack(fill="x", padx=16, pady=6)
        canvas.update_idletasks()
        w = canvas.winfo_width() or 900
        canvas.create_rectangle(0, 0, int(w * pct / 100), 10,
                                 fill=COULEURS["green"], outline="")

    # ═══════════════════════════════════════════
    # CYCLES
    # ═══════════════════════════════════════════
    def _build_cycles(self):
        frame = self.tab_cycles
        pad = {"padx": 20, "pady": 6}

        # Titre + bouton
        top = tk.Frame(frame, bg=COULEURS["bg"])
        top.pack(fill="x", **pad, pady=12)
        tk.Label(top, text="🔄 Cycles d'élevage", bg=COULEURS["bg"],
                 fg=COULEURS["text"], font=("Courier", 14, "bold")).pack(side="left")
        btn(top, "+ Nouveau cycle", self._nouveau_cycle).pack(side="right")

        c = self._active_cycle()

        # Actions rapides
        if c:
            actions = card(frame)
            actions.pack(fill="x", **pad)
            tk.Label(actions, text=f"Actions — {c['emoji']} {c['type_animal']}",
                     bg=COULEURS["surface"], fg=COULEURS["muted"],
                     font=("Courier", 10)).pack(anchor="w", padx=14, pady=(10, 6))
            ab = tk.Frame(actions, bg=COULEURS["surface"])
            ab.pack(padx=14, pady=(0, 10), anchor="w")
            btn(ab, "💀 Ajouter décès",     lambda: self._update_stat("deces"),     "red").pack(side="left", padx=(0, 8))
            btn(ab, "🐣 Ajouter naissances", lambda: self._update_stat("naissances"), "amber").pack(side="left")

            # Compteurs
            cnt_frame = tk.Frame(actions, bg=COULEURS["surface"])
            cnt_frame.pack(fill="x", padx=14, pady=(0, 14))
            for txt, val, col in [("DÉCÈS", c["deces"], COULEURS["red"]),
                                   ("NAISSANCES", c["naissances"], COULEURS["amber"])]:
                cf = tk.Frame(cnt_frame, bg=COULEURS["bg"],
                              highlightbackground=COULEURS["border"], highlightthickness=1)
                cf.pack(side="left", padx=(0, 10), ipadx=20, ipady=8)
                tk.Label(cf, text=txt, bg=COULEURS["bg"], fg=col,
                         font=("Courier", 9)).pack()
                tk.Label(cf, text=str(val), bg=COULEURS["bg"], fg=col,
                         font=("Courier", 24, "bold")).pack()

        # Liste cycles
        list_frame = tk.Frame(frame, bg=COULEURS["bg"])
        list_frame.pack(fill="both", expand=True, padx=20, pady=8)

        canvas = tk.Canvas(list_frame, bg=COULEURS["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COULEURS["bg"])
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for cy in self.data["cycles"]:
            is_a = cy["id"] == self.data.get("active_id")
            restants = cy["nombre_initial"] + cy["naissances"] - cy["deces"]
            row = tk.Frame(scroll_frame,
                           bg=COULEURS["green_bg"] if is_a else COULEURS["surface"],
                           highlightbackground=COULEURS["green"] if is_a else COULEURS["border"],
                           highlightthickness=1)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=cy["emoji"], bg=row["bg"],
                     font=("Courier", 22)).pack(side="left", padx=12, pady=10)
            info = tk.Frame(row, bg=row["bg"])
            info.pack(side="left", pady=8, fill="x", expand=True)
            tk.Label(info, text=cy["type_animal"], bg=row["bg"],
                     fg=COULEURS["text"], font=("Courier", 12, "bold")).pack(anchor="w")
            debut_f = datetime.strptime(cy["date_debut"], "%Y-%m-%d").strftime("%d/%m/%Y")
            tk.Label(info, text=f"{cy['nombre_initial']} initial  ·  {restants} restants  ·  {debut_f}",
                     bg=row["bg"], fg=COULEURS["muted"], font=("Courier", 10)).pack(anchor="w")
            btns = tk.Frame(row, bg=row["bg"])
            btns.pack(side="right", padx=10)
            if not is_a:
                btn(btns, "Activer", lambda cid=cy["id"]: self._set_active(cid), "blue"
                    ).pack(side="left", padx=4)
            else:
                tk.Label(btns, text="● ACTIF", bg=row["bg"],
                         fg=COULEURS["green"], font=("Courier", 10, "bold")).pack(side="left", padx=8)
            btn(btns, "✕", lambda cid=cy["id"]: self._supprimer_cycle(cid), "red"
                ).pack(side="left")

    # ═══════════════════════════════════════════
    # SOINS (Vaccins + Traitements)
    # ═══════════════════════════════════════════
    def _build_soins(self):
        frame = self.tab_soins
        c = self._active_cycle()
        if not c:
            tk.Label(frame, text="Sélectionnez un cycle actif d'abord.",
                     bg=COULEURS["bg"], fg=COULEURS["muted"],
                     font=("Courier", 12)).place(relx=0.5, rely=0.5, anchor="center")
            return

        # Sous-onglets
        self._soins_mode = getattr(self, "_soins_mode", "vaccins")
        sub_frame = tk.Frame(frame, bg=COULEURS["surface"])
        sub_frame.pack(fill="x")
        for mode, label_txt in [("vaccins", "💉 Vaccins"), ("traitements", "💊 Traitements")]:
            is_sel = self._soins_mode == mode
            b = tk.Button(sub_frame, text=label_txt,
                          bg=COULEURS["surface"] if not is_sel else COULEURS["green_bg"],
                          fg=COULEURS["green"] if is_sel else COULEURS["muted"],
                          relief="flat", font=("Courier", 12, "bold" if is_sel else "normal"),
                          padx=20, pady=10, cursor="hand2",
                          command=lambda m=mode: self._switch_soins(m))
            b.pack(side="left")
        separator(frame).pack(fill="x")

        # En-tête
        top = tk.Frame(frame, bg=COULEURS["bg"])
        top.pack(fill="x", padx=20, pady=10)
        liste = c.get(self._soins_mode, [])
        tk.Label(top, text=f"{len(liste)} enregistré(s) — {c['emoji']} {c['type_animal']}",
                 bg=COULEURS["bg"], fg=COULEURS["muted"], font=("Courier", 10)).pack(side="left")
        btn(top, "+ Ajouter", lambda: self._nouveau_soin(self._soins_mode)).pack(side="right")

        # Liste
        list_frame = tk.Frame(frame, bg=COULEURS["bg"])
        list_frame.pack(fill="both", expand=True, padx=20)

        if not liste:
            tk.Label(list_frame, text=f"Aucun {'vaccin' if self._soins_mode=='vaccins' else 'traitement'} enregistré.",
                     bg=COULEURS["bg"], fg=COULEURS["muted"],
                     font=("Courier", 11)).pack(expand=True)
            return

        today = date.today()
        for item in liste:
            d = datetime.strptime(item["date"], "%Y-%m-%d").date()
            diff = (d - today).days
            status_color = COULEURS["muted"] if diff < 0 else COULEURS["red"] if diff == 0 \
                           else COULEURS["amber"] if diff <= 2 else COULEURS["green"]
            status_text = "Passé" if diff < 0 else "Aujourd'hui !" if diff == 0 \
                          else f"Dans {diff}j"

            row = tk.Frame(list_frame, bg=COULEURS["surface"],
                           highlightbackground=COULEURS["border"], highlightthickness=1)
            row.pack(fill="x", pady=3)
            ico = "💉" if self._soins_mode == "vaccins" else "💊"
            tk.Label(row, text=ico, bg=COULEURS["surface"],
                     font=("Courier", 18)).pack(side="left", padx=12, pady=8)
            info = tk.Frame(row, bg=COULEURS["surface"])
            info.pack(side="left", pady=6, fill="x", expand=True)
            tk.Label(info, text=item["nom"], bg=COULEURS["surface"],
                     fg=COULEURS["text"], font=("Courier", 11, "bold")).pack(anchor="w")
            sous = item.get("sous_type", "") or item.get("notes", "")
            if sous:
                tk.Label(info, text=sous, bg=COULEURS["surface"],
                         fg=COULEURS["muted"], font=("Courier", 9)).pack(anchor="w")
            right = tk.Frame(row, bg=COULEURS["surface"])
            right.pack(side="right", padx=12)
            tk.Label(right, text=d.strftime("%d/%m/%Y"), bg=COULEURS["surface"],
                     fg=COULEURS["muted"], font=("Courier", 10)).pack(anchor="e")
            tk.Label(right, text=status_text, bg=COULEURS["surface"],
                     fg=status_color, font=("Courier", 10, "bold")).pack(anchor="e")
            btn(right, "✕",
                lambda iid=item["id"]: self._supprimer_soin(iid, self._soins_mode),
                "red").pack(anchor="e", pady=2)

    # ═══════════════════════════════════════════
    # ALERTES
    # ═══════════════════════════════════════════
    def _build_alertes(self):
        frame = self.tab_alertes
        top = tk.Frame(frame, bg=COULEURS["bg"])
        top.pack(fill="x", padx=20, pady=12)
        tk.Label(top, text="🔔 Alertes", bg=COULEURS["bg"],
                 fg=COULEURS["text"], font=("Courier", 14, "bold")).pack(side="left")

        alertes = get_alertes(self.data["cycles"])
        nb_danger = sum(1 for a in alertes if a[0] == "DANGER")

        badge_color = COULEURS["red_bg"] if nb_danger else COULEURS["surface"]
        tk.Label(top, text=f"  {nb_danger} urgente(s)",
                 bg=badge_color, fg=COULEURS["red"],
                 font=("Courier", 10)).pack(side="right")

        if not alertes:
            tk.Label(frame, text="✅\n\nTout est en ordre.\nAucune alerte active.",
                     bg=COULEURS["bg"], fg=COULEURS["muted"],
                     font=("Courier", 13), justify="center").place(relx=0.5, rely=0.5, anchor="center")
            return

        for niveau, texte in alertes:
            bg = COULEURS["red_bg"] if niveau == "DANGER" else COULEURS["amber_bg"]
            fg = COULEURS["red"] if niveau == "DANGER" else COULEURS["amber"]
            row = tk.Frame(frame, bg=bg,
                           highlightbackground=fg, highlightthickness=1)
            row.pack(fill="x", padx=20, pady=3)
            dot = tk.Frame(row, bg=fg, width=8, height=8)
            dot.pack(side="left", padx=12, pady=12)
            tk.Label(row, text=texte, bg=bg, fg=fg,
                     font=("Courier", 11), anchor="w", justify="left").pack(side="left", pady=8)
            tk.Label(row, text=niveau, bg=bg, fg=fg,
                     font=("Courier", 9, "bold")).pack(side="right", padx=12)

    # ═══════════════════════════════════════════
    # ACTIONS
    # ═══════════════════════════════════════════
    def _set_active(self, cid):
        self.data["active_id"] = cid
        self._refresh_all()

    def _switch_soins(self, mode):
        self._soins_mode = mode
        self._build_soins()

    def _nouveau_cycle(self):
        win = tk.Toplevel(self)
        win.title("Nouveau cycle")
        win.configure(bg=COULEURS["surface"])
        win.geometry("380x300")
        win.grab_set()

        tk.Label(win, text="+ Nouveau cycle d'élevage", bg=COULEURS["surface"],
                 fg=COULEURS["green"], font=("Courier", 13, "bold")).pack(pady=(16, 12))

        # Animal
        tk.Label(win, text="TYPE D'ANIMAL", bg=COULEURS["surface"],
                 fg=COULEURS["muted"], font=("Courier", 9)).pack(anchor="w", padx=20)
        animal_var = tk.StringVar(value="Poulet|🐔")
        combo_a = ttk.Combobox(win, textvariable=animal_var, state="readonly",
                               values=[f"{a}|{e}" for a, e in ANIMAUX],
                               font=("Courier", 11))
        combo_a.pack(fill="x", padx=20, pady=(2, 8))

        # Nombre
        tk.Label(win, text="NOMBRE INITIAL", bg=COULEURS["surface"],
                 fg=COULEURS["muted"], font=("Courier", 9)).pack(anchor="w", padx=20)
        nb_var = tk.StringVar()
        tk.Entry(win, textvariable=nb_var, bg=COULEURS["bg"], fg=COULEURS["text"],
                 font=("Courier", 12), relief="flat",
                 insertbackground=COULEURS["green"]).pack(fill="x", padx=20, pady=(2, 8))

        # Durée
        tk.Label(win, text="DURÉE (JOURS)", bg=COULEURS["surface"],
                 fg=COULEURS["muted"], font=("Courier", 9)).pack(anchor="w", padx=20)
        dur_var = tk.StringVar(value="45")
        ttk.Combobox(win, textvariable=dur_var, state="readonly",
                     values=[str(d) for d in DUREES],
                     font=("Courier", 11)).pack(fill="x", padx=20, pady=(2, 12))

        def creer():
            try:
                nb = int(nb_var.get())
                assert nb > 0
            except:
                messagebox.showerror("Erreur", "Nombre initial invalide.", parent=win)
                return
            parts = animal_var.get().split("|")
            type_a, emoji = parts[0], parts[1]
            cycle = {
                "id": str(uuid.uuid4())[:8],
                "type_animal": type_a,
                "emoji": emoji,
                "nombre_initial": nb,
                "duree_jours": int(dur_var.get()),
                "date_debut": str(date.today()),
                "deces": 0,
                "naissances": 0,
                "vaccins": [],
                "traitements": [],
            }
            self.data["cycles"].append(cycle)
            self.data["active_id"] = cycle["id"]
            self._refresh_all()
            win.destroy()

        btn(win, "✓ Créer le cycle", creer).pack(pady=4)

    def _update_stat(self, key):
        c = self._active_cycle()
        if not c:
            return
        val = simpledialog.askinteger("Mise à jour",
                                       f"Nombre de {'décès' if key=='deces' else 'naissances'} à ajouter :",
                                       parent=self, minvalue=1)
        if val:
            for cy in self.data["cycles"]:
                if cy["id"] == c["id"]:
                    cy[key] += val
            self._refresh_all()

    def _supprimer_cycle(self, cid):
        if not messagebox.askyesno("Confirmation", "Supprimer ce cycle ?"):
            return
        self.data["cycles"] = [c for c in self.data["cycles"] if c["id"] != cid]
        if self.data.get("active_id") == cid:
            self.data["active_id"] = self.data["cycles"][0]["id"] if self.data["cycles"] else None
        self._refresh_all()

    def _nouveau_soin(self, mode):
        c = self._active_cycle()
        if not c:
            return
        win = tk.Toplevel(self)
        win.title(f"Nouveau {'vaccin' if mode=='vaccins' else 'traitement'}")
        win.configure(bg=COULEURS["surface"])
        win.geometry("360x260")
        win.grab_set()

        ico = "💉" if mode == "vaccins" else "💊"
        tk.Label(win, text=f"{ico} Nouveau {'vaccin' if mode=='vaccins' else 'traitement'}",
                 bg=COULEURS["surface"], fg=COULEURS["green"],
                 font=("Courier", 13, "bold")).pack(pady=(16, 12))

        tk.Label(win, text="NOM", bg=COULEURS["surface"],
                 fg=COULEURS["muted"], font=("Courier", 9)).pack(anchor="w", padx=20)
        nom_var = tk.StringVar()
        tk.Entry(win, textvariable=nom_var, bg=COULEURS["bg"], fg=COULEURS["text"],
                 font=("Courier", 12), relief="flat",
                 insertbackground=COULEURS["green"]).pack(fill="x", padx=20, pady=(2, 8))

        tk.Label(win, text="DATE (YYYY-MM-DD)", bg=COULEURS["surface"],
                 fg=COULEURS["muted"], font=("Courier", 9)).pack(anchor="w", padx=20)
        date_var = tk.StringVar(value=str(date.today()))
        tk.Entry(win, textvariable=date_var, bg=COULEURS["bg"], fg=COULEURS["text"],
                 font=("Courier", 12), relief="flat",
                 insertbackground=COULEURS["green"]).pack(fill="x", padx=20, pady=(2, 8))

        sous_var = tk.StringVar(value="Antibiotique")
        if mode == "traitements":
            tk.Label(win, text="TYPE", bg=COULEURS["surface"],
                     fg=COULEURS["muted"], font=("Courier", 9)).pack(anchor="w", padx=20)
            ttk.Combobox(win, textvariable=sous_var, state="readonly",
                         values=["Antibiotique", "Vitamine", "Antiparasitaire", "Antifongique", "Autre"],
                         font=("Courier", 11)).pack(fill="x", padx=20, pady=(2, 8))

        def enregistrer():
            nom = nom_var.get().strip()
            dat = date_var.get().strip()
            if not nom or not dat:
                messagebox.showerror("Erreur", "Remplissez tous les champs.", parent=win)
                return
            try:
                datetime.strptime(dat, "%Y-%m-%d")
            except:
                messagebox.showerror("Erreur", "Date invalide (format: YYYY-MM-DD)", parent=win)
                return
            entry = {"id": str(uuid.uuid4())[:8], "nom": nom, "date": dat}
            if mode == "traitements":
                entry["sous_type"] = sous_var.get()
            for cy in self.data["cycles"]:
                if cy["id"] == c["id"]:
                    cy[mode].append(entry)
            self._refresh_all()
            win.destroy()

        btn(win, "✓ Enregistrer", enregistrer).pack(pady=4)

    def _supprimer_soin(self, item_id, mode):
        c = self._active_cycle()
        if not c:
            return
        for cy in self.data["cycles"]:
            if cy["id"] == c["id"]:
                cy[mode] = [i for i in cy[mode] if i["id"] != item_id]
        self._refresh_all()


# ═══════════════════════════════════════════════
# LANCEMENT
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    app = FarmCareApp()
    app.mainloop()
