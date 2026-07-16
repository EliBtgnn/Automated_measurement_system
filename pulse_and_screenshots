import pyvisa
import os
import time
from datetime import datetime


# =========================
# SETTINGS
# =========================
GEN_IP = "147.102.14.105"
SCOPE_IP = "147.102.14.104"

SAVE_FOLDER = r"C:\Oscilloscope_Logs"
os.makedirs(SAVE_FOLDER, exist_ok=True)


# =========================
# VISA INSTRUMENT CLASS
# =========================
class Instrument:
    def __init__(self, ip, timeout=5000):
        self.ip = ip
        self.timeout = timeout
        self.rm = None
        self.inst = None

    def connect(self):
        self.rm = pyvisa.ResourceManager()
        resource = f"TCPIP0::{self.ip}::inst0::INSTR"

        self.inst = self.rm.open_resource(resource)
        self.inst.timeout = self.timeout
        self.inst.read_termination = "\n"
        self.inst.write_termination = "\n"

        self.write("*CLS")

    def write(self, cmd):
        self.inst.write(cmd)

    def query(self, cmd):
        return self.inst.query(cmd).strip()

    def query_binary(self, cmd):
        return self.inst.query_binary_values(
            cmd,
            datatype="B",
            container=bytes
        )

    def close(self):
        if self.inst:
            self.inst.close()
        if self.rm:
            self.rm.close()


# =========================
# RECOVERY FUNCTION
# =========================
def recover_scope(scope):
    print("\n[RECOVERY] Resetting scope...")

    scope.write(":STOP")
    scope.query("*OPC?")

    scope.write(":TRIGger:MODE EDGE")
    scope.write(":TRIGger:EDGE:SOURce CHANnel1")
    scope.write(":TRIGger:EDGE:LEVel 0")

    scope.write(":AUToscale")
    scope.query("*OPC?")

    scope.write(":RUN")
    scope.query("*OPC?")

    print("[RECOVERY] Done.")


# =========================
# SCREENSHOT FUNCTION (FIXED)
# =========================
def safe_screenshot(scope, folder):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(folder, f"scope_{timestamp}.png")

    print("\n[SCREENSHOT] Capturing...")

    scope.write(":STOP")
    scope.query("*OPC?")

    scope.write(":HARDcopy:INKSaver OFF")

    img = scope.inst.query_binary_values(
        ":DISPlay:DATA? PNG",
        datatype="B",
        container=bytes
    )

    with open(filename, "wb") as f:
        f.write(img)

    scope.write(":RUN")

    print(f"[SCREENSHOT] Saved -> {filename}")
    return filename


# =========================
# MAIN PROGRAM
# =========================
generator = Instrument(GEN_IP)
oscilloscope = Instrument(SCOPE_IP)

try:
    print("Connecting instruments...")

    generator.connect()
    oscilloscope.connect()

    print("Generator:", generator.query("*IDN?"))
    print("Scope:", oscilloscope.query("*IDN?"))

    # =========================
    # GENERATOR SETUP
    # =========================
    print("\nConfiguring generator...")

    generator.write("SOURCE1:FUNCTION SQUARE")
    generator.write("SOURCE1:FREQUENCY 2500")
    generator.write("SOURCE1:VOLTAGE 1.5")
    generator.write("OUTPUT1 ON")

    time.sleep(1)

    # =========================
    # SCOPE SETUP
    # =========================
    print("\nConfiguring oscilloscope...")

    recover_scope(oscilloscope)

    # =========================
    # MEASUREMENTS
    # =========================
    print("\nMeasuring signal...")

    vpp = float(oscilloscope.query(":MEASure:VPP? CHANnel1"))
    freq = float(oscilloscope.query(":MEASure:FREQuency? CHANnel1"))

    print(f"Vpp  = {vpp:.4f} V")
    print(f"Freq = {freq/1000:.3f} kHz")

    # =========================
    # SCREENSHOT
    # =========================
    safe_screenshot(oscilloscope, SAVE_FOLDER)

except Exception as e:
    print("ERROR:", e)

finally:
    try:
        generator.write("OUTPUT1 OFF")
    except:
        pass

    generator.close()
    oscilloscope.close()

    print("\nDone.")
