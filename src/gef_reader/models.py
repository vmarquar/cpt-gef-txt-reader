from dataclasses import dataclass

@dataclass
class CPTMeasurement:
    #penetration_length: float|None = None
    measured_depth: float|None = None # measured depth, downwards along the metal rod
    #penetration_elevation: float|None = None
    qc: float|None = None #measured cone resistance
    qt: float|None = None #corrected cone resistance
    fs: float|None = None # measures friction resistance
    u1: float|None = None # pore pressure, measured at position u1
    u2: float|None = None # pore pressure, measured at position u2
    u3: float|None = None # pore pressure, measured at position u3
    inclination: float|None = None
    ic: float|None = None
    friction_ratio_rf: float|None = None
    su_min: float|None = None
    su_max: float|None = None
    soilfr: int|None = None
    soilbq: int|None = None
    soilavg: int|None = None
    inner_friction_angle: float|None = None

@dataclass
class CPTHeader:
    project_number: str|None = None
    project_name: str|None = None
    hole_id: str|None = None
    client_name: str|None = None
    location: str|None = None
    date: str|None = None
    cone_number: str|None = None
    water_level: float|None = None
    pre_excavation: float|None = None
    northing: float|None = None
    easting: float|None = None
    elevation: float|None = None

@dataclass
class CPT:
    cpt_header: CPTHeader
    cpt_measurements: list[CPTMeasurement]
