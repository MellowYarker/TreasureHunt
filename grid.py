"""
This module contains the Node and Grid classes.
"""

import functools
import sys
from container import PriorityQueue


@functools.total_ordering
class Node:
    """
    Represents a node in the grid. A node can be navigable
    (that is located in water)
    or it may belong to an obstacle (island).

    === Attributes: ===
    @type navigable: bool
       navigable is true if and only if this node represents a
       grid element located in the sea
       else navigable is false
    @type grid_x: int
       represents the x-coordinate (counted horizontally, left to right)
       of the node
    @type grid_y: int
       represents the y-coordinate (counted vertically, top to bottom)
       of the node
    @type parent: Node
       represents the parent node of the current node in a path
       for example, consider the grid below:
        012345
       0..+T..
       1.++.++
       2..B..+
       the navigable nodes are indicated by dots (.)
       the obstacles (islands) are indicated by pluses (+)
       the boat (indicated by B) is in the node with
       x-coordinate 2 and y-coordinate 2
       the treasure (indicated by T) is in the node with
       x-coordinate 3 and y-coordinate 0
       the path from the boat to the treasure if composed of the sequence
       of nodes with coordinates:
       (2, 2), (3,1), (3, 0)
       the parent of (3, 0) is (3, 1)
       the parent of (3, 1) is (2, 2)
       the parent of (2, 2) is of course None
    @type in_path: bool
       True if and only if the node belongs to the path plotted by A-star
       path search
       in the example above, in_path is True for nodes with coordinates
       (2, 2), (3,1), (3, 0)
       and False for all other nodes
    @type gcost: float
       gcost of the node, as described in the handout
       initially, we set it to the largest possible float
    @type hcost: float
       hcost of the node, as described in the handout
       initially, we set it to the largest possible float
    """
    def __init__(self, navigable, grid_x, grid_y):
        """
        Initialize a new node

        @type self: Node
        @type navigable: bool
        @type grid_x: int
        @type grid_y: int
        @rtype: None

        Preconditions: grid_x, grid_y are non-negative

        >>> n = Node(True, 2, 3)
        >>> n.grid_x
        2
        >>> n.grid_y
        3
        >>> n.navigable
        True
        """
        self.navigable = navigable
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.in_path = False
        self.parent = None
        self.gcost = sys.float_info.max
        self.hcost = sys.float_info.max

    def set_gcost(self, gcost):
        """
        Set gcost to a given value

        @type gcost: float
        @rtype: None

        Precondition: gcost is non-negative

        >>> n = Node(True, 1, 2)
        >>> n.set_gcost(12.0)
        >>> n.gcost
        12.0
        """
        self.gcost = gcost

    def set_hcost(self, hcost):
        """
        Set hcost to a given value

        @type hcost: float
        @rtype: None

        Precondition: gcost is non-negative

        >>> n = Node(True, 1, 2)
        >>> n.set_hcost(12.0)
        >>> n.hcost
        12.0
        """
        self.hcost = hcost

    def fcost(self):
        """
        Compute the fcost of this node according to the handout

        @type self: Node
        @rtype: float
        """
        return self.gcost + self.hcost

    def set_parent(self, parent):
        """
        Set the parent to self
        @type self: Node
        @type parent: Node
        @rtype: None
        """
        self.parent = parent

    def distance(self, other):
        """
        Compute the distance from self to other
        @self: Node
        @other: Node
        @rtype: int
        """
        dstx = abs(self.grid_x - other.grid_x)
        dsty = abs(self.grid_y - other.grid_y)
        if dstx > dsty:
            return 14 * dsty + 10 * (dstx - dsty)
        return 14 * dstx + 10 * (dsty - dstx)

    def __eq__(self, other):
        """
        Return True if self equals other, and false otherwise.

        @type self: Node
        @type other: Node
        @rtype: bool
        >>> a = Node(True, 1, 2)
        >>> b = Node(True, 1, 2)
        >>> a == b
        True
        >>> c = Node(False, 0, 2)
        >>> a == c
        False
        """

        return (self.navigable == other.navigable) and \
               (self.grid_x == other.grid_x) and (self.grid_y == other.grid_y)

    def __lt__(self, other):
        """
        Return True if self less than other, and false otherwise.

        @type self: Node
        @type other: Node
        @rtype: bool
        """
        # TODO
        return self.fcost() < other.fcost()

    def __str__(self):
        """
        Return a string representation.

        @type self: Node
        @rtype: str
        >>> a = Node(True, 1, 2)
        >>> b = Node(False, 5, 6)
        >>> print(a)
        .
        >>> print(b)
        +
        """
        if self.navigable is True:
            return "."
        return "+"


class Grid:
    """
    Represents the world where the action of the game takes place.
    You may define helper methods as you see fit.

    === Attributes: ===
    @type width: int
       represents the width of the game map in characters
       the x-coordinate runs along width
       the leftmost node has x-coordinate zero
    @type height: int
       represents the height of the game map in lines
       the y-coordinate runs along height; the topmost
       line contains nodes with y-coordinate 0
    @type map: List[List[Node]]
       map[x][y] is a Node with x-coordinate equal to x
       running from 0 to width-1
       and y-coordinate running from 0 to height-1
    @type treasure: Node
       a navigable node in the map, the location of the treasure
    @type boat: Node
       a navigable node in the map, the current location of the boat

    === Representation invariants ===
    - width and height are positive integers
    - map has dimensions width, height
    """

    def __init__(self, file_path, text_grid=None):
        """
        If text_grid is None, initialize a new Grid assuming file_path
        contains pathname to a text file with the following format:
        ..+..++
        ++.B..+
        .....++
        ++.....
        .T....+
        where a dot indicates a navigable Node, a plus indicates a
        non-navigable Node, B indicates the boat, and T the treasure.
        The width of this grid is 7 and height is 5.
        If text_grid is not None, it should be a list of strings
        representing a Grid. One string element of the list represents
        one row of the Grid. For example the grid above, should be
        stored in text_grid as follows:
        ["..+..++", "++.B..+", ".....++", "++.....", ".T....+"]

        @type file_path: str
           - a file pathname. See the above for the file format.
           - it should be ignored if text_grid is not None.
           - the file specified by file_path should exists, so there
             is no need for error handling
           Please call open_grid to open the file
        @type text_grid: List[str]
        @rtype: None

        >>> b = Grid("", ["+..T", ".+..", "B..+"])
        >>> b.width == 4
        True
        >>> b.height == 3
        True
        >>> b.map == [[Node(False, 0, 0), Node(True, 0, 1), Node(True, 0, 2)], \
        [Node(True, 1, 0), Node(False, 1, 1), Node(True, 1, 2)], \
        [Node(True, 2, 0), Node(True, 2, 1), Node(True, 2, 2)], \
        [Node(True, 3, 0), Node(True, 3, 1), Node(False, 3, 2)]]
        True
        >>> b.boat == Node(True, 0, 2)
        True
        >>> b.treasure == Node(True, 3, 0)
        True

        >>> c = Grid('',['+..T', '.+..', 'B..+'])
        >>> c.width == 4
        True
        >>> c.height == 3
        True
        >>> c.map == [[Node(False, 0, 0,), Node(True, 0, 1), Node(True, 0, 2)],\
         [Node(True, 1, 0), Node(False, 1, 1), Node(True, 1, 2)], \
         [Node(True, 2, 0), Node(True, 2, 1), Node(True, 2, 2)], \
         [Node(True, 3, 0), Node(True, 3, 1), Node(False, 3, 2)]]
        True
        """

        if text_grid is None:
            # Turn it into the same format as when text_grid is a list
            self.grid = [new_line.strip() for new_line in
                         Grid.open_grid(file_path).readlines()]
            self._map_creator(self.grid)

        else:
            self._map_creator(text_grid)

    def _map_creator(self, text_grid):
        """ Create the grid

        @type self: Grid
        @type text_grid: List[str]

        >>> c = Grid('',['+..T', '.+..', 'B..+'])
        >>> c.map == [[Node(False, 0, 0,), Node(True, 0, 1), Node(True, 0, 2)],\
         [Node(True, 1, 0), Node(False, 1, 1), Node(True, 1, 2)], \
         [Node(True, 2, 0), Node(True, 2, 1), Node(True, 2, 2)], \
         [Node(True, 3, 0), Node(True, 3, 1), Node(False, 3, 2)]]
        True
        """

        spread = []
        map_ = []
        self.width = len(text_grid[0])
        self.height = len(text_grid)
        for row in range(len(text_grid)):
            for node in range(len(text_grid[row])):
                spread.append(text_grid[row][node])
        for i in range(self.width):
            map_.append(spread[i::self.width])
        for column in range(len(map_)):
            for node in range(len(map_[column])):
                nav = False
                if map_[column][node] in [".", "B", "T"]:
                    nav = True
                if map_[column][node] == "T":
                    self.treasure = Node(nav, column, node)
                elif map_[column][node] == "B":
                    self.boat = Node(nav, column, node)
                map_[column][node] = Node(nav, column, node)
        self.map = map_

    @classmethod
    def open_grid(cls, file_path):
        """
        @rtype TextIOWrapper:
        """
        return open(file_path)

    def __str__(self):
        """
        Return a string representation.

        @type self: Grid
        @rtype: str

        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> print(g)
        B.++
        .+..
        ...T
        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> print(g)
        B.++
        .+..
        ...T
        >>> g = Grid("", ["B.....", "+++++.", ".+++.+", "+.++..", "..+...", \
        "..+..T"])
        >>> print(g)
        B.....
        +++++.
        .+++.+
        +.++..
        ..+...
        ..+..T

        >>> f = Grid("", ["..+..++", "++.B..+", ".....++", "++.....", \
        ".T....+"])
        >>> print(f)
        ..+..++
        ++.B..+
        .....++
        ++.....
        .T....+
        """

        final_grid = ""
        grid = self._list_to_grid(self._map_to_list(self.map))

        for i in range(len(grid)):
            final_grid += grid[i] + "\n"
        return final_grid[:len(final_grid)-1]

    def _map_to_list(self, map_):
        """Takes the current map and turns it into a list of nodes.

        @type self: Grid
        @type map: List[List[Node]]
        @rtype: List[str]

        >>> a = Grid("", ["B.++", ".+..", "...T"])
        >>> a._map_to_list(a.map)
        ['B', '.', '.', '.', '+', '.', '+', '.', '.', '+', '.', 'T']
        >>> f = Grid("", ["..+T", "+++.", "B..."])
        >>> f._map_to_list(f.map)
        ['.', '+', 'B', '.', '+', '.', '+', '+', '.', 'T', '.', '.']
        """

        lst = []

        if isinstance(map_, Node):
            if map_.navigable is True:
                if map_ == self.boat:
                    return "B"
                elif map_ == self.treasure:
                    return "T"
                elif map_.in_path is True:
                    return "*"
                else:
                    return "."
            else:
                return "+"
        else:
            for i in map_:
                lst.extend(self._map_to_list(i))
        return lst

    def _list_to_grid(self, lst):
        """Takes list created by _map_to_list and turns it into a grid

        @type self: Grid
        @type lst: list[str]
        @rtype: list[str]

        >>> a = Grid("", ["B.++", ".+..", "...T"])
        >>> new_list = a._map_to_list(a.map)
        >>> a._list_to_grid(new_list)
        ['B.++', '.+..', '...T']
        >>> g = Grid("", ["B.....", "+++++.", ".+++.+", "+.++..", "..+...", \
        "..+..T"])
        >>> new = g._map_to_list(g.map)
        >>> g._list_to_grid(new)
        ['B.....', '+++++.', '.+++.+', '+.++..', '..+...', '..+..T']
        >>> f = Grid("", ["..+..++", "++.B..+", ".....++", "++.....",".T....+"])
        >>> new = f._map_to_list(f.map)
        >>> f._list_to_grid(new)
        ['..+..++', '++.B..+', '.....++', '++.....', '.T....+']
        """

        final = []
        currated = []
        for i in range(self.height):
            currated.extend(lst[i::self.height])
        while len(currated) >= self.width:
            final.append(currated[:self.width])
            currated = currated[self.width:]
        return[''.join(row) for row in final]

    def move(self, direction):
        """
        Move the boat in a specific direction, if the node
        corresponding to the direction is navigable
        Else do nothing

        @type self: Grid
        @type direction: str
        @rtype: None

        direction may be one of the following:
        N, S, E, W, NW, NE, SW, SE
        (north, south, ...)
        123
        4B5
        678
        1=NW, 2=N, 3=NE, 4=W, 5=E, 6=SW, 7=S, 8=SE
        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> g.move("S")
        >>> print(g)
        ..++
        B+..
        ...T
        >>> g.move("SE")
        >>> print(g)
        ..++
        .+..
        .B.T
        >>> g.move("N")
        >>> print(g)
        ..++
        .+..
        .B.T
        """

        compass = {"NW": (-1, -1), "N": (0, -1), "NE": (1, -1), "W": (-1, 0),
                   "SW": (-1, 1), "S": (0, 1), "SE": (1, 1), "E": (1, 0)}
        if direction in compass:
            for i in range(len(self.map)):
                if Node(True, self.boat.grid_x + compass[direction][0], self.
                        boat.grid_y + compass[direction][1]) in self.map[i]:
                    self.boat.grid_x += compass[direction][0]
                    self.boat.grid_y += compass[direction][1]
                    break

    def _get_neighbors(self, node):
        """Find all the neighbors of the node

        @type self: Grid
        @type node: Node
        @rtype: List[]

        # [print(i) for i in g.get_neighbors(g.boat)]
            The node at 1, 0 is True.
            The node at 0, 1 is True.
            [None, None]

        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> isinstance(g._get_neighbors(Node(True, 1, 0)), list)
        True
        """

        compass = {"NW": (-1, -1), "N": (0, -1), "NE": (1, -1), "W": (-1, 0),
                   "SW": (-1, 1), "S": (0, 1), "SE": (1, 1), "E": (1, 0)}
        navigable_neighbors = []

        for point in compass:
            neighbor = Node(True, node.grid_x + compass[point][0], node.grid_y
                            + compass[point][1])

            for i in range(len(self.map)):
                if neighbor in self.map[i]:
                    navigable_neighbors.append(neighbor)
        return navigable_neighbors

    def find_path(self, start_node, target_node):
        """
        Implement the A-star path search algorithm
        If you will add a new node to the path, don't forget to set the parent.
        You can find an example in the docstring of Node class
        Please note the shortest path between two nodes may not be unique.
        However all of them have same length!

        @type self: Grid
        @type start_node: Node
           The starting node of the path
        @type target_node: Node
           The target node of the path
        @rtype: None

        >>> g = Grid("",["B.....", "+++++.", ".+++.+", "+.++..", "..+...", \
        "..+..T"])
        >>> g.find_path(g.boat, g.treasure)
        """

        def less_than(a, b):
            """Return if a is less than b.

            >>> less_than(1, 2)
            True
            """
            return a < b

        opened = PriorityQueue(less_than)
        closed = []

        if opened.is_empty():
            start_node.set_gcost(0)
            start_node.set_hcost(start_node.distance(target_node))
            start_node.set_parent(None)
            opened.add(start_node)

        while not opened.is_empty():

            current = opened.remove()
            closed.append(current)

            if current == target_node:
                break
            neighbors = self._get_neighbors(current)
            for neighbor in range(len(neighbors)):
                # Check if the neighbor you are viewing is in the closed list
                # If it is go to the next neighbor (go back to for loop above)
                # Otherwise, keep going

                if neighbors[neighbor] not in closed:
                        # If the hcost from the neighbor to the target is
                            # less than the distance from the current to target
                            # or the neighbor is not in the opened list

                    if neighbors[neighbor].distance(target_node) < \
                            current.distance(target_node) or \
                            neighbors[neighbor] not in opened:
                        # Set the gcost

                        if current.parent is not None:
                            neighbors[neighbor].set_gcost(neighbors[neighbor].
                                                          distance(current) +
                                                          current.parent.gcost)
                        else:
                            neighbors[neighbor].set_gcost(neighbors[neighbor].
                                                          distance(current))

                        # Set the hcost
                        neighbors[neighbor].set_hcost(neighbors[neighbor].
                                                      distance(target_node))
                        # Set the parent
                        neighbors[neighbor].set_parent(current)
                        if neighbors[neighbor] not in opened:
                            opened.add(neighbors[neighbor])
        # Use the nodes in the closed list to find the nodes in the map and
        # set their parents to access them LATER
        closed = closed[::-1]

        for node in range(len(closed)):
            for i in range(len(self.map)):
                if closed[node] in self.map[i]:
                    node_index = self.map[i].index(closed[node])
                    self.map[i][node_index].set_parent(closed[node].parent)

    def retrace_path(self, start_node, target_node):
        """
        Return a list of Nodes, starting from start_node,
        ending at target_node, tracing the parent
        Namely, start from target_node, and add its parent
        to the list. Keep going until you reach the start_node.
        If the chain breaks before reaching the start_node,
        return and empty list.

        @type self: Grid
        @type start_node: Node
        @type target_node: Node
        @rtype: list[Node]

        >>> g = Grid("", ["B.....", "+++++.", ".+++.+", "+.++..", "..+...", \
        "..+..T"])
        >>> isinstance(g.retrace_path(g.boat, g.treasure), list)
        True
        >>> b = Grid("", ["B+++", "++..", "...T"])
        >>> b.retrace_path(b.boat, b.treasure)
        []
        >>> a = Grid("", ["..+..++", "++.B..+", ".....++", "++.....", \
        ".T....+"])
        >>> len(a.retrace_path(a.boat, a.treasure)) == 4
        True
        """

        final = []
        start_flag = False
        flag = False
        self.find_path(start_node, target_node)

        for col in range(len(self.map)):
            if start_node in self.map[col]:
                start_flag = True
            if target_node in self.map[col]:
                flag = True

        if start_flag and flag:
            for col in range(len(self.map)):
                for node in range(len(self.map[col])):
                    if self.map[col][node] == target_node:
                        i = self.map[col][node]
                        while i is not None:
                            final.append(i)
                            i = i.parent
        final = final[::-1]
        if start_node in final and target_node in final:
            # Set in_path to true for all values in the list
            for node in range(len(final)):
                for i in range(len(self.map)):
                    if final[node] in self.map[i]:
                        node_index = self.map[i].index(final[node])
                        self.map[i][node_index].in_path = True
            return final
        return []

    def get_treasure(self, s_range):
        """
        Return treasure node if it is located at a distance s_range or
        less from the boat, else return None
        @type s_range: int
        @rtype: Node, None

        >>> test = Grid("", ["B.++", ".+..", "...T"])
        >>> test.get_treasure(10) is None
        True
        >>> test.get_treasure(50) == test.treasure
        True
        """
        if self.boat.distance(self.treasure) <= s_range:
            return self.treasure
        return None

    def plot_path(self, start_node, target_node):
        """
        Return a string representation of the grid map,
        plotting the shortest path from start_node to target_node
        computed by find_path using "*" characters to show the path
        @type self: Grid
        @type start_node: Node
        @type target_node: Node
        @rtype: str
        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> isinstance(g.plot_path(g.boat, g.treasure), str)
        True
        >>> print(g.plot_path(g.boat, g.treasure))
        B*++
        .+*.
        ...T
        """

        self.retrace_path(start_node, target_node)
        return str(self)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config='pylintrc.txt')
