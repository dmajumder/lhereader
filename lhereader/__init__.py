import xml.etree.ElementTree as ET
from ROOT import TLorentzVector
from xml import sax
class Particle:
    def __init__(self, pdgid, spin, status, px = 0, py = 0, pz = 0, energy = 0, mass = 0, vtau = 0):
        self.pdgid = pdgid
        self.px = px
        self.py = py
        self.pz = pz
        self.energy = energy
        self.mass = mass
        self.spin = spin
        self.status = status
        self.vtau = vtau

    @property
    def p4(self):
        return TLorentzVector(self.px, self.py, self.pz, self.energy)

    @p4.setter
    def p4(self, value):
        self.px = value.Px()
        self.py = value.Py()
        self.pz = value.Pz()
        self.energy = value.E()
        self.mass = value.M()

    @property
    def p(self):
        return self.p4.P()

    @property
    def eta(self):
        return self.p4.Eta()

    @property
    def pt(self):
        return self.p4.Pt()

    @property
    def status(self):
        return self.status

    @property
    def vtau(self):
        return self.vtau

def ensure_is_list(argument):
    """Make sure that something is a list type

    :param argument: Object to check
    :type argument: anything
    :return: List containing all items in argument
    :rtype: list
    """
    if type(argument) is not list:
        return [argument]
    else:
        return argument


class Event:
    def __init__(self, num_particles):
        self.num_particles = num_particles
        self.particles = []
        self.weights = []
        self.scale = None

    def __add_particle__(self, particle):
        self.particles.append(particle)

    def get_particles_by_property(self, property, value):
        return filter(lambda x: getattr(x, property) in ensure_is_list(value), self.particles)

    def get_particles_by_multiple_properties(self, props_and_values):
        """Find particles fulfilling multiple filter criteria

        :param props_and_values: Property names and acceptable values for each property name.
        :type props_and_values: list
        :return: Filtered particles
        :rtype: list
        """
        parts = []
        for part in self.particles:
            good = True
            for prop, values in props_and_values:
                good &= getattr(part, prop) in ensure_is_list(values)
            if good:
                parts.append(part)
        return parts

    def get_particles_by_id(self, id):
        return self.get_particles_by_property("pdgid", id)


class LHEFData:
    def __init__(self, version = 0):
        self.version = version
        self.events = []

    def __add_event__(self, event):
        self.events.append(event)

    def get_particles_by_i_ds(self, idlist):
        partlist = []
        for event in self.events:
            partlist.extend(event.getParticlesByIDs(idlist))
        return partlist

class LHEReader():
    def __init__(self, file_path):
        self.file_path = file_path
        self.iterator = ET.iterparse(self.file_path)
        self.current = None
        self.current_weights = None
    def unpack_from_iterator(self):
        lines = self.current[1].text.strip().split("\n")
        event_header = lines[0].strip()
        num_part = int(event_header.split()[0].strip())
        e = Event(num_part)

        e.scale = float(lines[0].strip().split()[3])

        for i in range(1, num_part+1):
            part_data = lines[i].strip().split()
            p = Particle(pdgid = int(part_data[0]),
                        status = int(part_data[1]),
                        px = float(part_data[6]),
                        py = float(part_data[7]),
                        pz = float(part_data[8]),
                        energy = float(part_data[9]),
                        mass = float(part_data[10]),
                        vtau = float(part_data[11]),
                        spin = int(float(part_data[12])))
            e.__add_particle__(p)
        e.weights = self.current_weights


        return e

    def next_event(self):
        if(self.current):
            self.current[1].clear()

        xmlev = self.iterator.next()
        while xmlev[1].tag != "event":
            xmlev = self.iterator.next()
        self.current = xmlev

        xmlev = self.iterator.next()
        self.current_weights = []
        while xmlev[1].tag == "wgt":
            self.current_weights.append(float(xmlev[1].text))
            xmlev = self.iterator.next()
        return self.unpack_from_iterator()

