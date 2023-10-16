from typing import List, Optional

class Room:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._neighbors: List["Room"] = []

    def add_neighbor(self, room: "Room") -> None:
        self._neighbors.append(room)
        if isinstance(room, Room):
            room._neighbors.append(self)

    def enter(self) -> "Room":
        print(f"You have entered {self.name}.")
        print(self.description)
        return self

    def move_to_next_room(self) -> "Room":
        if not self._neighbors:
            print("There are no neighboring rooms.")
            return self
        print(f"From {self.name}, you can go to:")
        for i, neighbor in enumerate(self._neighbors):
            print(f"{i + 1}. {neighbor.name}")
        while True:
            choice = input(f"Enter your choice (1-{len(self._neighbors)}): ")
            if choice.isnumeric():
                choice = int(choice)
                if 1 <= choice <= len(self._neighbors):
                    next_room = self._neighbors[choice - 1]
                    print(f"You are now entering {next_room.name}.")
                    return next_room.enter()

    def is_locked(self) -> bool:
        return False

    def __str__(self) -> str:
        return self.name


class RiddleRoom(Room):
    def __init__(self, name: str, description: str, puzzle_question: str, puzzle_answer: str):
        super().__init__(name, description)
        self._puzzle_question = puzzle_question
        self._puzzle_answer = puzzle_answer
        self._locked = True

    def is_locked(self) -> bool:
        return self._locked

    def _unlock(self) -> Optional["Room"]:
        print(self._puzzle_question)
        answer = input().strip()
        if answer.lower() == self._puzzle_answer.lower():
            self._locked = False
            print("Nice, that's correct!")
            return self
        print(f"Incorrect answer. You cannot enter {self.name} until you solve the puzzle.")
        return None

    def enter(self) -> Optional["Room"]:
        if self.is_locked():
            return self._unlock()
        return super().enter()


class Player:
    def __init__(self, name: str, room: "Room"):
        self._name = name
        self._current_room = room

    @property
    def name(self) -> str:
        return self._name

    def move_on(self) -> None:
        moved_to = self._current_room.move_to_next_room()
        if moved_to is not None:
            self._current_room = moved_to

    def __str__(self) -> str:
        return self._name


def all_rooms_unlocked(rooms: List[Room]) -> bool:
    for room in rooms:
        if room.is_locked():
            return False
    return True


def main():
    # Create rooms
    room1 = Room("Room 1", "This is room 1.")
    room2 = RiddleRoom("Room 2", "This is room 2.", "What is the capital of France?", "Paris")
    room3 = RiddleRoom("Room 3", "This is room 3.", "What is the square root of 16?", "4")
    room4 = RiddleRoom("Room 4", "This is room 4.", "What is the largest planet in our solar system?", "Jupiter")
    room5 = RiddleRoom("Room 5", "This is room 5.", "What is the largest continent by land area?", "Asia")
    room6 = RiddleRoom("Room 6", "This is room 6.", "What is the capital of Japan?", "Tokyo")
    room7 = RiddleRoom("Room 7", "This is room 7.", "What is the smallest country in the world by land area?", "Vatican City")
    room8 = RiddleRoom("Room 8", "This is room 8.", "What is the capital of Italy?", "Rome")
    room9 = RiddleRoom("Room 9", "This is room 9.", "What is the largest ocean on Earth?", "Pacific")

    # Connect rooms
    room1.add_neighbor(room2)
    room1.add_neighbor(room3)
    room1.add_neighbor(room4)
    room2.add_neighbor(room5)
    room2.add_neighbor(room6)
    room3.add_neighbor(room7)
    room4.add_neighbor(room8)
    room5.add_neighbor(room9)

    rooms = [room1, room2, room3, room4, room5, room6, room7, room8, room9]

    # Create player
    playername = input("Enter your name: ")
    player = Player(playername, room1)

    print(f"Welcome {player.name}! You start in {room1}")

    while not all_rooms_unlocked(rooms):
        player.move_on()

    print("Great, you're done!")

if __name__ == "__main__":
    main()
    