import pyautogui as pag
import keyboard
import time
from io import BytesIO
from PIL import Image
from datetime import datetime


class Position:
    def __init__(self, path='.'):
        self.left_x = None
        self.left_y = None
        self.right_x = None
        self.right_y = None
        self.filepath = path
        self.counter = 0

    def __check_position(self, value):
        if not self.left_x or not self.left_y:
            self.reset()
            raise ValueError(
                'left postion must be seted before set rigth position')

        if self.left_y > value.y or self.left_x > value.x:
            self.reset()
            raise ValueError(
                f'right postion must be bigger then left position left => {self.left_x}, {self.left_y}, rigth = {value.x}, {value.y}')

    def set_left_position(self, right=False):
        while True:
            if keyboard.is_pressed("`"):
                pos = pag.position()
                time.sleep(0.2)
                break
        if right:
            return pos

        self.left_x = pos.x
        self.left_y = pos.y

    def set_right_position(self):

        position = self.set_left_position(right=True)

        self.__check_position(position)

        self.right_x = position.x - self.left_x
        self.right_y = position.y - self.left_y

    def capture(self):
        try:
            pag.screenshot(self.filepath + f'/{self.counter}.png', region=(
                self.left_x, self.left_y, self.right_x, self.right_y))
            image = Image.open(self.filepath + f'/{self.counter}.png')
            output = BytesIO()
            image = image.resize((400, 400))
            image.convert("RGB").save(output, "BMP")
            output.close()
            self.counter += 1
        except:
            self.reset()
            raise ValueError('set left, rigth postion first')

    def reset(self):
        self.left_x = None
        self.left_y = None
        self.right_x = None
        self.right_y = None
