from __future__ import annotations
from dataclasses import dataclass

from projet.src.entities.station import Station


@dataclass
class StationNode:
    """
    Node in a doubly linked list of weather stations.
    Each node contains a station and references to previous/next nodes.
    """
    station: Station
    next: StationNode | None = None
    previous: StationNode | None = None
