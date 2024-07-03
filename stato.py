from dataclasses import dataclass

@dataclass
class Stato:
    id: str
    Name: str
    Capital: str
    Lat: float
    Lng: float
    Area: int
    Population: int
    Neighbors: str


    def __str__(self):
        return f"{self.Name} - {self.id}"

    def __hash__(self):
        return hash(self.id)