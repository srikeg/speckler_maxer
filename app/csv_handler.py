# csv_handler.py
import csv
import os
from typing import List, Dict, Any


class CSVHandler:
    def __init__(self, file_path: str):
        """
        Initialisiert den CSVHandler mit dem Pfad zur Datei.
        """
        self.file_path = file_path

    def read_as_dicts(self, delimiter: str = ',') -> List[Dict[str, str]]:
        """
        Liest die CSV-Datei und gibt den Inhalt als Liste von Dictionaries zurück.
        Nutzt die erste Zeile automatisch als Spaltennamen (Keys).
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Die Datei '{self.file_path}' existiert nicht.")

        # Nutzt 'cp1252' (ANSI), um Fehler mit Umlauten (z.B. Materialstärke) zu vermeiden
        with open(self.file_path, mode='r', encoding='cp1252', newline='') as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            return [dict(row) for row in reader]

    def write_from_dicts(self, data: List[Dict[str, Any]], fieldnames: List[str] = None, delimiter: str = ',',
                         append: bool = False) -> None:
        """
        Schreibt eine Liste von Dictionaries in die CSV-Datei.
        Unterstützt das Anhängen von neuen Zeilen (append=True).
        """
        if not data and not fieldnames:
            print("Keine Daten oder Spaltenueberschriften uebergeben. Es wurde nichts geschrieben.")
            return

        if not fieldnames and data:
            fieldnames = list(data[0].keys())

        mode = 'a' if append else 'w'

        file_is_empty = not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0
        write_header = mode == 'w' or file_is_empty

        # Auch hier einheitlich 'cp1252', damit neue Einträge im gleichen Format landen
        with open(self.file_path, mode=mode, encoding='cp1252', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter)

            if write_header:
                writer.writeheader()

            writer.writerows(data)