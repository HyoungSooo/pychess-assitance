import io
from PIL import Image
from board_to_fen.KerasNeuralNetwork import KerasNeuralNetwork
from board_to_fen.utils import Decoder_FEN, Tiler
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
from board_to_fen import saved_models

import torchvision.transforms.functional as F
from torchvision.io import read_image
import torch


def get_model():
    net = KerasNeuralNetwork()

    return net


def get_fen_from_image_path(image_path, end_of_row='/', black_view=False) -> str:
    image = Image.open(image_path)
    decoder = Decoder_FEN()
    net = KerasNeuralNetwork()
    f = pkg_resources.open_text(saved_models, 'november_model')
    net.load_model(f.name)
    tiler = Tiler()
    tiles = tiler.get_tiles(img=image)
    predictions = net.predict(tiles=tiles)
    fen = decoder.fen_decode(
        squares=predictions, end_of_row=end_of_row, black_view=black_view)

    print(fen)
    return fen


label_to_piece = ['-', 'r', 'n', 'b', 'q',
                  'k', 'p', 'R', 'N', 'B', 'Q', 'K', 'P']


def board_array_to_fen(board_array):
    fen = ''
    for row in range(8):
        counter = 0
        for col in range(8):
            if board_array[row][col] == '-':
                counter += 1
            else:
                if counter != 0:
                    fen += str(counter)
                    counter = 0
                fen += board_array[row][col]
        if counter != 0:
            fen += str(counter)
            counter = 0
        if row != 7:
            fen += '-'
    return fen


def image_to_predicted_fen(image_tensor, model):
    board_array = [[' ' for _ in range(8)] for _ in range(8)]

    for row in range(8):
        for col in range(8):
            tile = image_tensor[:, row*50:(row+1)*50,
                                col*50:(col+1)*50].unsqueeze(0).float()
            _, prediction = model(tile).max(1)
            board_array[row][col] = label_to_piece[prediction]

    return board_array_to_fen(board_array)


def predict(image_path, model):
    img_tensor = read_image(image_path)[:3, :, :]
    img_tensor = F.resize(img_tensor, 400)
    fen = image_to_predicted_fen(img_tensor, model).replace('-', '/')
    print(fen)
    return fen
