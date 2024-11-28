import tkinter as tk
import random
import time
import math


class Actor:
    def __init__(self, color):
        self.color = color
        self.is_satisfied = False


class NeighboursApp:
    def __init__(self, root):
        # Canvas dimensions and margin
        self.width = 500
        self.height = 500
        self.margin = 50
        self.dot_size = 0
        self.interval = 0.5  # in seconds

        # Initialize tkinter canvas
        self.root = root
        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.pack()

        # Initialize world
        self.world = []
        self.init_world()
        self.last_update_time = time.time()

        # Start animationNeighbours.py
        self.update_world()
        self.root.after(int(self.interval * 1000), self.animate)

        # init an empty world

    def init_world(self):
        # Distribution percentages for RED, BLUE, and NONE
        dist = [0.25, 0.25, 0.5]
        possible = ["Red", "Blue", None]
        n_locations = 25000 # Number of locations (should be a square and also work for 25000)
        y = int(n_locations**0.5)
        x = int(n_locations**0.5)
        for i in range(y):
            self.world.append([])
        for i in self.world:
            for i in range(x):
                value = random.choices(possible, dist)[0]
                if value is not None:
                    self.world[i].append(Actor(value))
                else:
                    self.world[i].append(None)


        # coordinates: list[y][x]

        # Adjust screen size based on the number of locations
        self.fix_screen_size(n_locations)

    def test_neighbours(self, row_number, column_number):
        subject = self.world[row_number][column_number].color
        total_rows = len(self.world)
        total_columns = len(self.world[0])
        check_range = [-1, 0, 1]

        total_neighbours = 0
        bad_neighbours = 0

        for diff_y in check_range:
            for diff_x in check_range:
                if diff_y == 0 and diff_x == 0:
                    continue
                neighbour_row = row_number + diff_y
                neighbour_col = column_number + diff_x

                if 0 <= neighbour_row < total_rows and 0 <= neighbour_col < total_columns:
                    neighbour = self.world[neighbour_row][neighbour_col]
                    total_neighbours += 1
                    if neighbour is not None and neighbour.color != subject:
                        bad_neighbours += 1

        return 1-(bad_neighbours/total_neighbours)
    def find_unhappy_actors(self, threshold, unhappy):
        for row in range(len(self.world)):
            for col in range(len(self.world[row])):
                if self.world[row][col] is None:
                    continue
                satisfaction = self.test_neighbours(row, col)
                if satisfaction < threshold:
                    unhappy.append((row,col))

    def remove_and_redistribute_actors(self, unhappy, size):
        for row, col in unhappy:
            actor = self.world[row][col]
            self.world[row][col] = None  # Remove actor from current location
            # Find a new empty location
            while True:
                new_row = random.randint(0, size - 1)
                new_col = random.randint(0, size - 1)
                if self.world[new_row][new_col] is None:  # Found an empty spot
                    self.world[new_row][new_col] = actor
                    # print(f'({row}, {col}) with satisfaction {satisfaction} moved to ({new_row},{new_col})')
                    break


    def update_world(self):
        threshold = 0.8
        size = len(self.world)
        unhappy = []
        satisfaction = 0
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