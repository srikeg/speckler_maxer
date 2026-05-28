import os
import qrcode


def generate_material_qr(material_name: str, thickness: float, output_dir: str = "labels") -> str:
    """
    Generiert einen QR-Code, der den Materialnamen und die Staerke speichert.
    Das Bild wird als PNG-Datei im angegebenen Ordner gespeichert.

    :param material_name: Der Name des Materials (z.B. Acryl, Sperrholz)
    :param thickness: Die Materialstaerke in mm
    :param output_dir: Ordner, in dem die QR-Code-Bilder abgelegt werden
    :return: Pfad zur generierten Bilddatei
    """
    # Erstelle den Zielordner, falls er noch nicht existiert
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Bereinige die Eingaben für konsistente Daten
    clean_material = material_name.strip()
    clean_thickness = str(thickness).replace(',', '.')

    # Strukturierter Text, den der Scanner ausliest
    # Format: Material: [Typ], Staerke: [Wert]mm
    qr_data = f"Material: {clean_material}, Staerke: {clean_thickness}mm"

    # QR-Code Konfiguration
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Daten hinzufuegen und QR-Code generieren
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Bild erstellen (Schwarz auf Weiss)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Dateiname generieren (z.B. "Acryl_3.0mm.png")
    filename = f"{clean_material.replace(' ', '_')}_{clean_thickness}mm.png"
    file_path = os.path.join(output_dir, filename)

    # Bild speichern
    qr_image.save(file_path)

    return file_path


# Testbereich: Kann direkt ausgefuehrt werden, um die Funktion zu pruefen
if __name__ == "__main__":
    print("Teste QR-Code Generierung...")
    try:
        gespeicherter_pfad = generate_material_qr("MDF Holz", 4.5)
        print(f"Erfolg: QR-Code wurde unter '{gespeicherter_pfad}' gespeichert.")
    except Exception as e:
        print(f"Fehler bei der Generierung: {e}")