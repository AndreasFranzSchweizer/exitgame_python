class Room:
    def __init__(self, name, description):
        self._name = name
        self._description = description
        self._neighbors = []
        self._player = None

    def add_neighbor(self, room):
        self._neighbors.append(room)
        room._neighbors.append(self)

    def enter(self, player):
        if self.is_unlocked():
            self._player = player
            player.current_room = self
            print(f"You have entered {self._name}.")
            print(self._description)

    def move_to_next_room(self):
        if not self.is_unlocked():
            print(f"You need to solve the puzzle to enter {self._name}.")
            return
        if not self._neighbors:
            print("There are no neighboring rooms.")
            return
        print(f"From {self._name}, you can go to:")
        for i, neighbor in enumerate(self._neighbors):
            print(f"{i+1}. {neighbor._name}")
        while True:
            choice = input(f"Enter your choice (1-{len(self._neighbors)}): ")
            if choice.isnumeric():
                choice = int(choice)
                if 1 <= choice <= len(self._neighbors):
                    next_room = self._neighbors[choice - 1]
                    print(f"You are now entering {next_room._name}.")
                    next_room.enter(self._player)
                    break

    def is_unlocked(self):
        return True

    def __str__(self):
        return self._name


class LockedRoom(Room):
    def __init__(self, name, description, puzzle_question, puzzle_answer):
        super().__init__(name, description)
        self._puzzle_question = puzzle_question
        self._puzzle_answer = puzzle_answer
        self._unlocked = False

    def is_unlocked(self):
        return self._unlocked

    def enter(self, player):
        if not self.is_unlocked():
            print(self._puzzle_question)
            answer = input().strip()
            if answer.lower() == self._puzzle_answer.lower():
                self._unlocked = True
            else:
                print(f"Incorrect answer. You cannot enter {self._name} until you solve the puzzle.")
                return
        super().enter(player)


class Player:
    def __init__(self, name):
        self._name = name
        self.current_room = None

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self._name

def all_rooms_unlocked(rooms):
    for room in rooms:
        if not room.is_unlocked():
            return False
    print("Great, you're done!")
    return True

def main():
    # Create rooms
    room1 = Room("Room 1", "This is room 1.")
    room2 = LockedRoom("Room 2", "This is room 2.", "What is the capital of France?", "Paris")
    room3 = LockedRoom("Room 3", "This is room 3.", "What is the square root of 16?", "4")
    room4 = LockedRoom("Room 4", "This is room 4.", "What is the largest planet in our solar system?", "Jupiter")
    room5 = LockedRoom("Room 5", "This is room 5.", "What is the largest continent by land area?", "Asia")
    room6 = LockedRoom("Room 6", "This is room 6.", "What is the capital of Japan?", "Tokyo")
    room7 = LockedRoom("Room 7", "This is room 7.", "What is the smallest country in the world by land area?", "Vatican City")
    room8 = LockedRoom("Room 8", "This is room 8.", "What is the capital of Italy?", "Rome")
    room9 = LockedRoom("Room 9", "This is room 9.", "What is the largest ocean on Earth?", "Pacific")

    # Connect rooms
    room1.add_neighbor(room2)
    room1.add_neighbor(room3)
    room1.add_neighbor(room4)
    room2.add_neighbor(room5)
    room2.add_neighbor(room6)
    room3.add_neighbor(room7)
    room4.add_neighbor(room8)
    room5.add_neighbor(room9)
    
    rooms = [room1,room2,room3,room4,room5,room6,room7,room8,room9]

    # Create player
    player_name = input("Enter your name: ")
    player = Player(player_name)
    
    room1.enter(player)
    
    while not all_rooms_unlocked(rooms):
        player.current_room.move_to_next_room()
    
main()
