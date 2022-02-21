from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class Province(Enum):
    """Provinces and its short names"""

    pir = "Pinar del Río"
    art = "Artemisa"
    may = "Mayabeque"
    hab = "La Habana"
    mat = "Matanzas"
    cfg = "Cienfuegos"
    ssp = "Sancti Spíritus"
    vlc = "Villa Clara"
    cav = "Ciego de Ávila"
    cam = "Camagüey"
    ltu = "Las Tunas"
    hol = "Holguín"
    gra = "Granma"
    stg = "Santiago de Cuba"
    gto = "Guantánamo"
    isj = "Isla de la Juventud"


class Travel(BaseModel):
    """Travels parsed from Viajando channel"""

    origin: str
    destination: str
    transport: str
    section: str
    date_time: datetime
    day_of_week: str
    seat: int

    @property
    def origin_short_name(self):
        return Province(self.origin).name

    @property
    def destination_short_name(self):
        return Province(self.destination).name

    def __repr__(self) -> str:
        out = "From {0} to {1} at {2} {3}".format(
            self.origin_short_name.upper(),
            self.destination_short_name.upper(),
            self.transport,
            self.date_time
        )
        return out
