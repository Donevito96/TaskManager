# Linux System Manager

### Task Manager & Device Manager for Linux

---

## 📌 Overview

**Linux System Manager** is a custom-built system monitoring and management tool for Linux, inspired by the functionality of the Windows Task Manager and Device Manager.

The goal of this project is to provide a **centralized, user-friendly graphical interface** to monitor system performance, manage processes, inspect services, and view hardware information.

---

## 🚀 Features

### 📊 System Overview

* Real-time CPU usage
* RAM utilization
* Disk usage
* Network activity (upload/download)
* System uptime
* Basic system information (hostname, kernel, OS)

### ⚙️ Process Management

* List all running processes
* Filter processes by name
* View CPU and memory usage per process
* Terminate processes safely

### 🔧 Services (systemctl)

* View active and inactive system services
* Display service status and descriptions

### 🖥️ Device Manager

* View hardware information using:

  * `lsblk` (storage devices)
  * `lspci` (PCI devices)
  * `lsusb` (USB devices)
  * `ip` (network interfaces)

---

## 🛠️ Technologies Used

* **Python 3**
* **Tkinter** – GUI framework
* **psutil** – system monitoring
* Linux CLI tools:

  * `systemctl`
  * `lsusb`
  * `lspci`
  * `lsblk`
  * `ip`

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/linux-system-manager.git
cd linux-system-manager
```

### 2. Install dependencies

```bash
pip install psutil
```

### 3. Install tkinter (Ubuntu / Pop!_OS)

```bash
sudo apt update
sudo apt install python3-tk
```

---

## ▶️ Usage

Run the application:

```bash
python3 Linux.py
```

---

## ⚠️ Notes

* This tool is designed for **Linux systems only**
* Some features may require **root privileges**
* Hardware and service output depends on your system configuration

---

## 🎯 Project Goals

* Combine multiple Linux system tools into a **single GUI**
* Improve usability for **beginners and administrators**
* Provide a foundation for further extensions (e.g. monitoring, security analysis)

---

## 🔮 Future Improvements

* Modern UI (PySide6 / Qt)
* Dark Mode
* Temperature monitoring (lm-sensors)
* Start/Stop services
* Network connection viewer (like Windows Resource Monitor)
* Alerts for high CPU/RAM usage

---

## 👨‍💻 Author

**Yasin Altundag**

* IT System Integration & Cybersecurity Enthusiast
* Focus: SOC / Blue Team / System Monitoring

---

## ⭐ Contributing

Feel free to fork this project and improve it.
Pull requests are welcome!

---

## 📄 License

This project is open-source and available under the MIT License.



# TaskManager
Linux System Manager (Task Manager &amp; Device Manager)
Deutsch – Projektbeschreibung

Linux System Manager (Task Manager & Device Manager)

Dieses Projekt ist ein selbst entwickelter System Manager für Linux, der sich an den Funktionen des Windows Task Managers und Geräte-Managers orientiert. Ziel ist es, eine zentrale und benutzerfreundliche Oberfläche zu schaffen, um Systemressourcen, Prozesse, Dienste und Hardwareinformationen übersichtlich darzustellen.

Die Anwendung bietet eine Echtzeit-Übersicht über CPU-, RAM-, Festplatten- und Netzwerkauslastung sowie eine detaillierte Prozessliste mit Filter- und Beenden-Funktion. Zusätzlich können laufende Systemdienste über systemctl angezeigt und grundlegende Hardwareinformationen über Tools wie lsusb, lspci und lsblk abgerufen werden.

Das Projekt kombiniert mehrere typische Linux-Systemtools in einer grafischen Oberfläche und erleichtert damit insbesondere Einsteigern und Administratoren die Systemanalyse und Fehlerdiagnose.

Technologien:

Python
Tkinter (GUI)
psutil (Systeminformationen)
Linux CLI Tools (systemctl, lsusb, lspci, lsblk)
--------------------------------------------------------------------------------------------------------------------
English – Project Description

Linux System Manager (Task Manager & Device Manager)

This project is a custom-built system manager for Linux inspired by the functionality of the Windows Task Manager and Device Manager. The goal is to provide a centralized and user-friendly interface for monitoring system resources, managing processes, viewing services, and inspecting hardware information.

The application includes a real-time overview of CPU, memory, disk, and network usage, as well as a detailed process list with filtering and termination capabilities. It also allows users to view active system services via systemctl and retrieve hardware information using tools such as lsusb, lspci, and lsblk.

This project combines multiple common Linux system tools into a single graphical interface, making system monitoring and troubleshooting more accessible—especially for beginners and system administrators.

Technologies:

Python
Tkinter (GUI)
psutil (system monitoring)
Linux CLI tools (systemctl, lsusb, lspci, lsblk)
