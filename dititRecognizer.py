import numpy as np
import tensorflow as tf
import pygame
import os
import matplotlib.pyplot as plt

GAME_WIDTH = 420
GAME_HEIGHT = 420
os.environ['SDL_VIDEO_CENTERED'] = '1'
GAME_WINDOW = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Digit Recognizer App")
pygame.init()


class Tile:

    def __init__(self, row, col, width, totalRows):
        self.row = row
        self.col = col
        self.width = width
        self.totalRows = totalRows
        self.x = row * width
        self.y = col * width
        self.colour = (0, 0, 0)
        self.calculated = False

    def getPos(self):
        return self.row, self.col

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))


def makeGrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            tile = Tile(i, j, gap, width)
            grid[i].append(tile)
    return grid


def drawGrid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, (0, 0, 255), (0, i * gap), (width, i * gap))
        pygame.draw.line(win, (0, 0, 255), (i * gap, 0), (i * gap, width))


def draw(win, grid, rows, width):
    win.fill((255, 255, 255))

    for row in grid:
        for tile in row:
            tile.draw(win)

    drawGrid(win, rows, width)
    pygame.display.update()


def getClickedPosition(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def resetGame(grid, rows):
    for i in range(rows):
        for j in range(rows):
            grid[i][j].colour = (0, 0, 0)
            grid[i][j].calculated = False


# Function used to train the model
# def trainModel():
#     data = tf.keras.datasets.mnist
#     (x_train, y_train), (x_test, y_test) = data.load_data()
#     x_train = tf.keras.utils.normalize(x_train, axis=1)
#     x_test = tf.keras.utils.normalize(x_test, axis=1)
#
#     model = tf.keras.models.Sequential()
#     model.add(tf.keras.layers.Flatten())
#     model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
#     model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
#     model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
#
#     model.compile(optimizer='adam',
#                   loss='sparse_categorical_crossentropy',
#                   metrics=['accuracy'])
#
#     model.fit(x_train, y_train, epochs=3)
#     model.save('model')


def verifyDigit(model, digit):
    digit = tf.keras.utils.normalize(digit, axis=1)
    digit = digit.astype('float32')
    digit = digit.reshape(1, 28, 28, 1)
    prediction = model.predict(digit)
    import ctypes
    ctypes.windll.user32.MessageBoxW(0, f'Predicted digit: {np.argmax(prediction)}', "Predicted digit", 0)


def main(win, width):
    ROWS = 28
    model = tf.keras.models.load_model('model')
    digitValuesArray = np.zeros((28, 28))
    grid = makeGrid(ROWS, width)
    running = True
    draw(win, grid, ROWS, width)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = getClickedPosition(pos, ROWS, width)
                (grid[row][col]).colour = (255, 255, 255)
                if ROWS-1 > row > 1 and ROWS-1 > col > 1:
                    nearRowTile = [row, row-1, row+1]
                    nearColTile = [col, col-1, col+1]
                    for r in nearRowTile:
                        for c in nearColTile:
                            (grid[r][c]).colour = (255, 255, 255)

                for i in range(ROWS):
                    for j in range(ROWS):
                        if grid[j][i].colour == (255, 255, 255) and grid[i][j].calculated is False:
                            grid[i][j].calculated = True
                            digitValuesArray[i][j] = 255
                draw(win, grid, ROWS, width)

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = getClickedPosition(pos, ROWS, width)
                (grid[row][col]).colour = (0, 0, 0)

                for i in range(ROWS):
                    for j in range(ROWS):
                        if grid[j][i].colour == (0, 0, 0) and grid[i][j].calculated is True:
                            grid[i][j].calculated = False
                            digitValuesArray[i][j] = 0
                draw(win, grid, ROWS, width)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    resetGame(grid, ROWS)
                    digitValuesArray = np.zeros((28, 28))
                    draw(win, grid, ROWS, width)

                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_e:
                    verifyDigit(model, digitValuesArray)

        draw(win, grid, ROWS, width)


if __name__ == "__main__":
    main(GAME_WINDOW, GAME_WIDTH)
