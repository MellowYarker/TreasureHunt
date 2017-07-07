"""This file contains the TreasureHunt class which is used to play the game."""
from grid import Grid


class TreasureHunt:
    """
    Represents an instance of the treasure hunt game.

    === Attributes: ===
    @type grid_path: str
        pathname to a text file that contains the grid map
        see Grid and Node classes for the format
    @type sonars: int
       the number of sonars the boat can drop
    @type so_range: int
       the range of sonars
    @type state: str
       the state of the game:
          STARTED, OVER, WON
    """

    def __init__(self, grid_path, sonars, so_range):
        """
        Initialize a new game with map data stored in the file grid_path
        and commands to be used to play the game in game_path file.

        @type grid_path: str
           pathname to a text file that contains the grid map
           see Grid and Node classes for the format
        @type sonars: int
        @type so_range: int
        """
        self.grid_path = Grid(grid_path)
        self.sonars = sonars
        self.so_range = so_range
        self.state = "STARTED"

    def process_command(self, command):
        """
        Process a command, set and return the state of the game
        after processing this command
        @type command: str
           a command that can be used to play, as follows:
           GO direction, where direction=N,S,E,W,NW,NE,SW,SE
           SONAR, drops a sonar
           QUIT, quit the game
        @rtype: str
           the state of the game
        """
        # Removing this print statement stops the map from being shown when you
        # play the game

        print(self.grid_path)
        print('\n')

        if command == "QUIT" or self.sonars == 0:
            self.state = "OVER"
            return self.state
        elif "GO" in command:
            self.grid_path.move(command.split()[1])
        elif "SONAR" == command:
            self.sonars -= 1
            if self.grid_path.get_treasure(self.so_range) is not None:
                if self.grid_path.retrace_path(self.grid_path.boat,
                                               self.grid_path.treasure) != []:
                    self.state = "WON"
                else:
                    self.state = "OVER"
        return self.state


class Play(TreasureHunt):
    """A class to play the treasure hunt game"""

    def __init__(self, grid_path, sonars, so_range, game_path):
        """Initialize a new game with map data stored in the file grid_path
        and commands to be used to play the game in game_path file."""

        TreasureHunt.__init__(self, grid_path, sonars, so_range)
        self.game_path = game_path

    def instructions(self):
        """Give some simple instructions"""

        print("""Weclome! To play the game, build the map in the file map.txt using the following characters:\n
                .
                +
                B
                T\n
                The "." represents open water, which is a location you can move to.\n
                The "+" represents land, which your boat cannot cross.\n
                The "B" represents your boat, which moves along the water.\n
                Finally the "T" represents the treasure, which is where you are trying to get to.\n\n
                The commands can be entered in the commands.txt file. Commands work as follows:\n
                GO direction\n
                SONAR\n
                QUIT\n\n
                Replace "direction" with a direction such as N, S, NE, etc
                """)
        play = input('Are you ready to play?(y/n): ')
        if play == 'y':
            self.play_game()
        elif play == 'n':
            print("Exiting")

    def play_game(self):
        """Play the game with the map and the command files."""

        with open(self.game_path, 'r') as game:
            commands = game.readlines()
        for i in commands:
            # Remove newline character
            i = i[:-1]
            print(TreasureHunt.process_command(self, i))


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    # import python_ta
    # python_ta.check_all(config='pylintrc.txt')
    a = Play('map.txt', 3, 14, 'commands.txt')
    a.instructions()
