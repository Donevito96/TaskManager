# Standardbibliotheken importieren
import os               # Für Betriebssystem-Funktionen, z. B. Prozesse beenden oder Dateien prüfen
import signal           # Für Signale wie SIGTERM zum Beenden von Prozessen
import subprocess       # Zum Ausführen externer Linux-Befehle wie lsusb, lspci, systemctl
import sys              # Für Plattform-Prüfungen, z. B. ob Linux genutzt wird
import time             # Für Zeitmessung und Uptime-Berechnungen
import tkinter as tk    # Hauptmodul für die GUI
from tkinter import ttk, messagebox  # ttk für moderne Widgets, messagebox für Dialogfenster

# Prüfen, ob psutil installiert ist
try:
    import psutil  # Bibliothek zum Auslesen von Systeminformationen wie CPU, RAM, Prozesse, Netzwerk
except ImportError:
    raise SystemExit(
        "psutil ist nicht installiert. Installiere es mit: pip install psutil"
    )


class SystemManagerApp(tk.Tk):
    """
    Einfacher Linux Task Manager / Geräte-Manager Prototyp.

    Funktionen:
    - Live-Übersicht über CPU, RAM, Festplatte und Netzwerk
    - Prozessliste mit Möglichkeit, Prozesse zu beenden
    - Dienste-Ansicht über systemctl
    - Hardware-Ansicht über lsusb, lspci und lsblk

    Hinweise:
    - Einige Funktionen sind Linux-spezifisch.
    - Für das Stoppen mancher Prozesse oder Dienste können Root-Rechte nötig sein.
    """

    def __init__(self):
        # Konstruktor der Hauptklasse aufrufen
        super().__init__()

        # Fenstertitel setzen
        self.title("Linux System Manager Prototype")

        # Standardgröße des Fensters festlegen
        self.geometry("1200x760")

        # Minimale Fenstergröße festlegen
        self.minsize(1000, 680)

        # Erste Netzwerkstatistik speichern, um später Upload-/Downloadrate berechnen zu können
        self.last_net = psutil.net_io_counters()

        # Zeitpunkt der letzten Netzwerkmessung speichern
        self.last_net_time = time.time()

        # Oberfläche aufbauen
        self._build_ui()

        # Daten beim Start direkt laden
        self.refresh_overview()
        self.refresh_processes()
        self.refresh_services()
        self.refresh_devices()

    def _build_ui(self):
        # Ein Tab-Container (Notebook) für die verschiedenen Bereiche
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabs erstellen
        self.overview_tab = ttk.Frame(notebook)
        self.process_tab = ttk.Frame(notebook)
        self.services_tab = ttk.Frame(notebook)
        self.devices_tab = ttk.Frame(notebook)

        # Tabs zum Notebook hinzufügen
        notebook.add(self.overview_tab, text="Übersicht")
        notebook.add(self.process_tab, text="Prozesse")
        notebook.add(self.services_tab, text="Dienste")
        notebook.add(self.devices_tab, text="Geräte")

        # Inhalt der einzelnen Tabs aufbauen
        self._build_overview_tab()
        self._build_process_tab()
        self._build_services_tab()
        self._build_devices_tab()

    # -------------------------
    # Übersicht
    # -------------------------
    def _build_overview_tab(self):
        # Hauptcontainer für den Übersichts-Tab
        top = ttk.Frame(self.overview_tab, padding=12)
        top.pack(fill="both", expand=True)

        # Bereich für die kleinen Info-Karten
        cards = ttk.Frame(top)
        cards.pack(fill="x")

        # Textvariablen für Live-Anzeigen
        self.cpu_var = tk.StringVar(value="CPU: --")
        self.ram_var = tk.StringVar(value="RAM: --")
        self.disk_var = tk.StringVar(value="Disk: --")
        self.net_var = tk.StringVar(value="Netzwerk: --")
        self.uptime_var = tk.StringVar(value="Uptime: --")

        # Für jede Info eine kleine Karte erzeugen
        for i, var in enumerate(
            [self.cpu_var, self.ram_var, self.disk_var, self.net_var, self.uptime_var]
        ):
            frame = ttk.LabelFrame(cards, text=f"Info {i + 1}", padding=10)
            frame.grid(row=0, column=i, padx=6, pady=6, sticky="nsew")

            # Wert der Karte anzeigen
            ttk.Label(frame, textvariable=var, font=("Arial", 11, "bold")).pack()

            # Jede Karte soll sich gleichmäßig verteilen
            cards.columnconfigure(i, weight=1)

        # Trennlinie zwischen Karten und Details
        ttk.Separator(top).pack(fill="x", pady=12)

        # Bereich für detaillierte Systeminformationen
        details = ttk.LabelFrame(top, text="Systemdetails", padding=12)
        details.pack(fill="both", expand=True)

        # Textfeld für Hostname, Kernel, Interfaces usw.
        self.system_text = tk.Text(details, wrap="word", height=18)
        self.system_text.pack(fill="both", expand=True)

    def refresh_overview(self):
        # CPU-Auslastung in Prozent ermitteln
        cpu_percent = psutil.cpu_percent(interval=0.2)

        # Arbeitsspeicher-Infos holen
        ram = psutil.virtual_memory()

        # Speicherplatz für Root-Partition abfragen
        disk = psutil.disk_usage("/")

        # Aktuelle Zeit und Netzwerkinformationen holen
        now = time.time()
        net_now = psutil.net_io_counters()

        # Zeitdifferenz seit letzter Messung berechnen
        delta_time = max(now - self.last_net_time, 0.001)

        # Uploadrate in KB/s berechnen
        sent_rate = (net_now.bytes_sent - self.last_net.bytes_sent) / delta_time / 1024

        # Downloadrate in KB/s berechnen
        recv_rate = (net_now.bytes_recv - self.last_net.bytes_recv) / delta_time / 1024

        # Neue Messwerte speichern
        self.last_net = net_now
        self.last_net_time = now

        # Boot-Zeit holen und Uptime berechnen
        boot_time = psutil.boot_time()
        uptime_seconds = int(time.time() - boot_time)

        # Uptime in Stunden, Minuten, Sekunden zerlegen
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Werte in die GUI schreiben
        self.cpu_var.set(f"CPU: {cpu_percent:.1f}%")
        self.ram_var.set(
            f"RAM: {ram.percent:.1f}% ({self._fmt_bytes(ram.used)} / {self._fmt_bytes(ram.total)})"
        )
        self.disk_var.set(
            f"Disk: {disk.percent:.1f}% ({self._fmt_bytes(disk.used)} / {self._fmt_bytes(disk.total)})"
        )
        self.net_var.set(f"Netzwerk: ↓ {recv_rate:.1f} KB/s | ↑ {sent_rate:.1f} KB/s")
        self.uptime_var.set(f"Uptime: {hours}h {minutes}m {seconds}s")

        # Detaillierte Infos für das Textfeld vorbereiten
        info_lines = [
            f"Hostname: {self._run_command(['hostname']).strip() or 'Unbekannt'}",
            f"Kernel: {self._run_command(['uname', '-r']).strip() or 'Unbekannt'}",
            f"OS: {self._read_os_release()}",
            f"Physische CPU-Kerne: {psutil.cpu_count(logical=False)}",
            f"Logische CPU-Kerne: {psutil.cpu_count(logical=True)}",
            "",
            "Netzwerk-Interfaces:",
        ]

        # Alle Netzwerkadapter mit IP- und MAC-Adressen auflisten
        for iface, addrs in psutil.net_if_addrs().items():
            info_lines.append(f"- {iface}")
            for addr in addrs:
                if str(addr.family) in ("AddressFamily.AF_INET", "2"):
                    info_lines.append(f"    IPv4: {addr.address}")
                elif "AF_PACKET" in str(addr.family):
                    info_lines.append(f"    MAC:  {addr.address}")

        # Altes Textfeld leeren
        self.system_text.delete("1.0", tk.END)

        # Neue Infos einfügen
        self.system_text.insert(tk.END, "\n".join(info_lines))

        # Diese Methode nach 2 Sekunden erneut ausführen
        self.after(2000, self.refresh_overview)

    # -------------------------
    # Prozesse
    # -------------------------
    def _build_process_tab(self):
        # Container für den Prozess-Tab
        container = ttk.Frame(self.process_tab, padding=12)
        container.pack(fill="both", expand=True)

        # Toolbar für Buttons und Filter
        toolbar = ttk.Frame(container)
        toolbar.pack(fill="x", pady=(0, 8))

        # Button zum manuellen Aktualisieren
        ttk.Button(toolbar, text="Aktualisieren", command=self.refresh_processes).pack(side="left")

        # Button zum Beenden des ausgewählten Prozesses
        ttk.Button(toolbar, text="Prozess beenden", command=self.kill_selected_process).pack(side="left", padx=8)

        # Filterfeld für Prozessnamen
        ttk.Label(toolbar, text="Filter:").pack(side="left", padx=(16, 4))
        self.process_filter_var = tk.StringVar()

        # Bei jeder Änderung im Filter automatisch aktualisieren
        self.process_filter_var.trace_add("write", lambda *_: self.refresh_processes())

        # Eingabefeld für Filter
        ttk.Entry(toolbar, textvariable=self.process_filter_var, width=30).pack(side="left")

        # Spalten der Prozess-Tabelle
        columns = ("pid", "name", "cpu", "memory", "user", "status")
        self.process_tree = ttk.Treeview(container, columns=columns, show="headings")

        # Spalten konfigurieren
        for col, title, width in [
            ("pid", "PID", 90),
            ("name", "Name", 260),
            ("cpu", "CPU %", 90),
            ("memory", "RAM %", 90),
            ("user", "Benutzer", 180),
            ("status", "Status", 140),
        ]:
            self.process_tree.heading(col, text=title)
            self.process_tree.column(col, width=width, anchor="w")

        # Scrollbar hinzufügen
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=scrollbar.set)

        # Tabelle und Scrollbar platzieren
        self.process_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_processes(self):
        # Aktuellen Filtertext holen
        filter_text = self.process_filter_var.get().strip().lower() if hasattr(self, 'process_filter_var') else ""

        # Alte Einträge aus der Tabelle löschen
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)

        processes = []

        # Alle Prozesse durchlaufen und relevante Infos auslesen
        for proc in psutil.process_iter([
            "pid", "name", "cpu_percent", "memory_percent", "username", "status"
        ]):
            try:
                info = proc.info
                name = info.get("name") or ""

                # Wenn ein Filter gesetzt ist und nicht passt, überspringen
                if filter_text and filter_text not in name.lower():
                    continue

                processes.append(info)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Prozess existiert nicht mehr oder Zugriff verweigert
                continue

        # Prozesse nach CPU und RAM-Auslastung sortieren
        processes.sort(
            key=lambda p: (p.get("cpu_percent") or 0, p.get("memory_percent") or 0),
            reverse=True
        )

        # Prozesse in die Tabelle eintragen
        for p in processes:
            self.process_tree.insert(
                "",
                tk.END,
                values=(
                    p.get("pid", ""),
                    p.get("name", ""),
                    f"{p.get('cpu_percent', 0):.1f}",
                    f"{p.get('memory_percent', 0):.1f}",
                    p.get("username", ""),
                    p.get("status", ""),
                ),
            )

    def kill_selected_process(self):
        # Aktuell ausgewählten Prozess aus der Tabelle holen
        selected = self.process_tree.selection()

        # Falls nichts ausgewählt wurde, Hinweis anzeigen
        if not selected:
            messagebox.showinfo("Hinweis", "Bitte zuerst einen Prozess auswählen.")
            return

        # Daten des ausgewählten Eintrags auslesen
        item = self.process_tree.item(selected[0])
        pid = int(item["values"][0])
        name = item["values"][1]

        # Sicherheitsabfrage anzeigen
        if not messagebox.askyesno("Bestätigung", f"Prozess '{name}' (PID {pid}) wirklich beenden?"):
            return

        try:
            # Prozess mit SIGTERM freundlich beenden
            os.kill(pid, signal.SIGTERM)

            # Prozessliste neu laden
            self.refresh_processes()

            # Erfolgsmeldung anzeigen
            messagebox.showinfo("Erfolg", f"Prozess {name} wurde beendet.")

        except PermissionError:
            messagebox.showerror("Fehler", "Keine Berechtigung zum Beenden dieses Prozesses.")
        except ProcessLookupError:
            messagebox.showerror("Fehler", "Der Prozess existiert nicht mehr.")
        except Exception as exc:
            messagebox.showerror("Fehler", f"Prozess konnte nicht beendet werden:\n{exc}")

    # -------------------------
    # Dienste
    # -------------------------
    def _build_services_tab(self):
        # Container für den Dienste-Tab
        container = ttk.Frame(self.services_tab, padding=12)
        container.pack(fill="both", expand=True)

        # Toolbar mit Aktualisieren-Button
        toolbar = ttk.Frame(container)
        toolbar.pack(fill="x", pady=(0, 8))
        ttk.Button(toolbar, text="Aktualisieren", command=self.refresh_services).pack(side="left")

        # Tabelle für Systemdienste
        columns = ("unit", "load", "active", "sub", "description")
        self.service_tree = ttk.Treeview(container, columns=columns, show="headings")

        # Spalteneinstellungen
        settings = [
            ("unit", "Dienst", 260),
            ("load", "Load", 80),
            ("active", "Active", 80),
            ("sub", "Sub", 100),
            ("description", "Beschreibung", 420),
        ]

        for col, title, width in settings:
            self.service_tree.heading(col, text=title)
            self.service_tree.column(col, width=width, anchor="w")

        # Scrollbar hinzufügen
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.service_tree.yview)
        self.service_tree.configure(yscrollcommand=scrollbar.set)

        # Tabelle und Scrollbar anzeigen
        self.service_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_services(self):
        # Alte Dienste-Einträge löschen
        for item in self.service_tree.get_children():
            self.service_tree.delete(item)

        # Linux-Dienste mit systemctl abrufen
        output = self._run_command([
            "systemctl",
            "list-units",
            "--type=service",
            "--all",
            "--no-pager",
            "--no-legend",
        ])

        # Falls keine Ausgabe vorhanden ist
        if not output.strip():
            self.service_tree.insert("", tk.END, values=("systemctl nicht verfügbar", "-", "-", "-", "-"))
            return

        # Jede Zeile parsen und in Tabelle einfügen
        for line in output.splitlines():
            parts = line.split(None, 4)
            if len(parts) >= 5:
                self.service_tree.insert("", tk.END, values=parts)

    # -------------------------
    # Geräte
    # -------------------------
    def _build_devices_tab(self):
        # Container für den Geräte-Tab
        container = ttk.Frame(self.devices_tab, padding=12)
        container.pack(fill="both", expand=True)

        # Toolbar mit Aktualisieren-Button
        toolbar = ttk.Frame(container)
        toolbar.pack(fill="x", pady=(0, 8))
        ttk.Button(toolbar, text="Aktualisieren", command=self.refresh_devices).pack(side="left")

        # Großes Textfeld für Hardware-Ausgaben
        self.devices_text = tk.Text(container, wrap="word")
        self.devices_text.pack(fill="both", expand=True)

    def refresh_devices(self):
        # Liste für mehrere Hardware-Sektionen
        sections = []

        # Block Devices anzeigen
        sections.append("=== Block Devices (lsblk) ===\n")
        sections.append(self._run_command(["lsblk", "-o", "NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE"]))

        # PCI-Geräte anzeigen
        sections.append("\n=== PCI Devices (lspci) ===\n")
        sections.append(self._run_command(["lspci"]))

        # USB-Geräte anzeigen
        sections.append("\n=== USB Devices (lsusb) ===\n")
        sections.append(self._run_command(["lsusb"]))

        # Netzwerk-Links anzeigen
        sections.append("\n=== Network Links ===\n")
        sections.append(self._run_command(["ip", "-brief", "link"]))

        # Textfeld leeren und neue Ausgabe einfügen
        self.devices_text.delete("1.0", tk.END)
        self.devices_text.insert(tk.END, "\n".join(sections))

    # -------------------------
    # Hilfsfunktionen
    # -------------------------
    def _run_command(self, cmd):
        # Führt einen externen Befehl aus und gibt stdout oder Fehlermeldung zurück
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,  # Ausgabe speichern statt direkt im Terminal anzeigen
                text=True,            # Ausgabe als String statt Bytes
                check=False,          # Fehler nicht direkt als Exception werfen
            )

            # Falls der Befehl einen Fehlercode liefert
            if result.returncode != 0 and result.stderr:
                return f"Fehler bei {' '.join(cmd)}:\n{result.stderr.strip()}"

            # Normale Ausgabe zurückgeben
            return result.stdout.strip() or "Keine Ausgabe"

        except FileNotFoundError:
            return f"Befehl nicht gefunden: {cmd[0]}"
        except Exception as exc:
            return f"Fehler bei {' '.join(cmd)}: {exc}"

    def _read_os_release(self):
        # Liest Informationen zur Linux-Distribution aus /etc/os-release
        path = "/etc/os-release"

        # Wenn Datei nicht existiert
        if not os.path.exists(path):
            return "Unbekannt"

        data = {}

        # Datei zeilenweise einlesen
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    data[key] = value.strip('"')

        # Schöne Distributionsbezeichnung zurückgeben
        return data.get("PRETTY_NAME", "Unbekannt")

    def _fmt_bytes(self, value):
        # Wandelt Byte-Werte in lesbare Einheiten um
        units = ["B", "KB", "MB", "GB", "TB"]
        size = float(value)

        for unit in units:
            if size < 1024 or unit == units[-1]:
                return f"{size:.1f} {unit}"
            size /= 1024

        return f"{size:.1f} TB"


# Einstiegspunkt des Programms
if __name__ == "__main__":
    # Hinweis, falls das Programm nicht unter Linux ausgeführt wird
    if not sys.platform.startswith("linux"):
        print("Dieses Programm ist primär für Linux gedacht.")

    # App starten
    app = SystemManagerApp()
    app.mainloop()
