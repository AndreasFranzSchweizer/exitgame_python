class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.__neighbors = []

        
    def add_neighbor(self, room):
        """
        :type room: Room
        """
        self.__neighbors.append(room)
        if isinstance(room, Room):
            room.__neighbors.append(self)
        
    def enter(self):
        print(f"You have entered {self.name}.")
        print(self.description)
        return self

    
    def move_to_next_room(self):
        if not self.__neighbors:
            print("There are no neighboring rooms.")
            return self
        print(f"From {self.name}, you can go to:")
        for i, neighbor in enumerate(self.__neighbors):
            print(f"{i+1}. {neighbor.name}")
        while True:
            choice = input(f"Enter your choice (1-{len(self.__neighbors)}): ")
            if choice.isnumeric():
                choice = int(choice)
                if 1 <= choice <= len(self.__neighbors):
                    next_room = self.__neighbors[choice - 1]
                    print(f"You are now entering {next_room.name}.")
                    return next_room.enter()

                
    def is_locked(self):
        return False

    
    def __str__(self):
        return self.name


class RiddleRoom(Room):
    def __init__(self, name, description, puzzle_question, puzzle_answer):
        super().__init__(name, description)
        self.__puzzle_question = puzzle_question
        self.__puzzle_answer = puzzle_answer
        self.__locked = True

        
    def is_locked(self):
        return self.__locked

    
    def __unlock(self):
        print(self.__puzzle_question)
        answer = input().strip()
        if answer.lower() == self.__puzzle_answer.lower():
            self.__locked = False
            return self
        print(f"Incorrect answer. You cannot enter {self.name} until you solve the puzzle.")
        return None

        
    def enter(self):
        if self.is_locked():
            return self.__unlock()
        return super().enter()


class Player:
    def __init__(self, name, room):
        self.__name = name
        self.__current_room = room

        
    @property
    def name(self):
        return self.__name
 

    def move_on(self):
        moved_to = self.__current_room.move_to_next_room()
        if moved_to is not None:
            self.__current_room = moved_to

            
    def __str__(self):
        return self.__name

    
def all_rooms_unlocked(rooms):
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

main()
