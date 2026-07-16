import pyvisa
import time


class Instrument:
    def __init__(self, ip, timeout=5000):
        self.ip = ip
        self.timeout = timeout
        self.rm = None
        self.inst = None

    def connect(self):
        self.rm = pyvisa.ResourceManager()

        # VISA over TCP/IP
        resource = f"TCPIP0::{self.ip}::inst0::INSTR"

        self.inst = self.rm.open_resource(resource)

        self.inst.timeout = self.timeout
        self.inst.read_termination = "\n"
        self.inst.write_termination = "\n"

        self.write("*CLS")

    def write(self, command):
        self.inst.write(command)

    def query(self, command):
        return self.inst.query(command).strip()

    def close(self):
        if self.inst is not None:
            self.inst.close()

        if self.rm is not None:
            self.rm.close()
import time

GEN_IP = "147.102.14.105"
SCOPE_IP = "147.102.14.104"

generator = Instrument(GEN_IP)
oscilloscope = Instrument(SCOPE_IP)

try:
    print("Connecting to instruments...")

    generator.connect()
    print(f"Generator connected: {generator.query('*IDN?')}")

    oscilloscope.connect()
    print(f"Oscilloscope connected: {oscilloscope.query('*IDN?')}")

    # =====================================
    # Generator setup
    # =====================================
    print("\nSetting up Waveform Generator...")

    generator.write("SOURCE1:FUNCTION TRIANGLE")
    generator.write("SOURCE1:FREQUENCY 2500")
    generator.write("SOURCE1:VOLTAGE 1.5")
    generator.write("OUTPUT1 ON")

    time.sleep(1)

    # =====================================
    # Scope setup
    # =====================================
    print("\nConfiguring Oscilloscope...")

    oscilloscope.write(":AUToscale")

    time.sleep(10)

    # =====================================
    # Measurements
    # =====================================
    print("\nFetching measurements from scope...")

    vpp = float(
        oscilloscope.query(":MEASure:VPP? CHANnel1")
    )

    freq = float(
        oscilloscope.query(":MEASure:FREQuency? CHANnel1")
    )

    print(f"Measured Vpp: {vpp:.4f} V")
    print(f"Measured Frequency: {freq/1000:.3f} kHz")

except Exception as e:
    print("Error:", e)

finally:
    try:
        generator.write("OUTPUT1 OFF")
    except:
        pass

    generator.close()
    oscilloscope.close()

    print("Done!")
