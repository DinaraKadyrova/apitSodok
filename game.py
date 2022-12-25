import random
import pygame

WIDTH = 800
ROWS = 8

CYAN = pygame.image.load('src/blue.png')        # изображение шашек противника
YELLOW = pygame.image.load('src/yellow.png')    # изображение шашек игрока

WHITE = (255, 255, 255)    # цвет поля
BLACK = (0, 0, 0)          # цвет поля
ORANGE = (235, 168, 52)    # цвет подсвечивания
BLUE = (76, 252, 241)      # цвет подсвечивания

WIN = None

priorMoves = []
pieces = {"Y": [], "C": []}


class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.piece = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / ROWS, WIDTH / ROWS))
        if self.piece:
            WIN.blit(self.piece.image, (self.x, self.y))


def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

# зарисовка поля и расстановка шашек
def make_grid(rows, width):
    grid = []
    gap = width // rows
    count = 0
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)
            if abs(i - j) % 2 == 0:
                node.colour = BLACK
            if i == 0 or i == 2:
                piece = Piece('C')
                node.piece = piece
                pieces["C"].append(piece)
            elif i == rows - 3 or i == rows - 1:
                piece = Piece('Y')
                node.piece = piece
                pieces["Y"].append(piece)
            count += 1
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // ROWS
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))


class Piece:   # класс шашек
    def __init__(self, team):
        self.team = team
        self.image = CYAN if self.team == 'C' else YELLOW

    def draw(self, x, y):
        WIN.blit(self.image, (x, y))


# определяет по какой плитке кликнули
def getNode(grid, rows, width):
    gap = width // rows
    RowX, RowY = pygame.mouse.get_pos()
    Row = RowX // gap
    Col = RowY // gap
    return (Col, Row)


# убирает подсвечивание возможного хода
def resetColours(grid, node):
    positions = generatePotentialMoves(node, grid)
    positions.append(node)

    for colouredNodes in positions:
        nodeX, nodeY = colouredNodes
        grid[nodeX][nodeY].colour = BLACK if abs(nodeX - nodeY) % 2 == 0 else WHITE

# подсвечивает возможный ход
def HighlightpotentialMoves(piecePosition, grid):
    positions = generatePotentialMoves(piecePosition, grid)
    for position in positions:
        Column, Row = position
        grid[Column][Row].colour = BLUE

# определяет чей ход
def opposite(team):
    return "C" if team == "Y" else "Y"


# возвращает координаты возможных ходов
def generatePotentialMoves(nodePosition, grid):
    positions = []
    column, row = nodePosition

    current_row = row
    while current_row >= 1:
        current_row -= 1
        if grid[column][current_row].piece:
            break
        positions.append((column, current_row))
    current_row = row
    while current_row <= 6:
        current_row += 1
        if grid[column][current_row].piece:
            break
        positions.append((column, current_row))

    current_column = column
    while current_column >= 1:
        current_column -= 1
        if grid[current_column][row].piece:
            break
        positions.append((current_column, row))
    current_column = column
    while current_column <= 6:
        current_column += 1
        if grid[current_column][row].piece:
            break
        positions.append((current_column, row))

    return positions


# подсвечивает нажатую клетку
def highlight(ClickedNode, Grid, OldHighlight):
    Column, Row = ClickedNode
    Grid[Column][Row].colour = ORANGE
    if OldHighlight:
        resetColours(Grid, OldHighlight)
    HighlightpotentialMoves(ClickedNode, Grid)
    return (Column, Row)

# удаляет шашку
def remove_piece(piece: Piece):
    pieces[piece.team].remove(piece)

# проверка хода по правилам игры
def cut(grid, column, row, team):
    try:
        if row > 0 < 7:
            if grid[column][row - 1].piece.team != team and grid[column][row].piece.team == team \
                    and grid[column][row + 1].piece.team != team:
                remove_piece(grid[column][row - 1].piece)
                grid[column][row - 1].piece = None
                remove_piece(grid[column][row + 1].piece)
                grid[column][row + 1].piece = None
    except:
        pass
    try:
        if column > 0 < 7:
            if grid[column - 1][row].piece.team != team and grid[column][row].piece.team == team \
                    and grid[column + 1][row].piece.team != team:
                remove_piece(grid[column - 1][row].piece)
                grid[column - 1][row].piece = None
                remove_piece(grid[column + 1][row].piece)
                grid[column + 1][row].piece = None
    except:
        pass

    try:
        if row <= 5:
            if grid[column][row].piece.team == team and grid[column][row + 1].piece.team != team \
                    and grid[column][row + 2].piece.team == team:
                remove_piece(grid[column][row + 1].piece)
                grid[column][row + 1].piece = None
    except:
        pass
    try:
        if row >= 2:
            if grid[column][row].piece.team == team and grid[column][row - 1].piece.team != team \
                    and grid[column][row - 2].piece.team == team:
                remove_piece(grid[column][row - 1].piece)
                grid[column][row - 1].piece = None
    except:
        pass
    try:
        if column <= 5:
            if grid[column][row].piece.team == team and grid[column + 1][row].piece.team != team \
                    and grid[column + 2][row].piece.team == team:
                remove_piece(grid[column + 1][row].piece)
                grid[column + 1][row].piece = None
    except:
        pass
    try:
        if column >= 2:
            if grid[column][row].piece.team == team and grid[column - 1][row].piece.team != team \
                    and grid[column - 2][row].piece.team == team:
                remove_piece(grid[column - 1][row].piece)
                grid[column - 1][row].piece = None
    except:
        pass
# определяет победителя
def check_win(grid):
    count = {"C": 0, "Y": 0}
    for i in range(8):
        for j in range(8):
            if grid[i][j].piece:
                count[grid[i][j].piece.team] += 1
    if count["C"] == 0:
        return "Вы победили!"
    elif count["Y"] == 0:
        return "Вы проиграли"
    return ""

# ход компьютера
def random_step(grid):
    try:
        node = None
        positions = []
        while len(positions) == 0:
            piece = pieces["C"][random.randint(0, len(pieces["C"])-1)]
            for i in range(8):
                for j in range(8):
                    if grid[i][j].piece:
                        if piece is grid[i][j].piece:
                            node = (i, j)
            positions = generatePotentialMoves(node, grid)
        move(grid, node, positions[random.randint(0, len(positions)-1)])
    except:
        pass

# переставляет шашку
def move(grid, piecePosition, newPosition):
    resetColours(grid, piecePosition)
    newColumn, newRow = newPosition
    oldColumn, oldRow = piecePosition

    piece = grid[oldColumn][oldRow].piece
    grid[newColumn][newRow].piece = piece
    grid[oldColumn][oldRow].piece = None

    cut(grid, newColumn, newRow, piece.team)
    win = check_win(grid)
    return opposite(grid[newColumn][newRow].piece.team)


def main(result, WIDTH=800, ROWS=8):
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption('Апит Содок')
    grid = make_grid(ROWS, WIDTH)
    highlightedPiece = None
    currMove = 'Y'

    while True:
        result[0] = check_win(grid)
        if result[0] != "":
            pygame.display.quit()
            pygame.quit()
            return
        if currMove == "C":
            random_step(grid)
            currMove = "Y"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:      # работа мышки
                clickedNode = getNode(grid, ROWS, WIDTH)
                ClickedPositionColumn, ClickedPositionRow = clickedNode
                if grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE:
                    if highlightedPiece:
                        pieceColumn, pieceRow = highlightedPiece
                    if currMove == grid[pieceColumn][pieceRow].piece.team:
                        resetColours(grid, highlightedPiece)
                        currMove = move(grid, highlightedPiece, clickedNode)
                elif highlightedPiece == clickedNode:
                    pass
                else:
                    if grid[ClickedPositionColumn][ClickedPositionRow].piece:
                        if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                            highlightedPiece = highlight(clickedNode, grid, highlightedPiece)

        update_display(WIN, grid, ROWS, WIDTH)

if __name__ == "__main__":
    res = [None]
    main(res, WIDTH, ROWS)