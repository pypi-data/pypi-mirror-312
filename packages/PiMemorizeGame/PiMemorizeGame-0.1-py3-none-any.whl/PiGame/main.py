
"""
Main entry point for the PiGame application.

This module defines the main application logic and entry point for the PiGame.
It includes the main game loop and logic for handling user interactions across different game screens.
"""

import math
import sys
import pygame as pg
import pygame_gui
import time
from PiGame.helpers import Helpers


class PiGame:
    """
        A class used to manage the PiGame application, handling user interactions, game modes,
        and the graphical interface for learning, training, and challenge modes.

        Attributes
        ----------
        screen : pygame.Surface
            The primary display surface for the game.
        clock : pygame.time.Clock
            Manages the timing and frame rate of the game loop.
        manager : pygame_gui.UIManager
            Handles GUI elements in the game.
        fonts : dict
            A dictionary of fonts categorized by their name and size.
        images : dict
            A dictionary of preloaded images used in the game.
        user_input : list
            A list of digits entered by the user during training and challenge modes.
        keys_layout : int
            Determines the layout of the on-screen keyboard (0 or 1).
        switch_position : int
            Tracks the position of the hint switch (on or off).
        hint_counter : int
            Specifies the delay (in seconds) before a hint is displayed.
        mistakes_allowed_counter : int
            Counts the number of mistakes the user can make in challenge mode.
        goal_reached : bool
            Indicates whether the user has reached their goal in challenge mode.
        game_over : bool
            Indicates whether the game is over due to mistakes or time limits.
        page_number_counter : int
            Tracks the current page number in the learning screen.
        start_digit_counter : int
            Tracks the starting digit index in training and challenge modes.
        goal_digit_counter : int
            Specifies the target number of digits to guess in challenge mode.
        thinking_time_counter : int
            Sets the time limit for thinking during the challenge.
        digits_on_page_counter : int
            Specifies the number of digits displayed on the current page in learning mode.
        digit_counter : int
            Tracks the number of correct digits entered by the user.
        guessing_rect : pygame.Rect
            Represents the rectangular area for displaying user guesses in training and challenge modes.

        Methods
        -------
        __init__()
            Initializes the game by setting up the display, fonts, and main screen.
        setup_display()
            Configures the game display for full-screen mode and retrieves screen dimensions.
        setup_fonts()
            Initializes a dictionary of fonts to be used across different screens and UI elements.
        main_values()
            Initializes key game variables such as counters, multipliers, and screen-specific settings.
        images_initialization()
            Preloads required images and scales them to appropriate dimensions for display.
        scale_images()
            Scales loaded images based on the screen dimensions and predefined scaling parameters.
        main_screen()
            Displays the main menu screen and handles navigation to other game screens.
        main_screen_objects()
            Initializes all buttons and graphical elements for the main menu screen.
        learning_screen()
            Manages the learning mode, including digit visualization and navigation through pages.
        learning_screen_objects()
            Creates and positions graphical elements specific to the learning screen.
        draw_learning_pi_digits()
            Handles the drawing of digits in the learning mode, including pagination.
        learning_screen_logic()
            Computes and updates the spacing of rows and columns on the learning screen.
        training_screen()
            Manages the training mode, including digit input and feedback for the user.
        training_screen_objects()
            Initializes graphical elements specific to the training screen.
        guessing_rect_drawing()
            Displays user input and feedback in the guessing area during training and challenge modes.
        challenge_screen()
            Manages the challenge mode, including score calculation, hints, and game-over logic.
        challenge_screen_objects()
            Initializes graphical elements specific to the challenge mode.
        challenge_screen_settings()
            Handles the settings screen for the challenge mode.
        challenge_screen_settings_objects()
            Creates and positions UI elements for configuring challenge settings.
        training_screen_settings()
            Handles the settings screen for the training mode.
        training_screen_settings_objects()
            Creates and positions UI elements for configuring training settings.
        nickname_screen()
            Prompts the user to enter a nickname before saving their high score.
        calculate_score(digits_inserted, avg_thinking_time, time_for_thinking, total_time, mistakes_made, mistakes_allowed)
            Calculates the user's score based on performance in challenge mode.
        highscores_screen()
            Displays the highscores table and allows the user to return to the main menu.
        highscores_screen_objects()
            Initializes graphical elements for the highscores screen.
        draw_hearts()
            Displays remaining mistakes as hearts during the challenge mode.
        keys_initialization()
            Initializes the on-screen keyboard layout for training and challenge modes.
        compare_digits(user_input)
            Compares the user's input with the correct digits and provides feedback.

        Raises
        ------
        FileNotFoundError
            If the required image or highscores file is not found.
        ValueError
            If invalid parameters are passed to certain methods, such as invalid digit counters.

        """

    def __init__(self):
        pg.init()
        self.setup_display()
        self.clock = pg.time.Clock()
        self.setup_fonts()
        self.main_values()
        self.images_initialization()

        # GUI manager initialization
        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height))

        # Helpers class initialization
        self.helpers = Helpers(self.screen, self.fonts, self.images)

        # Main_screen initialization
        self.main_screen()

    def setup_display(self):
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        screen_info = pg.display.Info()
        self.screen_width, self.screen_height = screen_info.current_w, screen_info.current_h

    def setup_fonts(self):
        pg.font.init()
        sizes = range(10, 151)  # All sizes from 10 to 150
        font_names = ['candara', 'calibri', 'cambria']
        self.fonts = {name: {size: pg.font.SysFont(name, size) for size in sizes} for name in font_names}

    def main_values(self):
        # Learning screen counters
        self.digits_in_columns_counter = 5

        self.page_change_multipliers = [1, 2, 5, 10, 100]
        self.page_change_multiplier_counter = 1

        self.page_number_counter = 1

        self.digits_on_page_counter_bottom = 1
        self.digits_on_page_counter_top = 1
        self.digits_on_page_counter = 0

        # Screens settings counters ( training and challenge )
        self.digit_multipliers = [1, 10, 50, 100, 1000]
        self.digit_multiplier_counter = 1
        self.start_digit_counter = 1

        self.thinking_time_counter = 5
        self.mistakes_allowed_counter = 3

        # Training screen
        self.digits_display_offset = None
        self.switch_position = 1
        self.keys_layout = 1
        self.digit_counter = 1
        self.hint_counter = 4

        # Goal counters
        self.goal_digit_counter = 25

        self.goal_digit_multipliers = [25, 50, 100, 250, 500]
        self.goal_digit_multiplier_counter = 25

        self.goal_reached = False
        self.game_over = False
        self.user_input = []

    def images_initialization(self):
        self.images = {}
        image_files = ['minus', 'plus', 'switch_on', 'switch_off', 'switch_neutral', 'heart', 'logo']
        for img in image_files:
            self.images[img] = pg.image.load(f'PiGame/images/{img}.png')

        # Images aliases
        self.images['t_s_minus'] = self.images['minus']
        self.images['t_s_plus'] = self.images['plus']

        self.scale_images()

    def scale_images(self):
        # Scaling parameters
        scaling_parameters = {
            'logo': (0.23, 0.1),
            'minus': (0.035, 0.035),
            'plus': (0.035, 0.035),
            't_s_minus': (0.06, 0.06),
            't_s_plus': (0.06, 0.06),
            'switch_on': (0.06, 0.03),
            'switch_off': (0.06, 0.03),
            'switch_neutral': (0.06, 0.03),
            'heart': (0.038, 0.034),
        }

        for key, (width_factor, height_factor) in scaling_parameters.items():
            if key in self.images:  # Checking if the key exist
                self.images[key] = pg.transform.scale(
                    self.images[key], (int(self.screen_width * width_factor), int(self.screen_width * height_factor))
                )
            else:
                print(f"Warning: Missing key '{key}' in images.")

    def draw_learning_pi_digits(self):
        # Logic and starting parameters
        self.learning_screen_logic()
        max_digits = 1000000
        if self.digits_on_page_counter == 0:
            max_page_number = 1000
        else:
            max_page_number = math.ceil(max_digits / self.digits_on_page_counter)

        # Load the pi digits except "3."
        pi_digits = self.helpers.read_pi_digits()[2:]

        # Setting the bottom digit range on the page
        self.digits_on_page_counter_bottom = 1 + (self.page_number_counter - 1) * self.digits_on_page_counter

        # Limitation of numbers to the millionth place
        if self.page_number_counter >= max_page_number:
            self.digits_on_page_counter_bottom = max_digits - self.digits_on_page_counter
            self.digits_on_page_counter_top = max_digits  # Locking the top limit to 1 million
            self.page_number_counter = max_page_number

        # Decimation of `pi_digits` based on page count
        if self.page_number_counter > 1:
            pi_digits = pi_digits[(self.page_number_counter - 1) * self.digits_on_page_counter:]

        # Drawing positions resetting
        x, y = self.columns_spacing, self.rows_spacing
        for i, chunk in enumerate([pi_digits[i:i + self.digits_in_columns_counter] for i in
                                   range(0, len(pi_digits), self.digits_in_columns_counter)]):
            text = self.helpers.create_text(chunk, 'calibri', int(self.screen_width/50))
            rect = text.get_rect(center=(self.digits_rect.left + x, self.digits_rect.top + y))

            # Switching to the next row and rect positioning
            if rect.right > self.digits_rect.right:
                x, y = self.columns_spacing, y + self.rows_spacing
                rect.center = (self.digits_rect.left + x, self.digits_rect.top + y)

            # Checking whether the maximum height of the digit frame has been exceeded
            if rect.bottom > self.digits_rect.bottom:
                # Number of digits on the page reading
                self.digits_on_page_counter = i * self.digits_in_columns_counter
                self.digits_on_page_counter_top = min(self.page_number_counter * self.digits_on_page_counter, max_digits)
                self.learning_screen_logic()
                break

            # Switching to the next column
            x += self.columns_spacing + rect.width
            self.screen.blit(text, rect)

        # Displaying the digit range on the page
        self.screen.blit(self.digits_on_page_counter_text, self.digits_on_page_counter_rect)

    def learning_screen_logic(self):
        self.learning_screen_objects()

        # Columns spacing logic
        columns_space_available = 0.5 * (self.digits_rect.right - self.digits_rect.left)
        single_digit_width, single_digit_height = self.fonts['calibri'][int(self.screen_width/50)].size("0")
        self.columns = int(columns_space_available/(self.digits_in_columns_counter*single_digit_width))
        self.columns_spacing = ((self.digits_rect.right - self.digits_rect.left) - (
                    self.columns * (self.digits_in_columns_counter * single_digit_width))) / (
                             self.columns + 2)  # Space between columns width

        # Rows spacing logic
        rows_space_available = 0.5 * (self.digits_rect.bottom - self.digits_rect.top)
        self.rows = int(rows_space_available / single_digit_height)
        self.rows_spacing = ((self.digits_rect.bottom - self.digits_rect.top) - (
                    self.rows * single_digit_height)) / (
                             self.rows + 1)  # Space between rows width

    def keys_initialization(self):
        self.square_1_y_pos = self.switch_keys_layout_rect.y if self.keys_layout == 0 else self.back_button_rect.y
        self.square_7_y_pos = self.back_button_rect.y if self.keys_layout == 0 else self.switch_keys_layout_rect.y

        for i in range(10):
            setattr(self, f'square_{i}_text', self.helpers.create_text(str(i), 'calibri', int(self.screen_width/26)))

        square_size = self.screen_height * 0.12
        # Initial x and y based on guessing rect
        initial_x = self.guessing_rect.centerx - self.screen_height * 0.06
        initial_y = self.back_button_rect.bottom + self.back_button_rect.height * 0.3

        positions = [
            (initial_x, initial_y),  # Square 0
            (initial_x - square_size * 0.9 - self.guessing_rect.height * 0.5, self.square_1_y_pos),  # Square 1
            (initial_x, self.square_1_y_pos),  # Square 2
            (initial_x + square_size * 0.9 + self.guessing_rect.height * 0.5, self.square_1_y_pos),  # Square 3
            (initial_x - square_size * 0.9 - self.guessing_rect.height * 0.5,
             (self.square_1_y_pos + self.square_7_y_pos) * 0.5),  # Square 4
            (initial_x, (self.square_1_y_pos + self.square_7_y_pos) * 0.5),  # Square 5
            (initial_x + square_size * 0.9 + self.guessing_rect.height * 0.5,
             (self.square_1_y_pos + self.square_7_y_pos) * 0.5),  # Square 6
            (initial_x - square_size * 0.9 - self.guessing_rect.height * 0.5, self.square_7_y_pos),  # Square 7
            (initial_x, self.square_7_y_pos),  # Square 8
            (initial_x + square_size * 0.9 + self.guessing_rect.height * 0.5, self.square_7_y_pos),  # Square 9
        ]

        for i, pos in enumerate(positions):
            setattr(self, f'square_{i}_rect', pg.Rect(pos[0], pos[1], square_size, square_size))
            square_text = getattr(self, f'square_{i}_text')
            square_rect = getattr(self, f'square_{i}_rect')

            # Fonts issue centering correction
            text_rect = square_text.get_rect(center=(square_rect.centerx, square_rect.centery + 10))
            setattr(self, f'square_{i}_text_rect', text_rect)

    # Main screen initialization
    def main_screen_objects(self):
        self.images_initialization()

        # Buttons creating using the new create_button_and_rect
        self.learning_button_text, self.learning_button_rect, self.learning_button_text_rect = self.helpers.create_button_and_rect(
            "Learning", 'cambria', int(self.screen_width/54), self.screen_width * 0.42, self.screen_height * 0.37,
                                       self.screen_width * 0.16, self.screen_height * 0.08
        )
        self.training_button_text, self.training_button_rect, self.training_button_text_rect = self.helpers.create_button_and_rect(
            "Training", 'cambria', int(self.screen_width/54), self.learning_button_rect.x,
            self.learning_button_rect.bottom + self.learning_button_rect.height * 0.2,
            self.screen_width * 0.16, self.screen_height * 0.08
        )
        self.challenge_button_text, self.challenge_button_rect, self.challenge_button_text_rect = self.helpers.create_button_and_rect(
            "Challenge", 'cambria', int(self.screen_width/54), self.training_button_rect.x,
            self.training_button_rect.bottom + self.training_button_rect.height * 0.2,
            self.screen_width * 0.16, self.screen_height * 0.08
        )
        self.highscores_button_text, self.highscores_button_rect, self.highscores_button_text_rect = self.helpers.create_button_and_rect(
            "High Scores", 'cambria', int(self.screen_width/54), self.challenge_button_rect.x,
            self.challenge_button_rect.bottom + self.challenge_button_rect.height * 0.2,
            self.screen_width * 0.16, self.screen_height * 0.08
        )
        self.quit_button_text, self.quit_button_rect, self.quit_button_text_rect = self.helpers.create_button_and_rect(
            "Quit", 'cambria', int(self.screen_width/54), self.challenge_button_rect.x,
            self.challenge_button_rect.bottom + self.challenge_button_rect.height * 1.95,
            self.screen_width * 0.16, self.screen_height * 0.08
        )

        # Game logo positioning
        self.game_logo = self.images['logo'].get_rect(
            center=(self.screen_width * 0.5, self.screen_height * 0.20)
        )

    def learning_screen_objects(self):
        self.images_initialization()

        # Main rectangle for digits initialization
        self.digits_rect = pg.Rect(self.screen_width * 0.06, self.screen_height * 0.1,
                                   self.screen_width * 0.6, self.screen_height * 0.8)

        # Texts
        self.digits_in_columns_text, self.digits_in_columns_rect = self.helpers.create_text_and_rect(
            "Digits in columns:", 'calibri', int(self.screen_width/48),
            self.digits_rect.right + (self.screen_width - self.digits_rect.right) * 0.5,
            self.digits_rect.top + 25
        )
        self.page_number_text, self.page_number_rect = self.helpers.create_text_and_rect(
            "Page number:", 'calibri', int(self.screen_width/48), self.digits_in_columns_rect.centerx,
            self.digits_in_columns_rect.bottom + self.digits_in_columns_rect.height * 3
        )
        self.page_change_multiplier_text, self.page_change_multiplier_rect = self.helpers.create_text_and_rect(
            "Page change multiplier:", 'calibri', int(self.screen_width/48), self.digits_in_columns_rect.centerx,
            self.page_number_rect.bottom + self.digits_in_columns_rect.height * 3
        )
        self.digits_on_page_text, self.digits_on_page_rect = self.helpers.create_text_and_rect(
            "Digits on page:", 'calibri', int(self.screen_width/48), self.digits_in_columns_rect.centerx,
            self.page_change_multiplier_rect.bottom + 0.5 * (
                        (self.digits_rect.bottom - self.screen_height * 0.08) - self.page_change_multiplier_rect.bottom)
        )

        # Buttons and counters
        self.back_button_text, self.back_button_rect, self.back_button_text_rect = self.helpers.create_button_and_rect(
            "Back", 'cambria', int(self.screen_width/54),
            self.digits_rect.right + (self.screen_width - self.digits_rect.right) * 0.5 - self.screen_width * 0.08,
            self.digits_rect.bottom - self.screen_height * 0.08,
            self.screen_width * 0.16, self.screen_height * 0.08
        )

        # Counters
        self.digits_in_columns_counter_text, self.digits_in_columns_counter_rect = self.helpers.create_counter_and_rect(
            str(self.digits_in_columns_counter), 'calibri', int(self.screen_width/48), self.digits_in_columns_rect
        )
        self.page_number_counter_text, self.page_number_counter_rect = self.helpers.create_counter_and_rect(
            str(self.page_number_counter), 'calibri', int(self.screen_width/48), self.page_number_rect
        )
        self.page_change_multiplier_counter_text, self.page_change_multiplier_counter_rect = self.helpers.create_counter_and_rect(
            "x" + str(self.page_change_multiplier_counter), 'calibri', int(self.screen_width/48), self.page_change_multiplier_rect
        )
        self.digits_on_page_counter_text, self.digits_on_page_counter_rect = self.helpers.create_counter_and_rect(
            f"{self.digits_on_page_counter_bottom} - {self.digits_on_page_counter_top}", 'calibri', int(self.screen_width/48),
            self.digits_on_page_rect
        )

        # Images rectangles
        self.digits_in_columns_minus = self.helpers.create_image_rect('minus', self.digits_in_columns_rect, -80)
        self.digits_in_columns_plus = self.helpers.create_image_rect('plus', self.digits_in_columns_rect, 80)
        self.page_number_minus = self.helpers.create_image_rect('minus', self.page_number_rect, -80)
        self.page_number_plus = self.helpers.create_image_rect('plus', self.page_number_rect, 80)
        self.page_change_multiplier_minus = self.helpers.create_image_rect('minus', self.page_change_multiplier_rect, -80)
        self.page_change_multiplier_plus = self.helpers.create_image_rect('plus', self.page_change_multiplier_rect, 80)

    def training_screen_settings_objects(self):
        self.images_initialization()

        # Texts
        self.training_mode_title_text, self.training_mode_title_rect = self.helpers.create_text_and_rect(
            "Training mode", 'candara', int(self.screen_width/26), self.screen_width * 0.5, self.screen_height * 0.25
        )
        self.choose_start_point_text, self.choose_start_point_rect = self.helpers.create_text_and_rect(
            "Choose a start point", 'candara', int(self.screen_width/32), self.screen_width * 0.5,
                                                   self.training_mode_title_rect.bottom + self.training_mode_title_rect.height * 1.4
        )
        self.start_digit_text, self.start_digit_rect = self.helpers.create_text_and_rect(
            "Digit:", 'calibri', int(self.screen_width/48), self.training_mode_title_rect.left,
            self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 0.2
        )
        self.digit_multiplier_text, self.digit_multiplier_rect = self.helpers.create_text_and_rect(
            "Multiplier:", 'calibri', int(self.screen_width/48), self.training_mode_title_rect.right,
            self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 0.2
        )

        # Buttons
        self.start_button_text, self.start_button_rect, self.start_button_text_rect = self.helpers.create_button_and_rect(
            "Start", 'candara', int(self.screen_width/32), self.training_mode_title_rect.centerx - self.screen_width * 0.08,
                                    self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 3,
                                    self.screen_width * 0.16, self.screen_height * 0.08
        )
        self.back_button_text, self.back_button_rect, self.back_button_text_rect = self.helpers.create_button_and_rect(
            "Back", 'candara', int(self.screen_width/32), self.start_button_rect.x,
            self.start_button_rect.bottom + self.start_button_rect.height * 0.2,
            self.screen_width * 0.16, self.screen_height * 0.08
        )

        # Counters
        self.start_digit_counter_text, self.start_digit_counter_rect = self.helpers.create_counter_and_rect(
            str(self.start_digit_counter), 'candara', int(self.screen_width/38), self.start_digit_rect
        )
        self.digit_multiplier_counter_text, self.digit_multiplier_counter_rect = self.helpers.create_counter_and_rect(
            "x" + str(self.digit_multiplier_counter), 'candara', int(self.screen_width/38), self.digit_multiplier_rect
        )

        # Images
        self.start_digit_plus = self.helpers.create_image_rect('plus', self.start_digit_rect, 95)
        self.start_digit_minus = self.helpers.create_image_rect('minus', self.start_digit_rect, -95)
        self.digit_multiplier_plus = self.helpers.create_image_rect('plus', self.digit_multiplier_rect, 95)
        self.digit_multiplier_minus = self.helpers.create_image_rect('minus', self.digit_multiplier_rect, -95)

    def training_screen_objects(self):
        self.images_initialization()

        # Rectangles
        self.guessing_rect = pg.Rect(self.screen_width * 0.06, self.screen_height * 0.1,  # Position
                                     self.screen_width * 0.88, self.screen_height * 0.12)  # Size

        self.switch_keys_layout_text, self.switch_keys_layout_rect, self.switch_keys_layout_text_rect = self.helpers.create_button_and_rect(
            "Switch the keys layout", 'calibri', int(self.screen_width/48),
            self.guessing_rect.left,
            self.guessing_rect.bottom + self.guessing_rect.height,
            self.screen_width * 0.24, self.screen_height * 0.12
        )

        self.hint_rect = pg.Rect(self.guessing_rect.left,
                                 self.switch_keys_layout_rect.bottom + self.switch_keys_layout_rect.height * 0.35,
                                 self.screen_width * 0.24, self.screen_height * 0.12)

        # Texts
        hint_color = (59, 59, 59) if self.switch_position == 0 else 'white'
        self.hint_text, self.hint_text_rect = self.helpers.create_text_and_rect(
            f"Hint after: {self.hint_counter} seconds", 'calibri', int(self.screen_width/48), self.hint_rect.centerx, self.hint_rect.centery,
            hint_color
        )
        # Reducing the text_rect size (for better centering)
        self.hint_text_rect.inflate_ip(-10, -10)

        self.your_time_text, self.your_time_rect = self.helpers.create_text_and_rect(
            "Your time:", 'candara', int(self.screen_width/26), self.back_button_rect.centerx, self.switch_keys_layout_rect.centery
        )

        # Back button
        self.back_button_text, self.back_button_rect, self.back_button_text_rect = self.helpers.create_button_and_rect(
            'Back', 'candara', int(self.screen_width/32), self.guessing_rect.right - self.screen_width * 0.24,
                                   self.hint_rect.bottom + self.hint_rect.height * 0.35,
                                   self.screen_width * 0.24, self.screen_height * 0.12
        )

        # Images rectangles
        self.hint_minus = self.helpers.create_image_rect('t_s_minus', self.hint_rect,
                                                 int(-self.hint_rect.width * 0.5 + self.screen_width * 0.03),
                                                 int(-self.hint_rect.height * 0.1))
        self.hint_plus = self.helpers.create_image_rect('t_s_plus', self.hint_rect, 0, int(-self.hint_rect.height * 0.1))
        self.switch_on = self.helpers.create_image_rect('switch_on', self.hint_rect,
                                                int(self.hint_rect.width * 0.5 - self.screen_width * 0.03),
                                                int(-self.hint_rect.height * 0.1))
        self.switch_off = self.helpers.create_image_rect('switch_off', self.hint_rect,
                                                 int(self.hint_rect.width * 0.5 - self.screen_width * 0.03),
                                                 int(-self.hint_rect.height * 0.1))
        self.switch_neutral = self.helpers.create_image_rect('switch_neutral', self.hint_rect,
                                                     int(self.hint_rect.width * 0.5 - self.screen_width * 0.03),
                                                     int(-self.hint_rect.height * 0.1))

        # Keyboard keys initialization
        self.keys_initialization()

    def challenge_screen_settings_objects(self):
        self.images_initialization()

        # Texts
        self.challenge_mode_title_text, self.challenge_mode_title_rect = self.helpers.create_text_and_rect(
            "Challenge mode", 'candara', int(self.screen_width/26), self.screen_width * 0.5, self.screen_height * 0.15
        )

        self.choose_start_point_text, self.choose_start_point_rect = self.helpers.create_text_and_rect(
            "Choose a start point", 'candara', int(self.screen_width/32), self.screen_width * 0.25,
                                                   self.challenge_mode_title_rect.bottom + self.challenge_mode_title_rect.height * 0.7
        )

        self.set_ch_goal_text, self.set_ch_goal_rect = self.helpers.create_text_and_rect(
            "Set challenge goal", 'candara', int(self.screen_width/32), self.screen_width * 0.75, self.choose_start_point_rect.centery
        )

        self.set_thinking_time_text, self.set_thinking_time_rect = self.helpers.create_text_and_rect(
            "Set thinking time [s]", 'candara', int(self.screen_width/32), self.choose_start_point_rect.centerx,
            self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 3.35
        )

        self.mistakes_allowed_text, self.mistakes_allowed_rect = self.helpers.create_text_and_rect(
            "Mistakes allowed", 'candara', int(self.screen_width/32), self.set_ch_goal_rect.centerx,
            self.set_thinking_time_rect.centery
        )

        self.start_digit_text, self.start_digit_rect = self.helpers.create_text_and_rect(
            "Digit:", 'calibri', int(self.screen_width/48), self.choose_start_point_rect.left + 40,
                                     self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 0.2
        )

        self.digit_multiplier_text, self.digit_multiplier_rect = self.helpers.create_text_and_rect(
            "Multiplier:", 'calibri', int(self.screen_width/48), self.choose_start_point_rect.right - 40,
                                          self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 0.2
        )

        self.goal_digit_text, self.goal_digit_rect = self.helpers.create_text_and_rect(
            "Digit:", 'calibri', int(self.screen_width/48),
            self.set_ch_goal_rect.left + 15,
            self.set_ch_goal_rect.bottom + self.set_ch_goal_rect.height * 0.2
        )

        self.goal_digit_multiplier_text, self.goal_digit_multiplier_rect = self.helpers.create_text_and_rect(
            "Multiplier:", 'calibri', int(self.screen_width/48),
            self.set_ch_goal_rect.right - 15,
            self.set_ch_goal_rect.bottom + self.set_ch_goal_rect.height * 0.2
        )

        # Start and back buttons
        self.start_button_text, self.start_button_rect, self.start_button_text_rect = self.helpers.create_button_and_rect(
            'Start', 'candara', int(self.screen_width/32), self.challenge_mode_title_rect.centerx - self.screen_width * 0.08,
                                    self.set_thinking_time_rect.bottom + 0.4 * (
                                            self.screen_height - self.set_thinking_time_rect.bottom),
                                    self.screen_width * 0.16, self.screen_height * 0.08
        )

        self.back_button_text, self.back_button_rect, self.back_button_text_rect = self.helpers.create_button_and_rect(
            'Back', 'candara', int(self.screen_width/32), self.start_button_rect.left,
            self.start_button_rect.bottom + self.start_button_rect.height * 0.2, self.screen_width * 0.16,
            self.screen_height * 0.08
        )

        # Counters
        self.start_digit_counter_text, self.start_digit_counter_rect = self.helpers.create_counter_and_rect(
            str(self.start_digit_counter), 'candara', int(self.screen_width/38), self.start_digit_rect
        )

        self.digit_multiplier_counter_text, self.digit_multiplier_counter_rect = self.helpers.create_counter_and_rect(
            "x" + str(self.digit_multiplier_counter), 'candara', int(self.screen_width/38), self.digit_multiplier_rect
        )

        self.goal_digit_counter_text, self.goal_digit_counter_rect = self.helpers.create_counter_and_rect(
            str(self.goal_digit_counter), 'candara', int(self.screen_width/38), self.goal_digit_rect,
        )

        self.goal_digit_multiplier_counter_text, self.goal_digit_multiplier_counter_rect = self.helpers.create_counter_and_rect(
            "x" + str(self.goal_digit_multiplier_counter), 'candara', int(self.screen_width/38), self.goal_digit_multiplier_rect,
        )

        self.thinking_time_counter_text, self.thinking_time_counter_rect = self.helpers.create_counter_and_rect(
            str(self.thinking_time_counter), 'candara', int(self.screen_width/38), self.set_thinking_time_rect
        )

        self.mistakes_allowed_counter_text, self.mistakes_allowed_counter_rect = self.helpers.create_counter_and_rect(
            str(self.mistakes_allowed_counter), 'candara', int(self.screen_width/38), self.mistakes_allowed_rect
        )

        # Images rectangles
        self.start_digit_plus = self.helpers.create_image_rect('plus', self.start_digit_rect, offset_x=95)
        self.start_digit_minus = self.helpers.create_image_rect('minus', self.start_digit_rect, offset_x=-95)

        self.digit_multiplier_plus = self.helpers.create_image_rect('plus', self.digit_multiplier_rect, offset_x=95)
        self.digit_multiplier_minus = self.helpers.create_image_rect('minus', self.digit_multiplier_rect, offset_x=-95)

        self.goal_digit_plus = self.helpers.create_image_rect('plus', self.goal_digit_rect, offset_x=95)
        self.goal_digit_minus = self.helpers.create_image_rect('minus', self.goal_digit_rect, offset_x=-95)

        self.goal_digit_multiplier_plus = self.helpers.create_image_rect('plus', self.goal_digit_multiplier_rect, offset_x=95)
        self.goal_digit_multiplier_minus = self.helpers.create_image_rect('minus', self.goal_digit_multiplier_rect,
                                                                  offset_x=-95)

        self.thinking_time_plus = self.helpers.create_image_rect('plus', self.set_thinking_time_rect, offset_x=95)
        self.thinking_time_minus = self.helpers.create_image_rect('minus', self.set_thinking_time_rect, offset_x=-95)

        self.mistakes_allowed_plus = self.helpers.create_image_rect('plus', self.mistakes_allowed_rect, offset_x=95)
        self.mistakes_allowed_minus = self.helpers.create_image_rect('minus', self.mistakes_allowed_rect, offset_x=-95)

    def challenge_screen_objects(self):
        self.images_initialization()

        self.guessing_rect = pg.Rect(self.screen_width * 0.06, self.screen_height * 0.1,  # Position
                                     self.screen_width * 0.88, self.screen_height * 0.12)  # Size

        # Texts
        self.goal_text, self.goal_rect = self.helpers.create_text_and_rect(
            f"Goal: {self.goal_digit_counter - len(self.user_input)}", 'candara', int(self.screen_width/32),
            self.guessing_rect.left + self.screen_width * 0.12,
            self.guessing_rect.bottom + 2.8 * self.guessing_rect.height * 1.05
        )

        self.your_time_text, self.your_time_rect = self.helpers.create_text_and_rect(
            "Your time:", 'candara', int(self.screen_width/26), self.back_button_rect.centerx,
            self.guessing_rect.bottom + self.guessing_rect.height * 1.4
        )

        self.thinking_time_text, self.thinking_time_rect = self.helpers.create_text_and_rect(
            "Thinking time:", 'candara', int(self.screen_width/32), self.goal_rect.centerx,
            self.goal_rect.bottom + 2 * self.goal_rect.height * 0.6
        )

        #   Game_over texts
        self.game_text, self.game_rect = self.helpers.create_text_and_rect(
            "Game", 'candara', int(self.screen_width/20), self.screen_width * 0.5, self.screen_height * 0.45
        )

        self.over_text, self.over_rect = self.helpers.create_text_and_rect(
            "Over", 'candara', int(self.screen_width/20), self.game_rect.centerx, self.game_rect.bottom + self.game_rect.height
        )

        #   Winning texts
        self.win_main_text, self.win_main_rect = self.helpers.create_text_and_rect(
            "Good job!", 'candara', int(self.screen_width/20), self.screen_width * 0.5, self.screen_height * 0.5
        )

        self.win_second_text, self.win_second_rect = self.helpers.create_text_and_rect(
            "Goal reached!", 'calibri', int(self.screen_width/34),
            self.win_main_rect.centerx, self.win_main_rect.bottom + self.win_main_rect.height * 0.5, 'yellow'
        )

        # Buttons and counters
        self.switch_keys_layout_text, self.switch_keys_layout_rect, self.switch_keys_layout_text_rect = self.helpers.create_button_and_rect(
            "Switch the keys layout", 'calibri', int(self.screen_width/48),
            self.guessing_rect.left,
            self.guessing_rect.bottom + self.guessing_rect.height,
            self.screen_width * 0.24, self.screen_height * 0.12
        )

        # Back button
        self.back_button_text, self.back_button_rect, self.back_button_text_rect = self.helpers.create_button_and_rect(
            "OK" if self.goal_reached or self.game_over else "Back", 'candara', int(self.screen_width/32), self.guessing_rect.right - self.screen_width * 0.24,
                                   self.switch_keys_layout_rect.bottom + self.switch_keys_layout_rect.height * 1.7,
                                   self.screen_width * 0.24, self.screen_height * 0.12
        )

        # Keyboard initialization method
        self.keys_initialization()

    def nickname_screen(self):
        input_active = False  # Inactive insert box in the beginning
        color_inactive = 'lightskyblue'
        color_active = 'dodgerblue2'
        color = color_inactive
        x_offset = 0
        nick_length = 20

        # Nick inserting box initialization
        nick_rect = pg.Rect(self.screen_width * 0.5, self.screen_height * 0.45, self.screen_width * 0.16,
                            self.screen_height * 0.08)
        text = ''
        nick_inserted = False

        # Submit button
        submit_text, submit_rect, submit_text_rect = self.helpers.create_button_and_rect("Submit", 'cambria', int(self.screen_width/55),
                                                                                         nick_rect.x - self.screen_width * 0.06,
                                                                                         nick_rect.bottom + nick_rect.height * 0.6,
                                                                                         self.screen_width * 0.12,
                                                                                         self.screen_height * 0.08)

        while not nick_inserted:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    nick_inserted = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if submit_rect.collidepoint(event.pos):  # Submit button click handling
                        self.player_nick = text if text else 'Player'  # Nick saving
                        nick_inserted = True  # Confirmation
                    if nick_rect.collidepoint(event.pos):  # input field activation
                        input_active = True
                        color = color_active
                    else:  # outside input field click
                        input_active = False
                        color = color_inactive
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:  # Enter key click handling
                        self.player_nick = text if text else 'Player'  # Nick saving
                        nick_inserted = True  # Confirmation
                    elif input_active:  # if the field is active
                        if event.key == pg.K_BACKSPACE:
                            text = text[:-1]  # last character deleting
                        else:
                            if len(text) < nick_length:  # Nick length limit
                                text += event.unicode  # character inserting

            self.screen.fill('black')

            # "Enter your nickname" text
            prompt_text, prompt_rect = self.helpers.create_text_and_rect("Enter your nickname:", 'candara', int(self.screen_width/32),
                                                                         self.screen_width * 0.5,
                                                                         self.screen_height * 0.35)
            self.screen.blit(prompt_text, prompt_rect)

            # Inserted text rendering
            nick_text, nick_rect, nick_text_rect = self.helpers.create_button_and_rect(str(text), 'cambria', int(self.screen_width/55),
                                                                                       self.screen_width * 0.42 - x_offset,
                                                                                       self.screen_height * 0.45,
                                                                                       self.screen_width * 0.16 + x_offset * 2,
                                                                                       self.screen_height * 0.08,
                                                                                       color=color)
            if nick_rect.right - nick_text_rect.right < 25:
                x_offset += 17.5
            elif nick_rect.width > self.screen_width * 0.16 and nick_rect.right - nick_text_rect.right > 25:
                x_offset -= 17.5
                nick_text, nick_rect, nick_text_rect = self.helpers.create_button_and_rect(str(text), 'cambria', int(self.screen_width/55),
                                                                                           self.screen_width * 0.42 - x_offset,
                                                                                           self.screen_height * 0.45,
                                                                                           self.screen_width * 0.16 + x_offset * 2,
                                                                                           self.screen_height * 0.08,
                                                                                           color=color)

            # Buttons drawing
            self.helpers.draw_button(nick_rect, nick_text, nick_text_rect, color=color)
            self.helpers.draw_button(submit_rect, submit_text, submit_text_rect, 'green')

            pg.display.flip()
            self.clock.tick(30)

        return self.player_nick  # Nick returning after inserting

    def main_screen(self):
        main_running = True
        buttons = ('learning', 'training', 'challenge', 'highscores', 'quit')
        self.main_screen_objects()

        while main_running:
            self.screen.fill('black')

            # Logo displayed
            self.screen.blit(self.images['logo'], self.game_logo)

            # Drawing buttons
            for button in buttons:
                self.helpers.draw_button(
                    getattr(self, f"{button}_button_rect"),
                    getattr(self, f"{button}_button_text"),
                    getattr(self, f"{button}_button_text_rect")
                )

            for event in pg.event.get():
                if event.type == pg.QUIT:  # Application exit handling
                    if self.helpers.show_confirmation_dialog(self.screen):
                        main_running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.quit_button_rect.collidepoint(event.pos):
                        if self.helpers.show_confirmation_dialog(self.screen):
                            main_running = False
                    if self.learning_button_rect.collidepoint(event.pos):
                        self.learning_screen()
                    if self.training_button_rect.collidepoint(event.pos):
                        self.training_screen_settings()
                    if self.challenge_button_rect.collidepoint(event.pos):
                        self.challenge_screen_settings()
                    if self.highscores_button_rect.collidepoint(event.pos):
                        self.highscores_screen()

            pg.display.flip()
            self.clock.tick(60)

        pg.quit()
        sys.exit()

    def learning_screen(self):
        learning_running = True
        self.main_values()
        self.learning_screen_logic()

        def draw_texts():
            """Helper function to draw texts."""
            self.screen.blit(self.digits_in_columns_text, self.digits_in_columns_rect)
            self.screen.blit(self.page_number_text, self.page_number_rect)
            self.screen.blit(self.page_change_multiplier_text, self.page_change_multiplier_rect)
            self.screen.blit(self.digits_on_page_text, self.digits_on_page_rect)

        def draw_counters():
            """Helper function to draw counter-related texts."""
            self.screen.blit(self.digits_in_columns_counter_text, self.digits_in_columns_counter_rect)
            self.screen.blit(self.page_number_counter_text, self.page_number_counter_rect)
            self.screen.blit(self.page_change_multiplier_counter_text, self.page_change_multiplier_counter_rect)

        def draw_images():
            """Helper function to draw minus and plus images."""
            self.screen.blit(self.images['minus'], self.digits_in_columns_minus)
            self.screen.blit(self.images['plus'], self.digits_in_columns_plus)
            self.screen.blit(self.images['minus'], self.page_number_minus)
            self.screen.blit(self.images['plus'], self.page_number_plus)
            self.screen.blit(self.images['minus'], self.page_change_multiplier_minus)
            self.screen.blit(self.images['plus'], self.page_change_multiplier_plus)

        def handle_button_clicks(event_pos):
            """Helper function to handle button clicks."""
            if self.back_button_rect.collidepoint(event_pos):
                return False  # Exit learning screen

            # digits_in_columns - and + handling
            if self.digits_in_columns_minus.collidepoint(event_pos) and self.digits_in_columns_counter > 1:
                self.digits_in_columns_counter -= 1
            elif self.digits_in_columns_plus.collidepoint(event_pos) and self.digits_in_columns_counter < 10:
                self.digits_in_columns_counter += 1

            self.learning_screen_logic()
            self.digits_in_columns_counter_text = self.fonts['calibri'][int(self.screen_width/48)].render(
                str(self.digits_in_columns_counter), True, 'white')

            # page_number - and + handling
            if self.page_number_minus.collidepoint(event_pos):
                self.page_number_counter = max(1, self.page_number_counter - self.page_change_multiplier_counter)
            elif self.page_number_plus.collidepoint(event_pos):
                self.page_number_counter += self.page_change_multiplier_counter

            self.learning_screen_logic()
            self.page_number_counter_text = self.fonts['calibri'][int(self.screen_width/48)].render(
                str(self.page_number_counter), True, 'white')

            # page_change_multiplier - and + handling
            current_index = self.page_change_multipliers.index(self.page_change_multiplier_counter)
            if self.page_change_multiplier_minus.collidepoint(event_pos) and current_index > 0:
                self.page_change_multiplier_counter = self.page_change_multipliers[current_index - 1]
            elif self.page_change_multiplier_plus.collidepoint(event_pos) and current_index < len(
                    self.page_change_multipliers) - 1:
                self.page_change_multiplier_counter = self.page_change_multipliers[current_index + 1]

            self.learning_screen_logic()
            self.page_change_multiplier_counter_text = self.fonts['calibri'][int(self.screen_width/48)].render(
                "x" + str(self.page_change_multiplier_counter), True, 'white')

            return True  # Continue learning screen

        while learning_running:
            self.screen.fill((69, 69, 69))  # Dark gray background

            # Drawing
            draw_texts()
            draw_counters()
            draw_images()

            # Draw buttons
            pg.draw.rect(self.screen, 'white', self.digits_rect, 3)
            self.helpers.draw_button(self.back_button_rect, self.back_button_text, self.back_button_text_rect)

            # Draw digits
            self.draw_learning_pi_digits()

            # Events loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    learning_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # Handle button clicks and exit if necessary
                    learning_running = handle_button_clicks(event.pos)

            pg.display.flip()
            self.clock.tick(60)  # Screen refresh rate

    def training_screen_settings(self):
        training_settings_running = True
        self.main_values()
        self.training_screen_settings_objects()

        # Text_entries parameters to GUI manager
        text_entries_data = [
            ('start_digit_counter', self.start_digit_counter_rect),
        ]

        # Creating text rectangles and hiding them
        self.text_entries = {}
        for name, rect in text_entries_data:
            entry = pygame_gui.elements.UITextEntryLine(
                relative_rect=pg.Rect((rect.left - 5, rect.top), (60, 60)),
                manager=self.manager)
            entry.hide()
            self.text_entries[name] = entry

        def deactivate_all_entries():
            """Hide and deactivate all text entries."""
            for entry in self.text_entries.values():
                entry.unfocus()
                entry.hide()

        def draw_texts():
            self.screen.blit(self.training_mode_title_text, self.training_mode_title_rect)
            self.screen.blit(self.choose_start_point_text, self.choose_start_point_rect)
            self.screen.blit(self.start_digit_text, self.start_digit_rect)
            self.screen.blit(self.digit_multiplier_text, self.digit_multiplier_rect)

        def draw_counters():
            self.screen.blit(self.start_digit_counter_text, self.start_digit_counter_rect)
            self.screen.blit(self.digit_multiplier_counter_text, self.digit_multiplier_counter_rect)

        def draw_images():
            self.screen.blit(self.images['minus'], self.start_digit_minus)
            self.screen.blit(self.images['plus'], self.start_digit_plus)
            self.screen.blit(self.images['minus'], self.digit_multiplier_minus)
            self.screen.blit(self.images['plus'], self.digit_multiplier_plus)

        def handle_button_clicks(event_pos):
            """Helper function to handle button clicks."""
            if self.back_button_rect.collidepoint(event_pos):
                deactivate_all_entries()  # Deactivate all entries on exit
                return False  # Exit the settings screen

            if self.start_button_rect.collidepoint(event_pos):
                deactivate_all_entries()  # Deactivate all entries before starting the training screen
                self.training_screen()
                return False  # Start the training screen

            # Text entry handling after activation
            clicked_inside_entry = False
            for name, rect in text_entries_data:
                if rect.collidepoint(event_pos):
                    deactivate_all_entries()  # Deactivate other entries
                    entry = self.text_entries[name]
                    entry.set_text(str(getattr(self, name)))
                    entry.show()
                    entry.focus()
                    clicked_inside_entry = True

            if not clicked_inside_entry:
                deactivate_all_entries()  # Deactivate all entries if clicked outside

            # Handle start_digit - and + buttons
            if self.start_digit_minus.collidepoint(event_pos):
                self.start_digit_counter = max(1, self.start_digit_counter - self.digit_multiplier_counter)
            elif self.start_digit_plus.collidepoint(event_pos):
                self.start_digit_counter += self.digit_multiplier_counter

            self.training_screen_settings_objects()
            self.start_digit_counter_text = self.helpers.create_text(str(self.start_digit_counter), 'candara', int(self.screen_width/38))

            # Handle digit_multiplier - and + buttons
            current_index = self.digit_multipliers.index(self.digit_multiplier_counter)
            if self.digit_multiplier_minus.collidepoint(event_pos) and current_index > 0:
                self.digit_multiplier_counter = self.digit_multipliers[current_index - 1]
            elif self.digit_multiplier_plus.collidepoint(event_pos) and current_index < len(self.digit_multipliers) - 1:
                self.digit_multiplier_counter = self.digit_multipliers[current_index + 1]

            self.training_screen_settings_objects()
            self.digit_multiplier_counter_text = self.helpers.create_text("x" + str(self.digit_multiplier_counter),
                                                                          'candara', int(self.screen_width/38))

            return True  # Continue running

        while training_settings_running:
            time_delta = self.clock.tick(60) / 1000.0
            self.screen.fill((58, 58, 58))  # Dark gray background

            # Drawing
            draw_texts()
            draw_counters()
            draw_images()

            # Draw buttons
            self.helpers.draw_button(self.start_button_rect, self.start_button_text, self.start_button_text_rect)
            self.helpers.draw_button(self.back_button_rect, self.back_button_text, self.back_button_text_rect)

            # Events loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    training_settings_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    training_settings_running = handle_button_clicks(event.pos)
                elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    for name, entry in self.text_entries.items():
                        if event.ui_element == entry:
                            # Validate the input: only allow positive integers
                            if event.text.isdigit() and int(event.text) > 0:
                                setattr(self, name, int(event.text))
                            else:
                                setattr(self, name, 1)  # Set default value if invalid
                            entry.hide()
                            self.training_screen_settings_objects()
                            break

                self.manager.process_events(event)

            # Update and drawing GUI
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)

            pg.display.flip()
            self.clock.tick(60)  # Screen refresh rate

    def guessing_rect_drawing(self):
        # Start variables initialization
        single_digit_width, _ = self.fonts['calibri'][int(self.screen_width / 23)].size("0")
        if not self.digits_display_offset:
            self.digits_display_offset = single_digit_width

        # Display the text of digits entered by the user
        digits_str = "".join(self.user_input[-self.max_display_digits:])
        guessed_digits_text = self.fonts['calibri'][int(self.screen_width/23)].render(f"{digits_str}", True, 'white')

        # Full digit sequence for `base_text` (green)
        base_text_str = self.helpers.read_pi_digits()[:self.start_digit_counter + 1]

        # Set position for `guessed_digits_text`
        self.guessed_digits_text_rect = guessed_digits_text.get_rect(
            center=(self.guessing_rect.right - self.digits_display_offset, self.guessing_rect.centery + 8))

        # Calculate the maximum number of base digits to display based on available width
        available_width_for_base_text = self.guessed_digits_text_rect.left - self.guessing_rect.left
        max_base_digits_display = int(available_width_for_base_text / single_digit_width)

        # Display `base_text` only if there is space left
        displayed_base_text_str = base_text_str[-max_base_digits_display:] if len(
            digits_str) < self.max_display_digits else ""
        base_text = self.fonts['calibri'][int(self.screen_width/23)].render(displayed_base_text_str, True, 'green')

        # Set position for `base_text` only if it has content to display
        if displayed_base_text_str:
            self.base_text_rect = base_text.get_rect(
                center=(
                    self.guessed_digits_text_rect.left - 0.5 * base_text.get_width(), self.guessing_rect.centery + 8)
            )

        # Text indicating the digit number
        self.digit_number_text = self.fonts['calibri'][int(self.screen_width/35)].render(
            f"Digit: {self.digit_counter + self.start_digit_counter - 1}", True, 'white')
        self.digit_number_rect = self.digit_number_text.get_rect(
            center=(self.guessing_rect.centerx, self.guessing_rect.bottom + 0.4 * self.guessing_rect.height))

        # Drawing elements
        self.screen.blit(base_text, self.base_text_rect)
        self.screen.blit(guessed_digits_text, self.guessed_digits_text_rect)
        self.screen.blit(self.digit_number_text, self.digit_number_rect)

    def training_screen(self):
        training_running = True
        self.training_screen_objects()

        start_time = time.time()  # Start time initialization
        reset_time = time.time()  # Time of last interaction with digit squares initialization

        self.incorrect_square_number = None
        self.next_correct_digit = None  # Initially no digit highlighted

        single_digit_width, single_digit_height = self.fonts['calibri'][int(self.screen_width/23)].size("0")
        dot_width, _ = self.fonts['calibri'][int(self.screen_width/23)].size(".")
        self.max_display_digits = int((self.guessing_rect.width - dot_width) / single_digit_width)  # Number of digits visible in guessing_rect

        # Drawing texts (time, digits, and labels)
        def draw_texts():
            formatted_time = f'{time.strftime("%M:%S", time.gmtime(self.training_elapsed_time))}.{int((self.training_elapsed_time % 1) * 100):02d}'
            time_text = self.fonts['calibri'][int(self.screen_width/26)].render(f"{formatted_time}", True, 'white')
            time_rect = time_text.get_rect(
                center=(self.your_time_rect.centerx, self.your_time_rect.bottom + self.your_time_rect.height * 0.7))
            self.screen.blit(time_text, time_rect)
            self.screen.blit(self.your_time_text, self.your_time_rect)

            self.guessing_rect_drawing()

        # Drawing images and buttons
        def draw_images():
            """Draw all static images and buttons."""
            self.screen.blit(self.images['t_s_minus'], self.hint_minus)
            self.screen.blit(self.images['t_s_plus'], self.hint_plus)
            self.screen.blit(self.images['switch_off' if self.switch_position == 0 else 'switch_on'], self.switch_on)
            pg.draw.rect(self.screen, 'white', self.guessing_rect, width=3)
            pg.draw.rect(self.screen, 'white', self.switch_keys_layout_rect, width=3)
            pg.draw.rect(self.screen, (59, 59, 59) if self.switch_position == 0 else 'white', self.hint_rect, width=3)
            self.screen.blit(self.switch_keys_layout_text, self.switch_keys_layout_text_rect)
            self.screen.blit(self.hint_text, self.hint_text_rect)
            pg.draw.rect(self.screen, 'white', self.back_button_rect, 3)
            self.screen.blit(self.back_button_text, self.back_button_text_rect)

        # Drawing squares with digits and handling wrong clicks and hints
        def draw_digit_squares():
            for i in range(10):
                color = 'green' if i == self.next_correct_digit and self.switch_position == 1 else 'white'
                if i == self.incorrect_square_number:
                    color = 'red'
                pg.draw.rect(self.screen, color, getattr(self, f'square_{i}_rect'), 5)
                self.screen.blit(getattr(self, f'square_{i}_text'), getattr(self, f'square_{i}_text_rect'))

        def handle_button_clicks(event_pos):
            """Helper function to handle button clicks."""
            nonlocal reset_time, start_time

            # Back button handling
            if self.back_button_rect.collidepoint(event_pos):
                pause_start_time = time.time()  # Pause start time saving
                # Confirmation popup
                if self.helpers.show_confirmation_dialog(self.screen):  # Yes choice
                    return False  # Exit training screen
                else:  # "No" choice
                    pause_end_time = time.time()
                    pause_duration = pause_end_time - pause_start_time

                    start_time += pause_duration
                    reset_time += pause_duration

            # Switch button handling
            if self.switch_on.collidepoint(event_pos):
                self.switch_position = 1 - self.switch_position  # Toggle switch
                self.screen.blit(self.images['switch_neutral'], self.switch_neutral)

            # Hint + and - handling
            if self.hint_plus.collidepoint(event_pos) and self.switch_position == 1:
                self.hint_counter = min(10, self.hint_counter + 1)
            elif self.hint_minus.collidepoint(event_pos) and self.switch_position == 1:
                self.hint_counter = max(0, self.hint_counter - 1)

            # Switch keys layout
            if self.switch_keys_layout_rect.collidepoint(event_pos):
                self.keys_layout = 1 - self.keys_layout
                self.training_screen_objects()

            # Handle square clicks (digits 0-9)
            for i in range(10):
                if getattr(self, f'square_{i}_rect').collidepoint(event_pos):
                    self.compare_digits(str(i))  # Add the clicked digit
                    reset_time = time.time()  # Time resetting
                    self.next_correct_digit = None  # Reset the next correct digit hint timer
                    return True  # Continue training screen

            return True  # Continue training screen

        def handle_key_events(event_key):
            """Helper function to handle keyboard input."""
            nonlocal reset_time

            if pg.K_0 <= event_key <= pg.K_9:
                digit = event_key - pg.K_0  # Convert key to digit (0-9)
                self.compare_digits(str(digit))
                reset_time = time.time()  # Time resetting
                self.next_correct_digit = None
            elif 1073741913 <= event_key <= 1073741921:  # Numpad keys 1-9
                digit = event_key - 1073741912
                self.compare_digits(str(digit))
                reset_time = time.time()  # Time resetting
                self.next_correct_digit = None
            elif event_key == 1073741922:  # Numpad 0
                self.compare_digits("0")
                reset_time = time.time()  # Time resetting
                self.next_correct_digit = None

        while training_running:
            self.training_screen_objects()
            self.screen.fill((39, 39, 39))  # Dark gray color

            self.training_elapsed_time = time.time() - start_time
            self.time_to_hint = time.time() - reset_time

            draw_texts()
            draw_images()
            draw_digit_squares()

            # Checking if wrong square clicked
            if self.incorrect_square_number:
                i = self.incorrect_square_number
                pg.draw.rect(self.screen, 'red', getattr(self, f'square_{i}_rect'), 5)
                self.screen.blit(getattr(self, f'square_{i}_text'), getattr(self, f'square_{i}_text_rect'))

            # Check if it's time for a hint
            if self.time_to_hint > self.hint_counter and self.switch_position == 1:
                pi_digits = self.helpers.read_pi_digits()[self.start_digit_counter + 1:]
                self.next_correct_digit = int(pi_digits[len(self.user_input)])
                reset_time = time.time()

            # Events loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    training_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    training_running = handle_button_clicks(event.pos)
                elif event.type == pg.KEYDOWN:
                    handle_key_events(event.key)

            pg.display.flip()
            self.clock.tick(60)

    def compare_digits(self, user_input):
        # Single digit width
        single_digit_width, _ = self.fonts['calibri'][int(self.screen_width / 23)].size("0")

        self.incorrect_square_number = None
        pi_digits = self.helpers.read_pi_digits()[self.start_digit_counter + 1:].replace(".", "")

        # Building a list of digits to check
        tested_digits = self.user_input + [user_input]
        tested_token = pi_digits[:len(tested_digits)]

        # Digits compare
        if tested_digits == list(tested_token):
            self.user_input.append(user_input)
            self.digit_counter += 1
            if 1 < len(self.user_input) < self.max_display_digits + 1:
                self.digits_display_offset += single_digit_width/2
            return True
        else:
            self.mistakes_allowed_counter -= 1  # Working only in challenge_mode
            self.incorrect_square_number = user_input

    def challenge_screen_settings(self):
        challenge_settings_running = True
        self.main_values()
        self.challenge_screen_settings_objects()

        # Text_entries parameters to GUI manager
        text_entries_data = [
            ('start_digit_counter', self.start_digit_counter_rect),
            ('goal_digit_counter', self.goal_digit_counter_rect),
            ('thinking_time_counter', self.thinking_time_counter_rect),
        ]

        # Creating text rectangles and hiding them
        self.text_entries = {}
        for name, rect in text_entries_data:
            entry = pygame_gui.elements.UITextEntryLine(
                relative_rect=pg.Rect((rect.left - 5, rect.top), (60, 60)),
                manager=self.manager)
            entry.hide()
            self.text_entries[name] = entry

        def deactivate_all_entries():
            """Hide and deactivate all text entries."""
            for entry in self.text_entries.values():
                entry.unfocus()
                entry.hide()

        def draw_texts():
            # Drawing titles and labels
            self.screen.blit(self.challenge_mode_title_text, self.challenge_mode_title_rect)
            self.screen.blit(self.choose_start_point_text, self.choose_start_point_rect)
            self.screen.blit(self.start_digit_text, self.start_digit_rect)
            self.screen.blit(self.digit_multiplier_text, self.digit_multiplier_rect)
            self.screen.blit(self.set_ch_goal_text, self.set_ch_goal_rect)
            self.screen.blit(self.goal_digit_text, self.goal_digit_rect)
            self.screen.blit(self.goal_digit_multiplier_text, self.goal_digit_multiplier_rect)
            self.screen.blit(self.set_thinking_time_text, self.set_thinking_time_rect)
            self.screen.blit(self.mistakes_allowed_text, self.mistakes_allowed_rect)

        def draw_counters():
            # Drawing counter texts
            self.screen.blit(self.start_digit_counter_text, self.start_digit_counter_rect)
            self.screen.blit(self.digit_multiplier_counter_text, self.digit_multiplier_counter_rect)
            self.screen.blit(self.goal_digit_counter_text, self.goal_digit_counter_rect)
            self.screen.blit(self.goal_digit_multiplier_counter_text, self.goal_digit_multiplier_counter_rect)
            self.screen.blit(self.thinking_time_counter_text, self.thinking_time_counter_rect)
            self.screen.blit(self.mistakes_allowed_counter_text, self.mistakes_allowed_counter_rect)

        def draw_images():
            # Drawing plus and minus images
            controls = [
                (self.start_digit_minus, self.start_digit_plus),
                (self.digit_multiplier_minus, self.digit_multiplier_plus),
                (self.goal_digit_minus, self.goal_digit_plus),
                (self.goal_digit_multiplier_minus, self.goal_digit_multiplier_plus),
                (self.thinking_time_minus, self.thinking_time_plus),
                (self.mistakes_allowed_minus, self.mistakes_allowed_plus)
            ]

            for minus, plus in controls:
                self.screen.blit(self.images['minus'], minus)
                self.screen.blit(self.images['plus'], plus)

        def update_counter_texts():
            self.start_digit_counter_text = self.helpers.create_text(str(self.start_digit_counter), 'candara', int(self.screen_width/38))
            self.digit_multiplier_counter_text = self.helpers.create_text("x" + str(self.digit_multiplier_counter), 'candara',
                                                                  50)
            self.goal_digit_counter_text = self.helpers.create_text(str(self.goal_digit_counter), 'candara', int(self.screen_width/38))
            self.goal_digit_multiplier_counter_text = self.helpers.create_text("x" + str(self.goal_digit_multiplier_counter),
                                                                       'candara', int(self.screen_width/38))
            self.thinking_time_counter_text = self.helpers.create_text(str(self.thinking_time_counter), 'candara', int(self.screen_width/38))
            self.mistakes_allowed_counter_text = self.helpers.create_text(str(self.mistakes_allowed_counter), 'candara', int(self.screen_width/38))
            self.challenge_screen_settings_objects()

        def handle_button_clicks():
            """Helper function to handle button clicks."""
            if self.back_button_rect.collidepoint(event.pos):
                deactivate_all_entries()  # Deactivate all entries on exit
                self.main_screen()
                return False  # Exit the settings screen

            if self.start_button_rect.collidepoint(event.pos):
                deactivate_all_entries()  # Deactivate all entries on exit
                self.challenge_screen()
                return False  # Start the challenge screen

            # Text entry handling after activation
            for name, rect in text_entries_data:
                if rect.collidepoint(event.pos):
                    entry = self.text_entries[name]
                    entry.set_text(str(getattr(self, name)))
                    entry.show()
                    entry.focus()
                    return True

            # Start digit handling
            if self.start_digit_minus.collidepoint(event.pos):
                self.start_digit_counter = max(1, self.start_digit_counter - self.digit_multiplier_counter)
            elif self.start_digit_plus.collidepoint(event.pos):
                self.start_digit_counter += self.digit_multiplier_counter

            # Digit multiplier handling
            current_index = self.digit_multipliers.index(self.digit_multiplier_counter)
            if self.digit_multiplier_minus.collidepoint(event.pos) and current_index > 0:
                self.digit_multiplier_counter = self.digit_multipliers[current_index - 1]
            elif self.digit_multiplier_plus.collidepoint(event.pos) and current_index < len(self.digit_multipliers) - 1:
                self.digit_multiplier_counter = self.digit_multipliers[current_index + 1]

            # Goal digit handling
            if self.goal_digit_minus.collidepoint(event.pos):
                self.goal_digit_counter = max(25, self.goal_digit_counter - self.goal_digit_multiplier_counter)
            elif self.goal_digit_plus.collidepoint(event.pos):
                self.goal_digit_counter += self.goal_digit_multiplier_counter

            # Goal multiplier handling
            current_goal_index = self.goal_digit_multipliers.index(self.goal_digit_multiplier_counter)
            if self.goal_digit_multiplier_minus.collidepoint(event.pos) and current_goal_index > 0:
                self.goal_digit_multiplier_counter = self.goal_digit_multipliers[current_goal_index - 1]
            elif self.goal_digit_multiplier_plus.collidepoint(event.pos) and current_goal_index < len(
                    self.goal_digit_multipliers) - 1:
                self.goal_digit_multiplier_counter = self.goal_digit_multipliers[current_goal_index + 1]

            # Thinking time handling
            if self.thinking_time_minus.collidepoint(event.pos):
                self.thinking_time_counter = max(5, self.thinking_time_counter - 5)
            elif self.thinking_time_plus.collidepoint(event.pos):
                self.thinking_time_counter = min(60, self.thinking_time_counter + 5)

            # Mistakes allowed handling
            if self.mistakes_allowed_minus.collidepoint(event.pos):
                self.mistakes_allowed_counter = max(1, self.mistakes_allowed_counter - 1)
            elif self.mistakes_allowed_plus.collidepoint(event.pos):
                self.mistakes_allowed_counter = min(5, self.mistakes_allowed_counter + 1)

            # Update all counter texts
            update_counter_texts()

            return True  # Continue running

        while challenge_settings_running:
            time_delta = self.clock.tick(60) / 1000.0
            self.screen.fill((59, 59, 59))  # Dark gray background

            # Drawing
            draw_texts()
            draw_counters()
            draw_images()

            # Draw buttons
            self.helpers.draw_button(self.start_button_rect, self.start_button_text, self.start_button_text_rect)
            self.helpers.draw_button(self.back_button_rect, self.back_button_text, self.back_button_text_rect)

            # Events loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    challenge_settings_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    challenge_settings_running = handle_button_clicks()
                    # Handle text entry activation
                    clicked_inside_entry = False
                    for name, rect in text_entries_data:
                        if rect.collidepoint(event.pos):
                            deactivate_all_entries()
                            entry = self.text_entries[name]
                            entry.set_text(str(getattr(self, name)))
                            entry.show()
                            entry.focus()
                            clicked_inside_entry = True
                            break

                    if not clicked_inside_entry:
                        deactivate_all_entries()
                elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    for name, entry in self.text_entries.items():
                        if event.ui_element == entry:
                            # Validate the input: only allow positive integers
                            if event.text.isdigit() and int(event.text) > 0:
                                setattr(self, name, int(event.text))
                            else:
                                setattr(self, name, 1)  # Set default value if invalid
                            entry.hide()
                            update_counter_texts()
                            break

                self.manager.process_events(event)

            # Update and drawing GUI
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)

            pg.display.flip()
            self.clock.tick(60)

    def draw_hearts(self):
        if self.mistakes_allowed_counter:
            for i in range(self.mistakes_allowed_counter):
                mistakes_allowed_heart = self.images['heart'].get_rect(
                    center=(self.guessing_rect.right - self.screen_width * 0.019 - (i * self.screen_width * 0.039),
                            self.guessing_rect.bottom + 0.4 * self.guessing_rect.height)
                )

                self.screen.blit(self.images['heart'], mistakes_allowed_heart)
        else:
            self.game_over = True

    def challenge_screen(self):
        challenge_running = True
        nick = None
        mistakes_allowed = self.mistakes_allowed_counter
        self.challenge_screen_objects()

        start_time = time.time()
        thinking_start_time = time.time()

        self.incorrect_square_number = None
        self.average_thinking_time = 0

        total_time = None  # Time of challenge ending (initialization)

        single_digit_width, single_digit_height = self.fonts['calibri'][int(self.screen_width / 23)].size("0")
        self.max_display_digits = int((self.guessing_rect.width - single_digit_width) / single_digit_width)  # Number of digits visible in guessing_rect

        def draw_texts():
            formatted_time = f'{time.strftime("%M:%S", time.gmtime(self.challenge_elapsed_time))}.{int((self.challenge_elapsed_time % 1) * 100):02d}'
            time_color = 'red' if self.game_over else 'green' if self.goal_reached else 'white'
            time_text = self.fonts['calibri'][int(self.screen_width / 26)].render(formatted_time, True, time_color)
            time_rect = time_text.get_rect(
                center=(self.your_time_rect.centerx, self.your_time_rect.bottom + self.your_time_rect.height * 0.7))
            self.screen.blit(time_text, time_rect)

            remaining_thinking_time = max(self.thinking_time_counter - self.thinking_elapsed_time, 0)
            formatted_thinking_time = "{:.2f}".format(remaining_thinking_time)
            thinking_color = 'red' if remaining_thinking_time == 0 else 'white'
            thinking_time_text = self.fonts['calibri'][int(self.screen_width / 32)].render(formatted_thinking_time, True, thinking_color)
            thinking_time_rect = thinking_time_text.get_rect(center=(self.thinking_time_rect.centerx,
                                                                     self.thinking_time_rect.bottom + self.thinking_time_rect.height * 0.6))

            self.screen.blit(thinking_time_text, thinking_time_rect)
            self.screen.blit(self.your_time_text, self.your_time_rect)
            self.screen.blit(self.goal_text, self.goal_rect)
            self.screen.blit(self.thinking_time_text, self.thinking_time_rect)

            self.guessing_rect_drawing()

        def update_thinking_times():
            """Updates the list of thinking times and calculates the average time"""
            nonlocal thinking_start_time
            thinking_times = []
            total_thinking_time = 0

            current_thinking_time = time.time() - thinking_start_time
            thinking_times.append(current_thinking_time)
            total_thinking_time += current_thinking_time
            self.average_thinking_time = total_thinking_time / len(thinking_times)
            thinking_start_time = time.time()  # Thinking time start reset

        def draw_elements():
            self.draw_hearts()
            pg.draw.rect(self.screen, 'white', self.guessing_rect, width=3)
            pg.draw.rect(self.screen, 'white', self.switch_keys_layout_rect, width=3)
            pg.draw.rect(self.screen, 'green' if self.game_over or self.goal_reached else 'white',
                         self.back_button_rect, 5 if self.game_over or self.goal_reached else 3)
            self.screen.blit(self.switch_keys_layout_text, self.switch_keys_layout_text_rect)
            self.screen.blit(self.back_button_text, self.back_button_text_rect)

        def draw_digit_squares():
            if not self.game_over and not self.goal_reached:
                for i in range(10):
                    pg.draw.rect(self.screen, 'white', getattr(self, f'square_{i}_rect'), 5)
                    self.screen.blit(getattr(self, f'square_{i}_text'), getattr(self, f'square_{i}_text_rect'))

                # Checking if wrong square clicked
                if self.incorrect_square_number:
                    i = self.incorrect_square_number
                    pg.draw.rect(self.screen, 'red', getattr(self, f'square_{i}_rect'), 5)
                    self.screen.blit(getattr(self, f'square_{i}_text'), getattr(self, f'square_{i}_text_rect'))

        def handle_button_clicks(event_pos):
            nonlocal challenge_running, thinking_start_time, start_time, nick, total_time, mistakes_allowed
            if self.back_button_rect.collidepoint(event_pos):
                if self.game_over:
                    handle_back_button_logic()  # without confirmation popup
                else:  # if not game over, show confirmation popup
                    pause_start_time = time.time()  # Pause start time saving
                    if self.goal_reached:
                        handle_back_button_logic()
                    else:
                        if self.helpers.show_confirmation_dialog(self.screen):  # "Yes" choice
                            challenge_running = False
                            self.main_values()
                            self.challenge_screen_settings()
                        else:  # "No" choice
                            pause_end_time = time.time()
                            pause_duration = pause_end_time - pause_start_time
                            thinking_start_time += pause_duration
                            start_time += pause_duration

            elif not self.game_over and not self.goal_reached:
                if self.switch_keys_layout_rect.collidepoint(event_pos):
                    self.keys_layout = 1 - self.keys_layout
                    self.challenge_screen_objects()
                for i in range(10):
                    if getattr(self, f'square_{i}_rect').collidepoint(event_pos):
                        if self.compare_digits(str(i)):
                            update_thinking_times()

        def handle_back_button_logic():
            """Logic for handling back button or equivalent actions"""
            nonlocal challenge_running, nick, total_time, mistakes_allowed
            if self.goal_reached:
                nick = self.nickname_screen()
                digits = self.goal_digit_counter
                mistakes_ratio = str(f"{mistakes_allowed - self.mistakes_allowed_counter}/{mistakes_allowed}")
                score = self.calculate_score(digits, self.average_thinking_time, self.thinking_time_counter,
                                             total_time, mistakes_allowed - self.mistakes_allowed_counter,
                                             mistakes_allowed)
                self.helpers.save_to_highscores(nick, digits, self.average_thinking_time, total_time,
                                                mistakes_ratio, score, self.thinking_time_counter)
            challenge_running = False
            self.main_values()
            self.challenge_screen_settings()

        def handle_key_events(event_key):
            """Keyboard events handling."""
            nonlocal challenge_running, nick, total_time, mistakes_allowed

            if event_key == pg.K_RETURN:  # Enter key pressed
                if self.goal_reached or self.game_over:  # When the goal is reached or the game is over
                    handle_back_button_logic()

            if not self.game_over and not self.goal_reached:
                if pg.K_0 <= event_key <= pg.K_9:
                    digit = event_key - pg.K_0
                    if self.compare_digits(str(digit)):
                        update_thinking_times()
                elif 1073741913 <= event_key <= 1073741922:
                    digit = event_key - 1073741912 if event_key != 1073741922 else 0
                    if self.compare_digits(str(digit)):
                        update_thinking_times()

        while challenge_running:
            self.challenge_screen_objects()
            self.screen.fill((39, 39, 39))

            if not self.game_over and not self.goal_reached:
                self.challenge_elapsed_time = time.time() - start_time
                self.thinking_elapsed_time = time.time() - thinking_start_time
                if self.thinking_elapsed_time >= self.thinking_time_counter:
                    self.game_over = True

            # Total time saving after reaching the goal
            if self.digit_counter - 1 == self.goal_digit_counter:
                if total_time is None:
                    total_time = time.time() - start_time
                self.goal_reached = True
                self.goal_text = self.fonts['candara'][int(self.screen_width / 32)].render(f"Goal: {self.goal_digit_counter}", True, 'green')
                self.screen.blit(self.win_main_text, self.win_main_rect)
                self.screen.blit(self.win_second_text, self.win_second_rect)

            # Drawing
            draw_texts()
            draw_elements()
            draw_digit_squares()

            if self.game_over:
                self.screen.blit(self.game_text, self.game_rect)
                self.screen.blit(self.over_text, self.over_rect)
                pi_digits = self.helpers.read_pi_digits()[self.start_digit_counter + 1:]
                correct_digits_text = self.fonts['calibri'][int(self.screen_width / 32)].render(
                    f"Should be: {pi_digits[len(self.user_input):len(self.user_input) + 5]}...", True, 'yellow')
                correct_digits_rect = correct_digits_text.get_rect(
                    center=(self.over_rect.centerx, self.over_rect.bottom + self.over_rect.height * 0.5))
                self.screen.blit(correct_digits_text, correct_digits_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    challenge_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    handle_button_clicks(event.pos)
                elif event.type == pg.KEYDOWN:
                    handle_key_events(event.key)

            pg.display.flip()
            self.clock.tick(60)

    @staticmethod
    def calculate_score(digits_inserted, avg_thinking_time, time_for_thinking, total_time, mistakes_made,
                        mistakes_allowed):

        digits_inserted_points = digits_inserted * 2.6
        thinking_time_points = 0.5 * (65 - time_for_thinking) + (10 * (1 / avg_thinking_time))
        total_time_points = (15 * digits_inserted) * (1 / total_time)
        mistakes_points = (5 * (5 - mistakes_made)) * (5 * (1 / mistakes_allowed))

        # Final score calculation
        score = int(digits_inserted_points + thinking_time_points + total_time_points + mistakes_points)
        return max(0, score)

    def highscores_screen_objects(self):
        """Initialize objects for the highscores screen"""
        self.highscores_title_text, self.highscores_title_rect = self.helpers.create_text_and_rect(
            "High Scores", 'cambria', int(self.screen_width/25), self.screen_width * 0.5, self.screen_height * 0.1)
        self.back_button_text, self.back_button_rect, self.back_button_text_rect = self.helpers.create_button_and_rect(
            "Back", 'candara', int(self.screen_width/32), self.highscores_title_rect.centerx - self.screen_width * 0.1,
                                   self.screen_height * 0.80,
                                   self.screen_width * 0.20, self.screen_height * 0.1
        )

        highscores_labels = ["Nick", "Digits", "Thinking Time", "Total Time", "Mistakes Ratio", "Score"]
        self.highscore_labels_texts_rects = []
        x_offset = 0

        # Create labels
        for i, label in enumerate(highscores_labels):
            # Highscore labels
            label_text, label_rect = self.helpers.create_text_and_rect(
                highscores_labels[i], 'cambria', int(self.screen_width/55), self.screen_width * 0.125 + x_offset, self.screen_height * 0.2
            )
            # Adding text and rectangle to the list
            self.highscore_labels_texts_rects.append((label_text, label_rect))
            x_offset += self.screen_width * 0.15

    def highscores_screen(self):
        """Highscores screen logic"""
        highscores_running = True
        self.highscores_screen_objects()

        highscores_list = self.helpers.read_from_highscores()

        while highscores_running:
            self.screen.fill('black')

            # Display title
            self.screen.blit(self.highscores_title_text, self.highscores_title_rect)

            # Display labels
            for label_text, label_rect in self.highscore_labels_texts_rects:
                self.screen.blit(label_text, label_rect)

                # Display each highscore in columns under corresponding labels
                y_offset = self.screen_height * 0.3  # Initial Y position for values
                for entry in highscores_list:
                    x_offset = self.screen_width * 0.125  # Reset X position for each row
                    for value in entry:
                        # Display value under corresponding label
                        value_text = self.helpers.create_text(str(value), 'cambria', int(self.screen_width/76))
                        value_rect = value_text.get_rect(center=(x_offset, y_offset))
                        self.screen.blit(value_text, value_rect)
                        x_offset += self.screen_width * 0.15  # Move to the next column
                    y_offset += 40  # Move down for the next row of values

            # Display back button
            self.helpers.draw_button(self.back_button_rect, self.back_button_text, self.back_button_text_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    highscores_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.back_button_rect.collidepoint(event.pos):
                        highscores_running = False  # Return to the main screen

            pg.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    game = PiGame()
