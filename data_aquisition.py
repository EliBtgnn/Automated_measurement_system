import pyvisa
import time
import csv


class Instrument:
    def __init__(self, ip):
        self.ip = ip

    def connect(self):
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource(
            f"TCPIP0::{self.ip}::inst0::INSTR"
        )

        self.inst.read_termination = "\n"
        self.inst.write_termination = "\n"

    def write(self, cmd):
        self.inst.write(cmd)

    def query(self, cmd):
        return self.inst.query(cmd).strip()

    def close(self):
        self.inst.close()
        self.rm.close()


GEN_IP = "147.102.14.105"
SCOPE_IP = "147.102.14.104"

gen = Instrument(GEN_IP)
scope = Instrument(SCOPE_IP)

try:
    gen.connect()
    scope.connect()

    gen.write("SOURCE1:FUNCTION SIN")
    gen.write("SOURCE1:FREQUENCY 1000")
    gen.write("SOURCE1:VOLTAGE 2")
    gen.write("OUTPUT1 ON")

    scope.write(":AUTOSCALE")

    time.sleep(5)

    data = []

    print("Starting acquisition...")

    for i in range(60):

        vpp = float(
            scope.query(":MEASure:VPP? CHANnel1")
        )

        timestamp = time.time()

        print(i, vpp)

        data.append([timestamp, vpp])

        time.sleep(1)

    with open("daq_data.csv", "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Time",
            "Vpp"
        ])

        writer.writerows(data)

finally:

    gen.write("OUTPUT1 OFF")

    gen.close()
    scope.close()
