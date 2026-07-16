# 📡 Remote Laboratory Instrument Automation using Python

A robust, Python-based automation framework designed for **remote control, real-time data acquisition, and verification of laboratory instruments**. By leveraging the **PyVISA** library and executing **SCPI** (Standard Commands for Programmable Instruments) commands over TCP/IP, this system bypasses manual lab measurements to enable fast, repeatable, and automated experimental workflows.

> ⚡ **Core Use Case:** Perfect for Hardware-in-the-Loop (HIL) testing, component characterization, and validating physical circuits against simulated models (e.g., Cadence Virtuoso designs).

---
## 📐 System Architecture

The physical and logical connection of the automated testbench is structured as follows:
+----------------------------------+
|  Agilent 33612A                  |
|  Arbitrary Waveform Generator    |
+-----------------+----------------+
                  |
                  | [BNC Coaxial Cable / Signal Out]
                  v
+-----------------+----------------+
|  Keysight MSO9404A               |
|  Mixed Signal Oscilloscope       |
+-----------------+----------------+
                  |
                  | [TCP/IP / Ethernet / VISA Protocol]
                  v
+-----------------+----------------+
|  Python Automation Engine        |
|  - PyVISA Control                |
|  - SCPI Command Dispatcher       |
+-----------------+----------------+
                  |
                  v
+-----------------+----------------+
|  Data Processing & Analytics     |
|  - Matplotlib Plots (PNG)        |
|  - Signal Analysis (CSV / NumPy) |
+----------------------------------+
---

## 🛠️ Hardware Setup

The framework is developed and tested using industry-standard laboratory equipment:

* **Signal Generation:** `Agilent 33612A` Arbitrary Waveform Generator (120 MHz, 2-Channel).
* **Measurement & Capture:** `Keysight MSO9404A` Mixed Signal Oscilloscope (4 GHz, 4 Analog + 16 Digital Channels).
* **Interface Protocols:** VISA (Virtual Instrument Software Architecture) API over LAN (TCP/IP).

---

## 🚀 Key Implemented Features

### 1. Remote Instrument Connection
* Establishes stable TCP/IP socket connections to target IP addresses using PyVISA resource managers.
* Automates instrument discovery and identification queries (`*IDN?`).

### 2. Waveform Generator Automation
* Dynamic configuration of output wave shapes (Sine, Square, Ramp).
* Remote sweep controls for **Frequency** and **Amplitude** values.
* Programmatic output state toggling (`OUTP ON`/`OFF`).

### 3. Oscilloscope Data Acquisition
* Autoscale and channel-specific coupling configurations via SCPI.
* Continuous time-domain voltage logging.
* High-speed raw waveform point extraction for deeper numerical analysis.
* Direct export of captured waveforms to structured `.csv` files.

---
