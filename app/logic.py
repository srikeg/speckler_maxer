# logic.py
import os
from .csv_handler import CSVHandler


def get_material_parameters(
        material_name: str,
        operation_type: str,
        thickness: float,
        machine_type: str,
        file_path: str = "database.csv"
        # file_path: str = "/home/group1/speckler_maxer/app/database.csv"
) -> dict:
    """
    Sucht in der CSV nach Prozessparametern.
    Struktur: Material, Materialstärke, Maschine, Gravieren, Schneiden, Vorschub, Leistung, Liniendichte, Bearbeitbar
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Die Datenbank '{file_path}' wurde nicht gefunden.")

    handler = CSVHandler(file_path)
    try:
        # Falls du das Encoding in csv_handler.py noch nicht auf cp1252 umgestellt hast,
        # kannst du das direkt dort tun, um Umlaute-Fehler zu vermeiden.
        datenbank = handler.read_as_dicts()
    except Exception as e:
        raise IOError(f"Fehler beim Lesen der CSV-Datei: {e}")

    if not datenbank:
        raise ValueError(f"Die Datenbank '{file_path}' enthaelt keine Daten.")

    search_material = material_name.strip().lower()
    search_op = operation_type.strip().lower()
    search_machine = machine_type.strip().lower()

    for zeile in datenbank:
        # 1. Abgleich des Materialnamens
        row_material = zeile.get("Material", "").strip().lower()
        if row_material != search_material:
            continue

        # 2. Sicherheits-Pruefung
        is_bearbeitbar = zeile.get("Bearbeitbar", "").strip().lower()
        if is_bearbeitbar in ["nein", "false", "0"]:
            raise PermissionError(
                f"Sicherheits-Warnung: Das Material '{material_name}' ist in der "
                f"Datenbank als NICHT BEARBEITBAR markiert! Bitte nicht Lasern!"
            )

        # 3. Abgleich der Maschine (Spalte: 'Maschine')
        row_machine = zeile.get("Maschine", "").strip().lower()
        if row_machine != search_machine:
            continue

        # 4. Abgleich der Materialstaerke
        row_thickness_raw = zeile.get("Materialstärke", "").strip()
        try:
            row_thickness = float(row_thickness_raw.replace(',', '.'))
        except ValueError:
            continue

        if abs(row_thickness - float(thickness)) >= 0.01:
            continue

        # 5. Abgleich der Bearbeitungsart freigegeben
        if search_op == "schneiden":
            op_allowed = zeile.get("Schneiden", "").strip().lower()
        elif search_op == "gravieren":
            op_allowed = zeile.get("Gravieren", "").strip().lower()
        else:
            op_allowed = "nein"

        if op_allowed in ["nein", "false", "0", ""]:
            raise ValueError(
                f"Das Material '{material_name}' ist fuer {machine_type} und die Bearbeitungsart "
                f"'{operation_type}' bei {thickness}mm Staerke nicht freigegeben."
            )

        return {
            "Material": zeile.get("Material"),
            "Materialstaerke": f"{row_thickness} mm",
            "Maschine": zeile.get("Maschine"),
            "Vorschub": zeile.get("Vorschub", "N/A"),
            "Leistung": zeile.get("Leistung", "N/A"),
            "Liniendichte": zeile.get("Liniendichte", "N/A")
        }

    raise ValueError(
        f"Fuer das Material '{material_name}' ({machine_type}, {thickness}mm) wurden keine Eintraege in der "
        f"Datenbank gefunden."
    )