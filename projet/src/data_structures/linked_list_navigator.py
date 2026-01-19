"""
Linked list navigator implementation for station navigation.
"""

from projet.src.entities.station import Station
from projet.src.data_structures.linked_list_node import StationNode
from projet.src.interfaces.station_navigator import IStationNavigator


class LinkedListNavigator(IStationNavigator):
    """
    Station navigator implementation using a doubly linked list.
    Provides sequential navigation with O(1) next/previous operations.
    """

    def __init__(self, stations: list[Station]) -> None:
        self._head: StationNode | None = None
        self._tail: StationNode | None = None
        self._current: StationNode | None = None

        if not stations:
            return

        # Build the linked list from the stations
        previous_node = None
        for station in stations:
            new_node = StationNode(station=station, previous=previous_node)
            if previous_node:
                previous_node.next = new_node
            else:
                self._head = new_node
            previous_node = new_node
        self._tail = previous_node

        # Create circular links (works even with single node)
        self._tail.next = self._head
        self._head.previous = self._tail

        # Set the current node to the head of the list
        self._current = self._head

    def get_current(self) -> Station | None:
        """
        Returns the current station without moving the pointer.

        Returns:
            Current station or None if list is empty
        """
        return self._current.station if self._current else None

    def has_previous(self) -> bool:
        """
        Checks if there is a previous station available.

        Returns:
            True if previous station exists, False otherwise
        """
        return bool(self._head)

    def has_next(self) -> bool:
        """
        Checks if there is a next station available.

        Returns:
            True if next station exists, False otherwise
        """
        return bool(self._head)

    def get_previous(self) -> Station | None:
        """
        Moves to the previous station and returns it.
        If already at the start, returns None without moving.

        Returns:
            Previous station or None if at start or list is empty
        """
        if self._current:
            self._current = self._current.previous
            return self._current.station
        return None

    def get_next(self) -> Station | None:
        """
        Moves to the next station and returns it.
        If already at the end, returns None without moving.

        Returns:
            Next station or None if at end or list is empty
        """
        if self._current:
            self._current = self._current.next
            return self._current.station
        return None

    def set_current(self, station: Station) -> None:
        """
        Sets the current station to the specified one.

        Args:
            station: Station to set as current

        Raises:
            ValueError: If station is not found in the list
        """
        if self._head is None:
            raise ValueError("Station list is empty")

        current_node = self._head

        # First itération : check _head
        if current_node.station == station:
            self._current = current_node
            return

        current_node = current_node.next

        # Navigate back to _head
        while current_node is not None and current_node is not self._head:
            if current_node.station == station:
                self._current = current_node
                return
            current_node = current_node.next

        raise ValueError("Station not found in navigator")

    def get_all_stations(self) -> list[Station]:
        """
        Returns all stations in the navigator as a list.

        Returns:
            List of all Station objects in navigation order

        Note:
            For an empty list, returns an empty list.
            For a circular list, returns stations starting from head.
        """
        if self._head is None:
            return []

        stations = []
        current = self._head

        # Traverse the circular list once
        while True:
            stations.append(current.station)
            current = current.next
            if current is self._head:
                break

        return stations
