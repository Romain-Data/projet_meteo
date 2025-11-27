from abc import ABC, abstractmethod

from projet.src.entities.station import Station


class IStationNavigator(ABC):
    """
    Interface defining navigation operations between stations.
    Implementations can use different data structures
        (linked list, array, tree, etc.)
    to provide sequential navigation between weather stations.
    """

    @abstractmethod
    def get_current(self) -> Station | None:
        """Returns the current station, or None if no station is selected."""
        pass

    @abstractmethod
    def get_previous(self) -> Station | None:
        """Returns the previous station, or None if at the beginning."""
        pass

    @abstractmethod
    def get_next(self) -> Station | None:
        """Returns the next station, or None if at the end."""
        pass

    @abstractmethod
    def set_current(self, station: Station) -> None:
        """Sets the current station to the given station."""
        pass

    @abstractmethod
    def has_previous(self) -> bool:
        """Returns True if there is a previous station available."""
        pass

    @abstractmethod
    def has_next(self) -> bool:
        """Returns True if there is a next station available."""
        pass
