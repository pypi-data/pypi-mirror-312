
import time
import random
import threading
import vgamepad as vg
import configparser
import logging
import os
import platform
import subprocess
import requests
import zipfile
from zeus_server_load.utils import log_info, log_error, log_success


class GamepadController:
    def __init__(self, config_path="config.ini"):
        self.running = True
        self.anti_afk_enabled = False
        self.movement_enabled = False
        self.gamepad = vg.VX360Gamepad()
        self.load_config(config_path)
        self.lock = threading.Lock()

    def load_config(self, config_path):
        """Load configuration from config file."""
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # Load Anti-AFK settings
        self.anti_afk_interval = self.config.getfloat('AntiAFK', 'interval', fallback=60)
        self.right_bumper_duration = self.config.getfloat('AntiAFK', 'right_bumper_duration', fallback=0.1)
        self.left_bumper_duration = self.config.getfloat('AntiAFK', 'left_bumper_duration', fallback=0.1)
        self.delay_between_buttons = self.config.getfloat('AntiAFK', 'delay_between_buttons', fallback=0.5)

        # Load Movement settings
        self.min_movement_duration = self.config.getfloat('Movement', 'min_movement_duration', fallback=4.0)
        self.max_movement_duration = self.config.getfloat('Movement', 'max_movement_duration', fallback=6.0)
        self.min_break_duration = self.config.getfloat('Movement', 'min_break_duration', fallback=3.0)
        self.max_break_duration = self.config.getfloat('Movement', 'max_break_duration', fallback=7.0)

    def anti_afk_loop(self):
        """Anti-AFK loop that periodically presses buttons."""
        logging.info("Anti-AFK loop started")
        while self.running:
            if not self.anti_afk_enabled:
                time.sleep(0.1)
                continue

            with self.lock:
                self.press_rb()
                time.sleep(self.delay_between_buttons)
                self.press_lb()

            logging.info(f"Anti-AFK: Waiting {self.anti_afk_interval} seconds")
            time.sleep(self.anti_afk_interval)
        logging.info("Anti-AFK loop ended")

    def movement_loop(self):
        """Movement loop that simulates random controller inputs."""
        logging.info("Movement loop started")
        while self.running:
            if not self.movement_enabled:
                time.sleep(0.1)
                continue

            logging.info("Simulating movement...")
            duration = random.uniform(self.min_movement_duration, self.max_movement_duration)
            start_time = time.time()

            while self.running and self.movement_enabled and (time.time() - start_time) < duration:
                move_x = random.uniform(-1, 1)
                move_y = random.uniform(-1, 1)
                with self.lock:
                    self.gamepad.left_joystick_float(x_value_float=move_x, y_value_float=move_y)
                    self.gamepad.update()
                time.sleep(0.1)

            logging.info(f"Movement phase complete. Breaking for {duration} seconds.")
            time.sleep(random.uniform(self.min_break_duration, self.max_break_duration))
        logging.info("Movement loop ended")

    # Individual Button and Control Methods
    def press_a(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A, "A")

    def press_b(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B, "B")

    def press_x(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X, "X")

    def press_y(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y, "Y")

    def press_lb(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER, "LB")

    def press_rb(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER, "RB")

    def press_lt(self):
        self._press_trigger(0, "LT")

    def press_rt(self):
        self._press_trigger(1, "RT")

    def press_start(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START, "START")

    def press_back(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK, "BACK")

    def press_ls(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB, "Left Stick Click")

    def press_rs(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB, "Right Stick Click")

    def move_dpad_up(self):
        self._move_dpad(vg.DPAD.UP, "DPAD UP")

    def move_dpad_down(self):
        self._move_dpad(vg.DPAD.DOWN, "DPAD DOWN")

    def move_dpad_left(self):
        self._move_dpad(vg.DPAD.LEFT, "DPAD LEFT")

    def move_dpad_right(self):
        self._move_dpad(vg.DPAD.RIGHT, "DPAD RIGHT")

    def move_left_stick(self, x, y):
        with self.lock:
            self.gamepad.left_joystick_float(x_value_float=x, y_value_float=y)
            self.gamepad.update()
        logging.info(f"Moved Left Stick to ({x}, {y})")

    def move_right_stick(self, x, y):
        with self.lock:
            self.gamepad.right_joystick_float(x_value_float=x, y_value_float=y)
            self.gamepad.update()
        logging.info(f"Moved Right Stick to ({x}, {y})")

    # Helper Methods for Actions
    def _press_button(self, button, name):
        logging.info(f"Pressing '{name}' button")
        with self.lock:
            self.gamepad.press_button(button)
            self.gamepad.update()
            time.sleep(0.1)
            self.gamepad.release_button(button)
            self.gamepad.update()

    def _press_trigger(self, trigger, name):
        logging.info(f"Pressing '{name}' trigger")
        with self.lock:
            if trigger == 0:  # LT
                self.gamepad.left_trigger(value=255)
            elif trigger == 1:  # RT
                self.gamepad.right_trigger(value=255)
            self.gamepad.update()
            time.sleep(0.1)
            if trigger == 0:  # LT
                self.gamepad.left_trigger(value=0)
            elif trigger == 1:  # RT
                self.gamepad.right_trigger(value=0)
            self.gamepad.update()

    def _move_dpad(self, direction, name):
        logging.info(f"Moving '{name}'")
        with self.lock:
            self.gamepad.d_pad(direction)
            self.gamepad.update()
            time.sleep(0.1)
            self.gamepad.d_pad(vg.DPAD.OFF)
            self.gamepad.update()

    def toggle_mode(self, mode):
        """Switch between Anti-AFK and Movement mode."""
        if mode == "anti_afk":
            self.anti_afk_enabled = True
            self.movement_enabled = False
            logging.info("Switched to Anti-AFK mode")
        elif mode == "movement":
            self.anti_afk_enabled = False
            self.movement_enabled = True
            logging.info("Switched to Movement mode")


def check_and_install_dependencies():
    """Check and install required dependencies."""
    # Implement dependency checks if necessary
    try:
        # Check Google Chrome version
        chrome_version = get_chrome_version()
        log_success(f"Google Chrome version detected: {chrome_version}")

        # Check or install ChromeDriver
        if not os.path.exists("chromedriver/chromedriver"):
            log_info("ChromeDriver not found. Downloading...")
            download_chromedriver(chrome_version)
        else:
            log_success("ChromeDriver already exists.")
    except Exception as e:
        log_error(f"Dependency check failed: {e}")
        raise


def get_chrome_version():
    """Get the version of installed Google Chrome."""
    log_info("Checking Google Chrome version...")
    try:
        system = platform.system()
        if system == "Windows":
            command = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
            version = subprocess.check_output(command, shell=True).decode().strip()
            return version.split()[-1]
        elif system == "Darwin":  # macOS
            command = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version"
            version = subprocess.check_output(command, shell=True).decode().strip()
            return version.split()[-1]
        elif system == "Linux":
            command = "google-chrome --version"
            version = subprocess.check_output(command, shell=True).decode().strip()
            return version.split()[-1]
        else:
            raise Exception("Unsupported Operating System")
    except Exception as e:
        log_error(f"Could not detect Google Chrome version: {e}")
        raise


def download_chromedriver(chrome_version):
    """Download the ChromeDriver that matches the installed Google Chrome version."""
    try:
        log_info("Determining the correct ChromeDriver version...")
        major_version = chrome_version.split(".")[0]
        url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
        latest_driver_version = requests.get(url).text.strip()

        system = platform.system().lower()
        if system == 'darwin':
            system = 'mac64'  # For macOS
        elif system == 'windows':
            system = 'win32'
        elif system == 'linux':
            system = 'linux64'
        else:
            raise Exception("Unsupported Operating System for ChromeDriver")

        driver_download_url = f"https://chromedriver.storage.googleapis.com/{latest_driver_version}/chromedriver_{system}.zip"
        log_info(f"Downloading ChromeDriver from: {driver_download_url}")

        response = requests.get(driver_download_url, stream=True)
        zip_path = "chromedriver.zip"
        with open(zip_path, "wb") as file:
            file.write(response.content)

        # Extract the downloaded zip
        log_info("Extracting ChromeDriver...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall("chromedriver")

        # Clean up
        os.remove(zip_path)
        chromedriver_path = os.path.abspath("chromedriver/chromedriver")
        log_success(f"ChromeDriver downloaded and available at: {chromedriver_path}")
        return chromedriver_path
    except Exception as e:
        log_error(f"Failed to download ChromeDriver: {e}")
        raise
