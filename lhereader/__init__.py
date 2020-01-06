import xml.etree.ElementTree as ET
from xml import sax
from skhep.math import LorentzVector
import sys
if sys.version_info < (3,7):
    from dataclasses import dataclass

@dataclass
class Particle:
    pdgid: int
    px: float
    py: float
    pz: float
    energy: float
    mass: float
    spin: float
    status: int
    vtau: float
    parent: int

    def p4(self):
        return LorentzVector(self.px, self.py, self.pz, self.energy)


@dataclass
class Event:
    particles: list
    weights: list
    scale: float

    def add_particle(self, particle):
        self.particles.append(particle)


class LHEReader():
    def __init__(self, file_path):
        self.file_path = file_path
        self.iterator = ElementTree.iterparse(self.file_path)
        self.current = None
        self.current_weights = None

    def unpack_from_iterator(self):
        # Read the lines for this event
        lines = self.current[1].text.strip().split("\n")
        
        # Create a new event
        event = Event()
        event.scale = float(lines[0].strip().split()[3])
        event.weights = self.current_weights

        # Read header
        event_header = lines[0].strip()
        num_part = int(event_header.split()[0].strip())

        # Iterate over particle lines and push back
        for ipart in range(1, num_part+1):
            part_data = lines[ipart].strip().split()
            p = Particle(pdgid = int(part_data[0]),
                        status = int(part_data[1]),
                        parent = int(part_data[2]),
                        px = float(part_data[6]),
                        py = float(part_data[7]),
                        pz = float(part_data[8]),
                        energy = float(part_data[9]),
                        mass = float(part_data[10]),
                        vtau = float(part_data[11]),
                        spin = int(float(part_data[12])))
            event.add_particle(p)

        return event

    def __iter__(self):
        return self

    def __next__(self):
        # Clear XML iterator
        if(self.current):
            self.current[1].clear()

        # Find next event in XML
        element = self.iterator.next()
        while element[1].tag != "event":
            element = self.iterator.next()
        self.current = element

        # Weight information comes after
        # the actual event
        element = self.iterator.next()
        self.current_weights = []
        while element[1].tag == "wgt":
            self.current_weights.append(float(element[1].text))
            element = self.iterator.next()
        return self.unpack_from_iterator()

