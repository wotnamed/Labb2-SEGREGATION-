import tkinter as tk
import random
import time
import math


class Actor:
    def __init__(self, color):  # upon initialisation
        self.color = color  # class colour (determines what other actors it will be "satisfied" with.
        self.is_satisfied = False   # the attribute that determines whether the actor will be attempted to move or not


class NeighboursApp: # the container for the program (most variables and functions are declared here)
    def __init__(self, root):   # upon initialising an instance
        # Canvas dimensions and margin
        self.width = 500  # window width
        self.height = 500  # window height
        self.margin = 50  # margin for window width and height
        self.dot_size = 0  # This doesn't do shit (can be removed)
        self.interval = 0.5  # The interval used between each operation in seconds (ie 2 means a delay of 2 seconds)

        # Initialize tkinter canvas
        self.root = root
        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.pack()

        # Initialize world
        self.world = []  # create first list for world (will be matrix later)
        self.init_world()
        self.last_update_time = time.time()

        # Start animationNeighbours.py
        self.update_world()
        self.root.after(int(self.interval * 1000), self.animate)

        # init an empty world

    def init_world(self):
        dist = [0.25, 0.25, 0.5]  # the distribution of each colour declared below (the weights used in random.choices)
        possible = ["Red", "Blue", None]  # The possible colours for an agent. None means blank space.
        n_locations = 25000  # This determines the numbers of "locations" with in the matrix. It should be a product of a^2 where a is a whole number and not below zero.
        y = int(n_locations**0.5)  # y height equals sqrt number of locations
        x = int(n_locations**0.5)  # x width equals sqrt number of locations (the grid becomes a square)
        for i in range(y):
            self.world.append([])
        for i in self.world:
            for i in range(x):  # for every row in matrix
                value = random.choices(possible, dist)[0]  # Determines whether the item that is about to be assigned is an actor or not and what colour that actor obtains.
                if value is not None:  # If the item is an actor
                    self.world[i].append(Actor(value))  # Append the actor to the matrix
                else:  # If the item is not an actor
                    self.world[i].append(None)  # Append None
        # coordinates: list[y][x]

        self.fix_screen_size(n_locations) # Adjust screen size based on the number of locations

    def test_neighbours(self, row_number, column_number):
        subject = self.world[row_number][column_number].color
        total_rows = len(self.world)
        total_columns = len(self.world[0])
        check_range = [-1, 0, 1]  # Difference between actor coordinate.

        total_neighbours = 0
        bad_neighbours = 0

        for diff_y in check_range:  # Check the actors around the actor in question
            for diff_x in check_range:
                if diff_y == 0 and diff_x == 0:
                    continue
                neighbour_row = row_number + diff_y
                neighbour_col = column_number + diff_x

                if 0 <= neighbour_row < total_rows and 0 <= neighbour_col < total_columns:
                    neighbour = self.world[neighbour_row][neighbour_col]
                    total_neighbours += 1
                    if neighbour is not None and neighbour.color != subject:  # Self-explanatory
                        bad_neighbours += 1

        return 1-(bad_neighbours/total_neighbours)  # The function returns the percentage of all neighbours that are "bad" ie not the same colour as the actor.

    def find_unhappy_actors(self, threshold, unhappy):  # Find all unhappy actors and append them to the "unhappy" list.
        for row in range(len(self.world)):
            for col in range(len(self.world[row])):
                if self.world[row][col] is None:
                    continue
                satisfaction = self.test_neighbours(row, col)
                if satisfaction < threshold:
                    unhappy.append((row,col))

    def remove_and_redistribute_actors(self, unhappy, size):
        for row, col in unhappy:  # For every unhappy actor in the list
            actor = self.world[row][col]  # Bookmark the unhappy actor
            self.world[row][col] = None  # Remove actor from current location
            # Find a new empty location
            while True:
                new_row = random.randint(0, size - 1)
                new_col = random.randint(0, size - 1)
                if self.world[new_row][new_col] is None:  # Found an empty spot
                    self.world[new_row][new_col] = actor
                    # print(f'({row}, {col}) with satisfaction {satisfaction} moved to ({new_row},{new_col})')  # No longer used
                    break


    def update_world(self):
        threshold = 0.8
        size = len(self.world)
        unhappy = []
        self.find_unhappy_actors(threshold, unhappy)
        self.remove_and_redistribute_actors(unhappy, size)


    def is_valid_location(self, size, row, col):
        return 0 <= row < size and 0 <= col < size

    

# ============================ YOU DON'T HAVE TO CARE ABOUT THE CODE BELOW IN THE ORIGINAL VERSION, ONLY USED FOR DRAWING ============================
    def fix_screen_size(self, n_locations):
        self.dot_size = 10000 / n_locations
        if self.dot_size < 1:
            self.dot_size = 2
        self.width = math.sqrt(n_locations) * self.dot_size + 2 * self.margin
        self.height = self.width

    # Will draw the world
    def render_world(self):
        self.canvas.delete("all")  # Clear the canvas
        size = len(self.world)
        for row in range(size):
            for col in range(size):
                x = int(self.dot_size * col + self.margin)
                y = int(self.dot_size * row + self.margin)
                if self.world[row][col] is not None:
                    color = self.world[row][col].color
                    self.canvas.create_oval(x, y, x + self.dot_size, y + self.dot_size, fill=color)

    def animate(self):
        current_time = time.time()
        if current_time - self.last_update_time >= self.interval:
            self.update_world()
            self.render_world()
            self.last_update_time = current_time
        self.root.after(int(self.interval * 1000), self.animate)


def main():
    root = tk.Tk()
    app = NeighboursApp(root)
    root.title("Segregation Simulation")
    root.mainloop()


if __name__ == "__main__":
    main()