# webgui.py
import os
from flask import Flask, render_template_string, request
from .logic import get_material_parameters
from .csv_handler import CSVHandler
from .label import generate_material_qr
from .materialscanner import scan as call_material_scanner

# try:
#     from Materialscanner import scan as call_material_scanner
# except ImportError:
#     def call_material_scanner():
#         predicted_materil = 
#         return "Unbekanntes_Material"

app = Flask(__name__)


def get_unique_machines(file_path: str = "database.csv") -> list:
    """
    Liest die database.csv ein und gibt eine Liste aller einzigartigen
    Eintraege aus der Spalte 'Maschine' zurueck.
    """
    if not os.path.exists(file_path):
        print(f"WARNUNG: Datei {file_path} wurde nicht gefunden!")
        return ["CO2-Laser", "Faserlaser"]

    try:
        handler = CSVHandler(file_path)
        datenbank = handler.read_as_dicts()

        machines = {zeile.get("Maschine").strip() for zeile in datenbank if zeile.get("Maschine")}

        if machines:
            return sorted(list(machines))
    except Exception as e:
        print(f"FEHLER beim Laden der Maschinen: {e}")

    return ["CO2-Laser", "Faserlaser"]


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Makerthon Material Scanner</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = { darkMode: 'class' }
    </script>
</head>
<body class="bg-zinc-950 text-zinc-100 min-h-screen flex flex-col items-center justify-center font-sans p-4 space-y-6">

    <div class="w-full max-w-md bg-zinc-900 border border-zinc-800 rounded-2xl shadow-2xl p-6 transition-all">
        <h1 class="text-2xl font-bold tracking-tight text-center mb-6 bg-gradient-to-r from-teal-400 to-emerald-400 bg-clip-text text-transparent">
            Makerthon Material Scanner
        </h1>

        <form method="POST" class="space-y-5">

            <div class="bg-zinc-850 border border-zinc-800 rounded-xl p-4 space-y-3">
                <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-zinc-400">Smarte Materialerkennung</span>
                    {% if material %}
                        <span class="px-2.5 py-1 text-xs font-semibold bg-teal-500/10 text-teal-400 border border-teal-500/20 rounded-full animate-pulse">Bereit</span>
                    {% else %}
                        <span class="px-2.5 py-1 text-xs font-semibold bg-zinc-800 text-zinc-500 border border-zinc-700 rounded-full">Kein Scan</span>
                    {% endif %}
                </div>

                <div class="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-3 text-center">
                    {% if material %}
                        <span class="text-xl font-bold text-zinc-100 tracking-wide">{{ material }}</span>
                    {% else %}
                        <span class="text-sm italic text-zinc-500">Bitte Materialerkennung starten...</span>
                    {% endif %}
                </div>

                <button type="submit" name="action" value="scan"
                        class="w-full bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 text-zinc-200 font-medium py-2 px-4 rounded-lg text-sm flex items-center justify-center gap-2 active:scale-[0.99] transition-all">
                    Material scannen
                </button>
            </div>

{% if image_url %}
    <div class="w-full flex justify-center my-4">
        <img src="{{ image_url }}" alt="Letztes Scan-Bild" class="rounded-lg border border-zinc-700 max-w-full h-auto shadow-lg">
    </div>
{% endif %}

            <div>
                <label for="material_input" class="block text-sm font-medium text-zinc-400 mb-1.5">Materialbezeichnung (Eingabe oder Scan-Ergebnis)</label>
                <input type="text" id="material_input" name="material_input" value="{{ material }}" placeholder="z.B. Acryl, Sperrholz"
                       class="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-2.5 text-zinc-100 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all">
            </div>

            <div>
                <label for="thickness" class="block text-sm font-medium text-zinc-400 mb-1.5">Materialstärke (in mm)</label>
                <input type="number" step="0.1" id="thickness" name="thickness" value="{{ thickness_value }}"
                       class="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-2.5 text-zinc-100 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all">
            </div>

            <div>
                <label for="machine" class="block text-sm font-medium text-zinc-400 mb-1.5">Maschine / System</label>
                <select id="machine" name="machine" 
                        class="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-2.5 text-zinc-100 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all">
                    {% for mach in available_machines %}
                        <option value="{{ mach }}" {% if machine_value == mach %}selected{% endif %}>{{ mach }}</option>
                    {% endfor %}
                </select>
            </div>

            <div>
                <span class="block text-sm font-medium text-zinc-400 mb-2">Art der Bearbeitung</span>
                <div class="flex bg-zinc-800 p-1 rounded-xl border border-zinc-700">
                    <button type="submit" name="operation" value="schneiden" 
                            class="flex-1 text-center py-2 rounded-lg transition-all text-sm font-semibold select-none {% if operation_value == 'schneiden' %} bg-teal-600 text-white shadow-md {% else %} text-zinc-400 hover:text-zinc-200 {% endif %}">
                        Schneiden
                    </button>
                    <button type="submit" name="operation" value="gravieren" 
                            class="flex-1 text-center py-2 rounded-lg transition-all text-sm font-semibold select-none {% if operation_value == 'gravieren' %} bg-teal-600 text-white shadow-md {% else %} text-zinc-400 hover:text-zinc-200 {% endif %}">
                        Gravieren
                    </button>
                </div>
                <input type="hidden" name="current_operation" value="{{ operation_value }}">
            </div>

            <button type="submit" name="action" value="get_params"
                    class="w-full bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-zinc-950 font-bold py-3 px-4 rounded-xl shadow-lg shadow-teal-500/10 hover:shadow-teal-500/20 active:scale-[0.98] transition-all mt-2">
                Parameter abrufen
            </button>
        </form>

        {% if result %}
            <div class="mt-6 pt-6 border-t border-zinc-800">
                <h3 class="text-sm font-semibold text-emerald-400 uppercase tracking-wider mb-3">Gefundene Parameter:</h3>
                <div class="bg-zinc-850 border border-zinc-800 rounded-xl p-4 space-y-2 text-sm">
                    {% for key, value in result.items() %}
                        <div class="flex justify-between py-1 border-b border-zinc-800/50 last:border-0">
                            <span class="text-zinc-400 font-medium">{{ key }}</span>
                            <span class="text-zinc-200 font-mono font-semibold">{{ value }}</span>
                        </div>
                    {% endfor %}
                </div>
            </div>
        {% endif %}

        {% if error %}
            <div class="mt-6 pt-6 border-t border-zinc-800">
                {% if is_security_alert %}
                    <div class="bg-red-950 border-2 border-red-600 text-red-200 rounded-xl p-4 text-sm font-medium shadow-lg shadow-red-900/30">
                        <div class="flex items-center gap-2 text-red-500 font-bold text-base mb-1 uppercase tracking-wide">Warnung: Lebensgefahr / Maschinenschaden</div>
                        {{ error }}
                    </div>
                {% else %}
                    <div class="bg-amber-950/40 border border-amber-900/50 text-amber-400 rounded-xl p-4 text-sm font-medium">Hinweis: {{ error }}</div>
                {% endif %}
            </div>
        {% endif %}

        {% if success_msg %}
            <div class="mt-6 pt-6 border-t border-zinc-800">
                <div class="bg-emerald-950/40 border border-emerald-900/50 text-emerald-400 rounded-xl p-4 text-sm font-medium">Erfolg: {{ success_msg }}</div>
            </div>
        {% endif %}
    </div>

    {% if show_create_form %}
    <div class="w-full max-w-md bg-zinc-900 border border-yellow-600/30 rounded-2xl shadow-2xl p-6 transition-all animate-fade-in">
        <h2 class="text-xl font-bold tracking-tight text-zinc-100 mb-2 flex items-center gap-2">
            Eintrag hinzufügen
        </h2>
        <p class="text-xs text-zinc-400 mb-4">Das Material <span class="text-yellow-400 font-mono font-bold">{{ material }}</span> mit <span class="text-yellow-400 font-mono font-bold">{{ thickness_value }}mm</span> fehlt für das System <span class="text-yellow-400 font-mono font-bold">{{ machine_value }}</span>. Lege es jetzt an:</p>

        <form method="POST" class="space-y-4 text-sm">
            <input type="hidden" name="action" value="save_new_material">
            <input type="hidden" name="new_material_name" value="{{ material }}">
            <input type="hidden" name="new_thickness" value="{{ thickness_value }}">
            <input type="hidden" name="new_machine" value="{{ machine_value }}">

            <div class="grid grid-cols-2 gap-3">
                <div>
                    <label class="block text-xs text-zinc-400 mb-1">Schneiden erlauben?</label>
                    <select name="new_schneiden" class="w-full bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-100 focus:outline-none focus:ring-1 focus:ring-teal-500">
                        <option value="Ja">Ja</option>
                        <option value="Nein">Nein</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs text-zinc-400 mb-1">Gravieren erlauben?</label>
                    <select name="new_gravieren" class="w-full bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-100 focus:outline-none focus:ring-1 focus:ring-teal-500">
                        <option value="Ja">Ja</option>
                        <option value="Nein">Nein</option>
                    </select>
                </div>
            </div>

            <div class="grid grid-cols-3 gap-2">
                <div>
                    <label class="block text-xs text-zinc-400 mb-1">Vorschub</label>
                    <input type="text" name="new_vorschub" placeholder="z.B. 400" required class="w-full bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-100 focus:outline-none focus:ring-1 focus:ring-teal-500">
                </div>
                <div>
                    <label class="block text-xs text-zinc-400 mb-1">Leistung (%)</label>
                    <input type="text" name="new_leistung" placeholder="z.B. 80" required class="w-full bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-100 focus:outline-none focus:ring-1 focus:ring-teal-500">
                </div>
                <div>
                    <label class="block text-xs text-zinc-400 mb-1">Liniendichte</label>
                    <input type="text" name="new_liniendichte" placeholder="z.B. 0.1" value="0.1" required class="w-full bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-100 focus:outline-none focus:ring-1 focus:ring-teal-500">
                </div>
            </div>

            <div>
                <label class="block text-xs text-zinc-400 mb-1">Generell Bearbeitbar?</label>
                <select name="new_bearbeitbar" class="w-full bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-100 font-semibold focus:outline-none focus:ring-1 focus:ring-teal-500">
                    <option value="Ja" class="text-emerald-400">Ja (Sicher zum Lasern)</option>
                    <option value="Nein" class="text-red-400">Nein (Gefahrenstoff / Blacklist)</option>
                </select>
            </div>

            <button type="submit" class="w-full bg-yellow-600 hover:bg-yellow-500 text-zinc-950 font-bold py-2 px-4 rounded-xl shadow-lg transition-all active:scale-[0.99]">
                In Datenbank speichern
            </button>
        </form>
    </div>
    {% endif %}

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    success_msg = None
    show_create_form = False

    available_machines = get_unique_machines("database.csv")

    material = ""
    operation = "schneiden"
    thickness_value = "1.0"
    machine = available_machines[0] if available_machines else "CO2-Laser"

    if request.method == "POST":
        action = request.form.get("action")
        thickness_raw = request.form.get("thickness", "").strip()
        thickness_value = thickness_raw if thickness_raw else "1.0"
        machine = request.form.get("machine", machine)

        material = request.form.get("material_input", "").strip()

        if "operation" in request.form:
            operation = request.form.get("operation")
        else:
            operation = request.form.get("current_operation", "schneiden")

        if action == "scan":
            try:
                material ,  confidence, image_path = call_material_scanner()
                if not material:
                    error = "Der Scanner hat kein Material zurueckgegeben."
            except Exception as e:
                error = f"Fehler bei der Materialerkennung: {e}"
                material = ""
                image_path = None

        elif action == "save_new_material":
            mat_name = request.form.get("new_material_name")
            thick_val = request.form.get("new_thickness")
            mach_val = request.form.get("new_machine")

            neuer_datensatz = [{
                "Material": mat_name,
                "Materialstärke": thick_val,
                "Maschine": mach_val,
                "Gravieren": request.form.get("new_gravieren"),
                "Schneiden": request.form.get("new_schneiden"),
                "Vorschub": request.form.get("new_vorschub"),
                "Leistung": request.form.get("new_leistung"),
                "Liniendichte": request.form.get("new_liniendichte"),
                "Bearbeitbar": request.form.get("new_bearbeitbar")
            }]

            try:
                handler = CSVHandler("database.csv")
                handler.write_from_dicts(neuer_datensatz, append=True)

                try:
                    thickness_float = float(thick_val.replace(',', '.'))
                    generate_material_qr(material_name=mat_name, thickness=thickness_float)
                    qr_msg = " und QR-Code-Label wurde erstellt"
                except Exception:
                    qr_msg = " (QR-Code Erstellung fehlgeschlagen)"

                success_msg = f"Material '{mat_name}' fuer {mach_val} ({thick_val}mm) erfolgreich hinzugefuegt{qr_msg}!"
                material = mat_name
                thickness_value = thick_val
                machine = mach_val
                available_machines = get_unique_machines("database.csv")
            except Exception as e:
                error = f"Fehler beim Speichern in der CSV: {e}"

        else:
            if not thickness_raw:
                thickness = 1.0
            else:
                try:
                    thickness = float(thickness_raw.replace(',', '.'))
                except ValueError:
                    thickness = 1.0

            if material:
                try:
                    result = get_material_parameters(
                        material_name=material,
                        operation_type=operation,
                        thickness=thickness,
                        machine_type=machine,
                        file_path="database.csv"
                    )
                    app.config['SECURITY_ALERT'] = False
                except PermissionError as e:
                    error = str(e)
                    app.config['SECURITY_ALERT'] = True
                except ValueError as e:
                    error = str(e)
                    app.config['SECURITY_ALERT'] = False
                    if "keine Eintraege" in error or "nicht fuer die Bearbeitungsart" in error or "keine Einträge" in error:
                        show_create_form = True
                except Exception as e:
                    error = str(e)
                    app.config['SECURITY_ALERT'] = False
            elif action == "get_params":
                error = "Bitte gib ein Material ein oder nutze die Materialerkennung."
                app.config['SECURITY_ALERT'] = False

    is_security_alert = app.config.get('SECURITY_ALERT', False)
    return render_template_string(
        HTML_TEMPLATE,
        result=result,
        error=error,
        success_msg=success_msg,
        material=material,
        operation_value=operation,
        thickness_value=thickness_value,
        machine_value=machine,
        available_machines=available_machines,
        is_security_alert=is_security_alert,
        show_create_form=show_create_form
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)