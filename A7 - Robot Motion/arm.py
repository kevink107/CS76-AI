"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

import cs1lib
import time
import math


class ArmVisualizer:
    def __init__(self, width, height, arm_lengths, obstacles, init_config):
        self.width = width
        self.height = height
        self.arm = arm_lengths
        self.obstacles = obstacles
        # Adjust the ratio if the arm or obstacles are too large or too small
        self.ratio = 20
        self.init_config = init_config
        self.sequence = []  # To store the sequence of configurations
        self.current_index = 0  # Index of the current configuration
        self.last_update_time = None  # Time when the last configuration was updated

        # Set the graphics window size to be large enough to display the full arm and obstacles
        max_arm_length = sum(self.arm)
        self.window_width = max(self.width, max_arm_length) * self.ratio
        self.window_height = max(self.height, max_arm_length) * self.ratio

    def start_graphics(self):
        # Start the cs1lib graphics loop with appropriate window size
        cs1lib.start_graphics(self.draw_all, width=self.window_width, height=self.window_height, framerate=30)

    def coord_to_pix(self, y):
        # Converts y coordinate to pixel coordinate on the screen
        return self.height * self.ratio - y * self.ratio

    def config_to_coord(self, config):
        # Converts arm configuration (list of angles) to list of endpoint coordinates
        points = [[0, 0]]
        for i, length in enumerate(self.arm):
            angle = math.radians(config[i])
            new_point = [points[-1][0] + length * math.cos(angle),
                         points[-1][1] + length * math.sin(angle)]
            points.append(new_point)
        return points

    def draw_arm(self, points):
        # Draws the arm based on the list of endpoint coordinates
        cs1lib.set_stroke_color(0, 0, 1)  # Blue color for robot arm
        for i in range(1, len(points)):
            cs1lib.draw_line(points[i - 1][0] * self.ratio,
                             self.coord_to_pix(points[i - 1][1]),
                             points[i][0] * self.ratio,
                             self.coord_to_pix(points[i][1]))

    def draw_obstacles(self):
        # Draws rectangular obstacles based on the list of obstacle coordinates
        cs1lib.set_fill_color(1, 0, 0)  # Red color for obstacles
        for obstacle in self.obstacles:
            bl_point = obstacle[0]  # Bottom-left point
            tr_point = obstacle[1]  # Top-right point
            cs1lib.draw_rectangle(bl_point[0] * self.ratio,
                                  self.coord_to_pix(tr_point[1]),
                                  (tr_point[0] - bl_point[0]) * self.ratio,
                                  (bl_point[1] - tr_point[1]) * self.ratio)

    def draw_all(self):
        # Clears the window and draws the current arm configuration and obstacles
        cs1lib.clear()
        if not self.sequence:  # If the sequence is empty, just draw the initial configuration
            self.draw_arm(self.config_to_coord(self.init_config))
        else:
            # Check if it's time to update to the next configuration
            current_time = time.time()
            if self.last_update_time is None or (current_time - self.last_update_time) >= 2:
                self.last_update_time = current_time
                self.init_config = self.sequence[self.current_index]
                self.current_index = (self.current_index + 1) % len(self.sequence)

            self.draw_arm(self.config_to_coord(self.init_config))
        self.draw_obstacles()

    def simulate_path(self, sequence):
        # Stores the sequence of configurations and starts the graphics loop
        self.sequence = sequence
        self.current_index = 0
        self.last_update_time = None
        cs1lib.start_graphics(self.draw_all, framerate=30)
