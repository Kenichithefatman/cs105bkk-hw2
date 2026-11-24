"""HW2 · club.py: the club and its chat bot. Practises Session 4 (each class has one job),
Session 5 (importing your own modules and the standard library) and Session 6 (catching only
the errors you expect)."""

from errors import SignupError, UnknownEventError
from event import Event


class Club:
    """A student club. It finds events by title; each Event looks after its own seats."""

    def __init__(self, name: str):
        """Provided: a club with no events yet."""
        self.name = name
        self.events: dict[str, Event] = {}

    def add_event(self, title: str, capacity: int) -> Event:
        if capacity < 1:
         raise ValueError(f"capacity must be at least 1, got {capacity}")
        if title in self.events:
            raise ValueError(f"event already exists: {title}")
        new_event = Event(title, capacity)
        self.events[title] = new_event
        return new_event

    def event(self, title: str) -> Event:
        try:
         return self.events[title]
        except KeyError:
         raise UnknownEventError(title)

    def handle(self, line: str) -> str:
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 3:
           return f"Sorry, I don't understand {line!r}."
        command, title, member = parts
        command = command.lower()
        try:
            event = self.event(title)
            if command == "join":
                result = event.sign_up(member)
                if result == "seat":
                    return f"{member} has a seat at {title}."
                return f"{member} is on the waitlist for {title}."
            if command == "leave":
                moved = event.cancel(member)
                if moved is not None:
                    return f"{member} left {title}. {moved} gets the seat."
                return f"{member} left {title}."
            return f"Sorry, I don't understand {line!r}."
        except SignupError as error:
            return f"Sorry, {error}."
    def attendance(self) -> dict[str, int]:
        from collections import Counter
        counts = Counter()
        for event in self.events.values():
            for member in event.seats:
                counts[member] += 1
        return dict(counts)

if __name__ == "__main__":
    # Provided: a short run of the chat bot. It runs only with `python club.py`, not on import.
    club = Club("Harbour.Space Bangkok club")
    club.add_event("Muay Thai basics", 2)
    for line in [
        "join, Muay Thai basics, Nino",
        "join, Muay Thai basics, Aung",
        "join, Muay Thai basics, Tashi",
        "leave, Muay Thai basics, Nino",
        "join, Chess night, Ploy",
    ]:
        print(club.handle(line))
