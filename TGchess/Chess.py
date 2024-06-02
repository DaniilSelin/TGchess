import numpy as np
import copy

class Board():
    def __init__(self, black_stuff, white_stuff):
        self.board = np.zeros((8,8),dtype = str)
        self.tegs = np.zeros((8,8),dtype = int)
        self.black_stuff = black_stuff
        self.white_stuff = white_stuff
        self.simulation = 0 #если симуляция то 1\ инчае 0
        self.status_game = -1 # 1 - white/ -1 - black
        self.status_check = 0 # 1 - yep/ 0 - no
        self.status_mate = 0 # 1 - yep
        self.status_pat = 0
        #comit
        self.status_drawn = 0 #ничья

    def build(self):
        for figure in self.black_stuff:
            self.board[figure.position[0],figure.position[1]] = figure.gettype
            self.tegs[figure.position[0], figure.position[1]] = figure.color
        for figure in self.white_stuff:
            self.board[figure.position[0], figure.position[1]] = figure.gettype
            self.tegs[figure.position[0], figure.position[1]] = figure.color

    def search_board(self,position):
        #описк фигуры с такой позицией
        if self.status_game == -1:
            for item in self.black_stuff:
                if item.position == position:
                    return item
        else:
            for item in self.white_stuff:
                if item.position == position:
                    return item

def check(game):
    #place of king
    #так как после смены хода еще не обновиллся статус игры
    if game.status_game == 1:
        position_queen = game.black_stuff[-1].position
        #comit
        for figure in game.white_stuff:
            if figure.gettype == "Pown" and game.simulation == 0:
                if figure.virginity != 3:
                    figure.virginity -=1
            game.status_check -= 1
            pos_array = figure.motion(game)
            game.status_check += 1
            for pos in pos_array:
                if pos == position_queen:
                    game.status_check = 1
                    if game.simulation == 0:
                        mate(game)
                    return 1
    else:
        position_queen = game.white_stuff[-1].position
        #comit
        for figure in game.black_stuff:
            if figure.gettype == "Pown" and game.simulation == 0:
                if figure.virginity != 3:
                    figure.virginity -= 1
            game.status_check -= 1
            pos_array = figure.motion(game)
            game.status_check +=1
            #смотрим есть ли свопадения
            for pos in pos_array:
                if pos == position_queen:
                    game.status_check = 1
                    if game.simulation == 0:
                        mate(game)
                    return 1
    game.status_check = 0
    return 0

def mate(game):
    ability = []
    if game.status_game == 1:
        game.status_game *= -1
        for figure in game.black_stuff:
            game.status_check -= 1
            ability += figure.motion(game)
            game.status_check += 1
        game.status_game *= -1

    else:
        game.status_game *= -1
        for figure in game.white_stuff:
            game.status_check -= 1
            ability += figure.motion(game)
            game.status_check +=1
        game.status_game *= -1
    if len(ability) == 0:
        game.status_mate = 1

def pat(game):
    #comit
    if len(game.white_stuff) == 1 and len(game.black_stuff) == 1:
        game.status_drawn = 1

    ability = []
    if game.status_game == 1:
        game.status_game *= -1
        for figure in game.black_stuff:
            game.status_check -= 1
            ability += figure.motion(game)
            game.status_check += 1
        game.status_game *= -1
    else:
        game.status_game *= -1
        for figure in game.white_stuff:
            game.status_check -= 1
            ability += figure.motion(game)
            game.status_check += 1
        game.status_game *= -1
    if len(ability) == 0:
        game.status_pat = 1

def separeted(game, position_new_array, position, color):
    if game.simulation == 1:
        pass
    else:
        for tern in position_new_array[:]:
            new_white_stuff = []
            for figure in game.white_stuff:
                new_white_stuff.append(copy.deepcopy(figure))
            new_black_stuff = []
            for figure in game.black_stuff:
                new_black_stuff.append(copy.deepcopy(figure))

            new_game = Board(new_black_stuff, new_white_stuff)
            if game.status_game == 1:
                new_game.status_game = 1  # 1 - white/ -1 - black
            else:
                new_game.status_game = -1

            new_game.status_check = 1
            new_game.simulation = 1
            new_game.build()
            # находим эту фигурув новом списке и меняем координаты
            figure = game.search_board([position[0], position[1]])
            if game.status_game == 1:
                index = game.white_stuff.index(figure)
                new_white_stuff[index].interactive(tern, position, new_game)
            else:
                index = game.black_stuff.index(figure)
                new_black_stuff[index].interactive(tern, position, new_game)

            check(new_game)
            if new_game.status_check == 1:
                position_new_array.remove(tern)
    return position_new_array

class Figure():
    def __init__(self, position, color):
        self.color = color
        # 1 - white | -1 - black
        self.position = position
        # [вертикаль, горизонталь]

class Pawn(Figure):
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.virginity = 3 # использовалось ли право хода на две клетки >1 - более хода назад/ 2 - зод назад/ 2 - нет,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

    @property
    def gettype(self):
        return "Pown"

    def motion(self, game):
        position_new_array = []

        if self.position[0] + 1*self.color <= 7 and self.position[0] + 1 * self.color >= 0:
            #клетка перед пешкой
            if game.board[self.position[0]+1*self.color, self.position[1]] == "" and game.tegs[self.position[0]+1*self.color, self.position[1]] == 0:
                position_new_array += [[self.position[0]+1*self.color, self.position[1]]]

            # кушать
            if self.position[0] + 1 * self.color <= 7 and self.position[1] + 1 * self.color <= 7:
                if game.tegs[self.position[0] + 1 * self.color, self.position[1] + 1 * self.color] == -game.status_game:
                    if self.position[1] + 1 * self.color!= -1:
                        position_new_array += [[self.position[0] + 1 * self.color, self.position[1] + 1 * self.color]]

            if self.position[0] + 1 * self.color <= 7 and self.position[1] - 1 * self.color <= 7:
                if game.tegs[self.position[0] + 1 * self.color, self.position[1] - 1 * self.color] == -game.status_game:
                    if self.position[1] - 1 * self.color!=-1:
                        position_new_array += [[self.position[0] + 1 * self.color, self.position[1] - 1 * self.color]]

        if self.virginity == 3 and game.tegs[self.position[0] + 2 * self.color, self.position[1]] == 0 and game.tegs[self.position[0] + 1 * self.color, self.position[1]] == 0:
            #лвойной ход
            if game.board[self.position[0] + 2 * self.color, self.position[1]] == "":
                position_new_array += [[self.position[0] + 2 * self.color, self.position[1]]]
        elif self.virginity == 1 and game.simulation == 0:
            self.virginity -= 1

        # eat on the dabl move
        #left
        if self.position[1] - 1 * self.color != -1 and self.position[1] - 1 * self.color != 8 and game.tegs[self.position[0], self.position[1] - 1 * self.color] == -game.status_game:
            game.status_game *= -1
            figure = game.search_board([self.position[0], self.position[1] - 1 * self.color])
            game.status_game *= -1
            if figure.gettype == "Pown":
                if figure.virginity == 0:
                    if game.tegs[self.position[0] + 1 * self.color, self.position[1] - 1 * self.color] == 0:
                        position_new_array += [[self.position[0] + 1 * self.color, self.position[1] - 1 * self.color]]
        #right
        if self.position[1] + 1 * self.color != -1 and self.position[1] + 1 * self.color != 8 and game.tegs[self.position[0], self.position[1] + 1 * self.color] == -game.status_game:
            game.status_game *= -1
            figure = game.search_board([self.position[0], self.position[1] + 1 * self.color])
            game.status_game *= -1
            if figure.gettype == "Pown":
                if figure.virginity == 0:
                    if game.tegs[self.position[0] + 1 * self.color, self.position[1] + 1 * self.color] == 0:
                        position_new_array += [[self.position[0] + 1 * self.color, self.position[1] + 1 * self.color]]

        position_new_array = separeted(game, position_new_array, self.position, self.color)

        return position_new_array

    def interactive(self, new_position, last_position, game, /, figure_im="", dabl_eat = 0):

        if (new_position[0]+2 == last_position[0] or new_position[0]-2 == last_position[0]) and game.simulation == 0:
            self.virginity = 4

        #проверяем было взятие или нет, соответственно удаляем вражескую фигуру
        if last_position[1] != new_position[1]:
            if game.status_game == 1:
                game.status_game *= -1
                figure = game.search_board([new_position[0], new_position[1]])
                if figure != None:
                    game.black_stuff.remove(figure)

                figure_2 = game.search_board([new_position[0]-1, new_position[1]])
                if figure_2 != None and figure_2.color == -1:
                    if figure_2.gettype == "Pown":
                        if figure_2.virginity == 0:
                            game.black_stuff.remove(figure_2)
                            dabl_eat = 1
                            game.board[new_position[0]-1, new_position[1]] = ""
                            game.tegs[new_position[0]-1, new_position[1]] = 0
                game.status_game *= -1

            else:
                game.status_game *= -1
                figure = game.search_board([new_position[0], new_position[1]])
                if figure != None:
                    game.white_stuff.remove(figure)

                figure_2 = game.search_board([new_position[0] + 1, new_position[1]])

                if figure_2 != None and figure_2.color == 1:
                    if figure_2.gettype == "Pown":
                        if figure_2.virginity == 0:
                            game.white_stuff.remove(figure_2)
                            dabl_eat = 1
                            game.board[new_position[0] + 1, new_position[1]] = ""
                            game.tegs[new_position[0] + 1, new_position[1]] = 0
                game.status_game *= -1

        game.board[last_position[0], last_position[1]] = ""
        game.tegs[last_position[0], last_position[1]] = 0
        self.position = new_position
        game.board[new_position[0], new_position[1]] = self.gettype
        game.tegs[new_position[0], new_position[1]] = self.color

        if self.virginity != 4 and game.simulation == 0:
            self.virginity = 0
        else:
            if game.simulation == 0:
                self.virginity = 2

        if new_position[0] == 0 and game.simulation == 0:
            figure = game.search_board(self.position)
            print(figure, figure.color, figure.position)
            game.black_stuff.remove(figure)
            exec(f'game.black_stuff.insert(-2, {figure_im}(new_position, -1))')
        elif new_position[0] == 7 and game.simulation == 0:
            figure = game.search_board(self.position)
            game.white_stuff.remove(figure)
            exec(f'game.white_stuff.insert(-2,  {figure_im}(new_position, 1))')

        if game.simulation == 0:
            pat(game)
            check(game)


        game.status_game *= -1
        return dabl_eat

class Rook(Figure):
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.virginity = 0  #смещалась ли ладья/ 1-да/ 0 - нет

    @property
    def gettype(self):
        return "Rook"

    def motion(self, game):

        position_new_array = []
        top = bot = right = left = 1

        for num in range(1, 8):
            #для белых
            if self.color == 1:
                #клетки сверху
                if self.position[0] + num*self.color < 8 and top == 1:
                    if game.tegs[
                        self.position[0] + num*self.color, self.position[1]
                    ] == -game.status_game:
                        top = 0
                        position_new_array += [[self.position[0] + num*self.color, self.position[1]]]

                    elif game.tegs[
                        self.position[0] + num*self.color, self.position[1]
                    ] == 0:
                        position_new_array += [[self.position[0] + num * self.color, self.position[1]]]

                    else:
                        top = 0
                #клетки снизу
                if self.position[0] - num*self.color >= 0 and bot == 1:

                    if game.tegs[
                        self.position[0] - num*self.color, self.position[1]
                    ] == -game.status_game:
                        bot = 0
                        position_new_array += [[self.position[0] - num*self.color, self.position[1]]]

                    elif game.tegs[
                        self.position[0] - num*self.color, self.position[1]
                    ] == 0:
                        position_new_array += [[self.position[0] - num*self.color, self.position[1]]]

                    else:
                        bot = 0
                #клетки слева
                if self.position[1] - num*self.color >= 0 and left == 1:

                    if game.tegs[
                        self.position[0], self.position[1] - num*self.color
                    ] == -game.status_game:
                        left = 0
                        position_new_array += [[self.position[0], self.position[1] - num*self.color]]

                    elif game.tegs[
                        self.position[0], self.position[1] - num*self.color
                    ] == 0:
                        position_new_array += [[self.position[0], self.position[1] - num*self.color]]

                    else:
                        left = 0
                #клетки справа
                if self.position[1] + num*self.color < 8 and right == 1:

                    if game.tegs[
                        self.position[0], self.position[1] + num*self.color
                    ] == -game.status_game:
                        right = 0
                        position_new_array += [[self.position[0], self.position[1] + num*self.color]]

                    elif game.tegs[
                        self.position[0], self.position[1] + num*self.color
                    ] == 0:
                        position_new_array += [[self.position[0], self.position[1] + num*self.color]]

                    else:
                        right = 0

            else:
                #для черных
                #клетки снизу
                if self.position[0] + num * self.color >= 0 and bot == 1:

                    if game.tegs[
                        self.position[0] + num * self.color, self.position[1]
                    ] == -game.status_game:
                        bot = 0
                        position_new_array += [[self.position[0] + num * self.color, self.position[1]]]

                    elif game.tegs[
                        self.position[0] + num * self.color, self.position[1]
                    ] == 0:
                        position_new_array += [[self.position[0] + num * self.color, self.position[1]]]

                    else:
                        bot = 0
                #клетки сверху
                if self.position[0] - num * self.color < 8 and top == 1:

                    if game.tegs[
                        self.position[0] - num * self.color, self.position[1]
                    ] == -game.status_game:
                        top = 0
                        position_new_array += [[self.position[0] - num * self.color, self.position[1]]]

                    elif game.tegs[
                        self.position[0] - num * self.color, self.position[1]
                    ] == 0:
                        position_new_array += [[self.position[0] - num * self.color, self.position[1]]]

                    else:
                        top = 0

                #клетки справа
                if self.position[1] - num * self.color < 8 and right == 1:

                    if game.tegs[
                        self.position[0], self.position[1] - num * self.color
                    ] == -game.status_game:
                        right = 0
                        position_new_array += [[self.position[0], self.position[1] - num * self.color]]

                    elif game.tegs[
                        self.position[0], self.position[1] - num * self.color
                    ] == 0:
                        position_new_array += [[self.position[0], self.position[1] - num * self.color]]

                    else:
                        right = 0
                #клетки слева
                if self.position[1] + num * self.color >= 0 and left == 1:

                    if game.tegs[
                        self.position[0], self.position[1] + num * self.color
                    ] == -game.status_game:
                        left = 0
                        position_new_array += [[self.position[0], self.position[1] + num * self.color]]

                    elif game.tegs[
                        self.position[0], self.position[1] + num * self.color
                    ] == 0:
                        position_new_array += [[self.position[0], self.position[1] + num * self.color]]

                    else:
                        left = 0


        position_new_array = separeted(game, position_new_array, self.position, self.color)

        return position_new_array

    def interactive(self, new_position, last_position, game):
        #проверяем была ли вражеская пешка на новой позиции ладьи
        if game.status_game == 1:
            game.status_game *= -1
            figure = game.search_board([new_position[0], new_position[1]])
            if figure != None:
                game.black_stuff.remove(figure)
            game.status_game *= -1
        else:
            game.status_game *= -1
            figure = game.search_board([new_position[0], new_position[1]])
            if figure != None:
                game.white_stuff.remove(figure)
            game.status_game *= -1

        game.board[last_position[0], last_position[1]] = ""
        game.tegs[last_position[0], last_position[1]] = 0
        self.position = new_position
        game.board[new_position[0], new_position[1]] = self.gettype
        game.tegs[new_position[0], new_position[1]] = self.color

        self.virginity = 1

        if game.simulation == 0:
            check(game)
            pat(game)

        game.status_game *= -1

class Knight(Figure):
    def __init__(self, position, color):
        self.position = position
        self.color = color

    @property
    def gettype(self):
        return "Knight"

    def motion(self, game):
        new_action_array = []
        if self.color == 1:
            #для белый
            #ходы сверху
            if self.position[0] + 2 < 8:
                #вверхний правый
                if self.position[1] + 1*self.color < 8:
                    if game.tegs[self.position[0] + 2 * self.color, self.position[1] + 1 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] + 2 * self.color, self.position[1] + 1 * self.color]]
                #вверхний левый
                if self.position[1] - 1 * self.color >= 0:
                    if game.tegs[self.position[0] + 2 * self.color, self.position[1] - 1 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] + 2 * self.color, self.position[1] - 1 * self.color]]

            # ходы снизу
            if self.position[0] - 2 * self.color >= 0:
                # снизу правый
                if self.position[1] + 1 * self.color < 8:
                    if game.tegs[self.position[0] - 2 * self.color, self.position[1] + 1 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] - 2 * self.color, self.position[1] + 1 * self.color]]
                # снизу левый
                if self.position[1] - 1 * self.color >= 0:
                    if game.tegs[self.position[0] - 2 * self.color, self.position[1] - 1 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] - 2 * self.color, self.position[1] - 1 * self.color]]

            #справа
            if self.position[1] + 2*self.color < 8:
                # вверхний правый
                if self.position[0] + 1*self.color < 8:
                    if game.tegs[self.position[0] + 1 * self.color, self.position[1] + 2 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] + 1 * self.color, self.position[1] + 2 * self.color]]
                # нижний правый
                if self.position[0] - 1*self.color >= 0:
                    if game.tegs[self.position[0] - 1 * self.color, self.position[1] + 2 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] - 1 * self.color, self.position[1] + 2 * self.color]]

            # слева
            if self.position[1] - 2 * self.color >= 0:
                # сверзу левый
                if self.position[0] + 1*self.color < 8:
                    if game.tegs[self.position[0] + 1 * self.color, self.position[1] - 2 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] + 1 * self.color, self.position[1] - 2 * self.color]]
                # снизу левый
                if self.position[0] - 1 * self.color >= 0:
                    if game.tegs[self.position[0] - 1 * self.color, self.position[1] - 2 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] - 1 * self.color, self.position[1] - 2 * self.color]]

        if self.color == -1:
            #для чёрных
            #ходы сверху
            if self.position[0] + 2*self.color >= 0:
                #вверхний правый
                if self.position[1] + 1 * self.color >= 0:
                    if game.tegs[self.position[0] + 2 * self.color, self.position[1] + 1 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] + 2 * self.color, self.position[1] + 1 * self.color]]
                #вверхний левый
                if self.position[1] - 1*self.color < 8:
                    if game.tegs[self.position[0] + 2 * self.color, self.position[1] - 1 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] + 2 * self.color, self.position[1] - 1 * self.color]]

            # ходы снизу
            if self.position[0] - 2*self.color < 8:
                # снизу правый
                if self.position[1] + 1 * self.color >= 0:
                    if game.tegs[self.position[0] - 2 * self.color, self.position[1] + 1 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] - 2 * self.color, self.position[1] + 1 * self.color]]
                # снизу левый
                if self.position[1] - 1*self.color < 8:
                    if game.tegs[self.position[0] - 2 * self.color, self.position[1] - 1 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] - 2 * self.color, self.position[1] - 1 * self.color]]

            #справа
            if self.position[1] + 2 * self.color >= 0:
                # вверхний правый
                if self.position[0] + 1 * self.color >= 0:
                    if game.tegs[self.position[0] + 1 * self.color, self.position[1] + 2 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] + 1 * self.color, self.position[1] + 2 * self.color]]
                # нижний правый
                if self.position[0] - 1*self.color < 8:
                    if game.tegs[self.position[0] - 1 * self.color, self.position[1] + 2 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] - 1 * self.color, self.position[1] + 2 * self.color]]

            # слева
            if self.position[1] - 2*self.color < 8:
                # сверзу левый
                if self.position[0] + 1 * self.color >= 0:
                    if game.tegs[self.position[0] + 1 * self.color, self.position[1] - 2 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] + 1 * self.color, self.position[1] - 2 * self.color]]
                # снизу левый
                if self.position[0] - 1*self.color < 8:
                    if game.tegs[self.position[0] - 1 * self.color, self.position[1] - 2 * self.color] != game.status_game:
                        new_action_array += [[self.position[0] - 1 * self.color, self.position[1] - 2 * self.color]]

        new_action_array = separeted(game, new_action_array, self.position, self.color)

        return new_action_array

    def interactive(self, new_position, last_position, game):
        # проверяем была ли вражеская фигура на новой позиции
        if game.status_game == 1:
            game.status_game *= -1
            figure = game.search_board([new_position[0], new_position[1]])
            if figure != None:
                game.black_stuff.remove(figure)
            game.status_game *= -1
        else:
            game.status_game *= -1
            figure = game.search_board([new_position[0], new_position[1]])
            if figure != None:
                game.white_stuff.remove(figure)
            game.status_game *= -1

        game.board[last_position[0], last_position[1]] = ""
        game.tegs[last_position[0], last_position[1]] = 0
        self.position = new_position
        game.board[new_position[0], new_position[1]] = self.gettype
        game.tegs[new_position[0], new_position[1]] = self.color

        if game.simulation == 0:
            check(game)
            pat(game)

        game.status_game *= -1

class Bishop(Figure):
    def __init__(self, position, color):
        self.position = position
        self.color = color

    @property
    def gettype(self):
        return "Bishop"

    def motion(self, game):
        position_new_array = []
        right_bot = left_bot = left_top = right_top = 1
        #превая верхняя диагональ
        for num in range(1, 8):

            # для белых
            # right bot
            if self.position[0] + num < 8 and self.position[1] + num < 8 and right_bot == 1:
                if game.tegs[
                    self.position[0] + num, self.position[1] + num
                ] == -game.status_game:
                    right_bot = 0
                    position_new_array += [[self.position[0] + num, self.position[1] + num]]
                elif game.tegs[
                    self.position[0] + num, self.position[1] + num
                ] == 0:
                    position_new_array += [[self.position[0] + num, self.position[1] + num]]
                else:
                    right_bot = 0
            # right_top
            if self.position[0] + num < 8 and self.position[1] - num >= 0 and right_top == 1:
                if game.tegs[
                    self.position[0] + num, self.position[1] - num
                ] == -game.status_game:
                    right_top = 0
                    position_new_array += [[self.position[0] + num, self.position[1] - num]]
                elif game.tegs[
                    self.position[0] + num, self.position[1] - num
                ] == 0:
                    position_new_array += [[self.position[0] + num, self.position[1] - num]]
                else:
                    right_top = 0
            # left bot
            if self.position[0] - num >= 0 and self.position[1] + num < 8 and left_bot == 1:
                if game.tegs[
                    self.position[0] - num, self.position[1] + num
                ] == -game.status_game:
                    left_bot = 0
                    position_new_array += [[self.position[0] - num, self.position[1] + num]]
                elif game.tegs[
                    self.position[0] - num, self.position[1] + num
                ] == 0:
                    position_new_array += [[self.position[0] - num, self.position[1] + num]]
                else:
                    left_bot = 0
            # left_top
            if self.position[0] - num >= 0 and self.position[1] - num >= 0 and left_top == 1:
                if game.tegs[
                    self.position[0] - num, self.position[1] - num
                ] == -game.status_game:
                    left_top = 0
                    position_new_array += [[self.position[0] - num, self.position[1] - num]]
                elif game.tegs[
                    self.position[0] - num, self.position[1] - num
                ] == 0:
                    position_new_array += [[self.position[0] - num, self.position[1] - num]]
                else:
                    left_top = 0

        position_new_array = separeted(game, position_new_array, self.position, self.color)

        return position_new_array

    def interactive(self, new_position, last_position, game):
        #проверяем была ли вражеская пешка на новой позиции ладьи
        if game.status_game == 1:
            game.status_game *= -1
            figure = game.search_board([new_position[0], new_position[1]])
            if figure != None:
                game.black_stuff.remove(figure)
            game.status_game *= -1
        else:
            game.status_game *= -1
            figure = game.search_board([new_position[0], new_position[1]])
            if figure != None:
                game.white_stuff.remove(figure)
            game.status_game *= -1

        game.board[last_position[0], last_position[1]] = ""
        game.tegs[last_position[0], last_position[1]] = 0
        self.position = new_position
        game.board[new_position[0], new_position[1]] = self.gettype
        game.tegs[new_position[0], new_position[1]] = self.color

        if game.simulation == 0:
            check(game)
            pat(game)

        game.status_game *= -1

class Queen(Figure):
    def __init__(self, position, color):
        self.position = position
        self.color = color

    @property
    def gettype(self):
        return "Queen"

    def motion(self, game):
        position_new_array = []
        top = bot = right = left = 1

        #Quinn = rook
        for num in range(1, 8):
            # для белых
            if self.color == 1:
                # клетки сверху
                if self.position[0] + num * self.color < 8 and top == 1:
                    if game.tegs[
                        self.position[0] + num * self.color, self.position[1]
                    ] == -game.status_game:
                        top = 0
                        position_new_array += [[self.position[0] + num * self.color, self.position[1]]]

                    elif game.tegs[
                        self.position[0] + num * self.color, self.position[1]
                    ] == 0:
                        position_new_array += [[self.position[0] + num * self.color, self.position[1]]]

                    else:
                        top = 0
                # клетки снизу
                if self.position[0] - num * self.color >= 0 and bot == 1:

                    if game.tegs[
                        self.position[0] - num * self.color, self.position[1]
                    ] == -game.status_game:
                        bot = 0
                        position_new_array += [[self.position[0] - num * self.color, self.position[1]]]

                    elif game.tegs[
                        self.position[0] - num * self.color, self.position[1]
                    ] == 0:
                        position_new_array += [[self.position[0] - num * self.color, self.position[1]]]

                    else:
                        bot = 0
                # клетки слева
                if self.position[1] - num * self.color >= 0 and left == 1:

                    if game.tegs[
                        self.position[0], self.position[1] - num * self.color
                    ] == -game.status_game:
                        left = 0
                        position_new_array += [[self.position[0], self.position[1] - num * self.color]]

                    elif game.tegs[
                        self.position[0], self.position[1] - num * self.color
                    ] == 0:
                        position_new_array += [[self.position[0], self.position[1] - num * self.color]]

                    else:
                        left = 0
                # клетки справа
                if self.position[1] + num * self.color < 8 and right == 1:

                    if game.tegs[
                        self.position[0], self.position[1] + num * self.color
                    ] == -game.status_game:
                        right = 0
                        position_new_array += [[self.position[0], self.position[1] + num * self.color]]

                    elif game.tegs[
                        self.position[0], self.position[1] + num * self.color
                    ] == 0:
                        position_new_array += [[self.position[0], self.position[1] + num * self.color]]

                    else:
                        right = 0

            else:
                # для черных
                # клетки снизу
                if self.position[0] + num * self.color >= 0 and bot == 1:

                    if game.tegs[
                        self.position[0] + num * self.color, self.position[1]
                    ] == -game.status_game:
                        bot = 0
                        position_new_array += [[self.position[0] + num * self.color, self.position[1]]]

                    elif game.tegs[
                        self.position[0] + num * self.color, self.position[1]
                    ] == 0:
                        position_new_array += [[self.position[0] + num * self.color, self.position[1]]]

                    else:
                        bot = 0
                # клетки сверху
                if self.position[0] - num * self.color < 8 and top == 1:

                    if game.tegs[
                        self.position[0] - num * self.color, self.position[1]
                    ] == -game.status_game:
                        top = 0
                        position_new_array += [[self.position[0] - num * self.color, self.position[1]]]

                    elif game.tegs[
                        self.position[0] - num * self.color, self.position[1]
                    ] == 0:
                        position_new_array += [[self.position[0] - num * self.color, self.position[1]]]

                    else:
                        top = 0

                # клетки справа
                if self.position[1] - num * self.color < 8 and right == 1:

                    if game.tegs[
                        self.position[0], self.position[1] - num * self.color
                    ] == -game.status_game:
                        right = 0
                        position_new_array += [[self.position[0], self.position[1] - num * self.color]]

                    elif game.tegs[
                        self.position[0], self.position[1] - num * self.color
                    ] == 0:
                        position_new_array += [[self.position[0], self.position[1] - num * self.color]]

                    else:
                        right = 0
                # клетки слева
                if self.position[1] + num * self.color >= 0 and left == 1:

                    if game.tegs[
                        self.position[0], self.position[1] + num * self.color
                    ] == -game.status_game:
                        left = 0
                        position_new_array += [[self.position[0], self.position[1] + num * self.color]]

                    elif game.tegs[
                        self.position[0], self.position[1] + num * self.color
                    ] == 0:
                        position_new_array += [[self.position[0], self.position[1] + num * self.color]]

                    else:
                        left = 0

        #Queen = Bishop
        right_bot = left_bot = left_top = right_top = 1
        for num in range(1, 8):

            # для белых
            # right bot
            if self.position[0] + num < 8 and self.position[1] + num < 8 and right_bot == 1:
                if game.tegs[
                    self.position[0] + num, self.position[1] + num
                ] == -game.status_game:
                    right_bot = 0
                    position_new_array += [[self.position[0] + num, self.position[1] + num]]
                elif game.tegs[
                    self.position[0] + num, self.position[1] + num
                ] == 0:
                    position_new_array += [[self.position[0] + num, self.position[1] + num]]
                else:
                    right_bot = 0
            # right_top
            if self.position[0] + num < 8 and self.position[1] - num >= 0 and right_top == 1:
                if game.tegs[
                    self.position[0] + num, self.position[1] - num
                ] == -game.status_game:
                    right_top = 0
                    position_new_array += [[self.position[0] + num, self.position[1] - num]]
                elif game.tegs[
                    self.position[0] + num, self.position[1] - num
                ] == 0:
                    position_new_array += [[self.position[0] + num, self.position[1] - num]]
                else:
                    right_top = 0
            # left bot
            if self.position[0] - num >= 0 and self.position[1] + num < 8 and left_bot == 1:
                if game.tegs[
                    self.position[0] - num, self.position[1] + num
                ] == -game.status_game:
                    left_bot = 0
                    position_new_array += [[self.position[0] - num, self.position[1] + num]]
                elif game.tegs[
                    self.position[0] - num, self.position[1] + num
                ] == 0:
                    position_new_array += [[self.position[0] - num, self.position[1] + num]]
                else:
                    left_bot = 0
            # left_top
            if self.position[0] - num >= 0 and self.position[1] - num >= 0 and left_top == 1:
                if game.tegs[
                    self.position[0] - num, self.position[1] - num
                ] == -game.status_game:
                    left_top = 0
                    position_new_array += [[self.position[0] - num, self.position[1] - num]]
                elif game.tegs[
                    self.position[0] - num, self.position[1] - num
                ] == 0:
                    position_new_array += [[self.position[0] - num, self.position[1] - num]]
                else:
                    left_top = 0

        position_new_array = separeted(game, position_new_array, self.position, self.color)

        return position_new_array

    def interactive(self, new_position, last_position, game):
        #проверяем была ли вражеская фигура на новой позиции ферьзя
        if game.status_game == 1:
            game.status_game *= -1
            figure = game.search_board([new_position[0], new_position[1]])
            if figure != None:
                game.black_stuff.remove(figure)
            game.status_game *= -1
        else:
            game.status_game *= -1
            figure = game.search_board([new_position[0], new_position[1]])
            if figure != None:
                game.white_stuff.remove(figure)
            game.status_game *= -1

        game.board[last_position[0], last_position[1]] = ""
        game.tegs[last_position[0], last_position[1]] = 0
        self.position = new_position
        game.board[new_position[0], new_position[1]] = self.gettype
        game.tegs[new_position[0], new_position[1]] = self.color

        if game.simulation == 0:
            check(game)
            pat(game)

        game.status_game *= -1

class King(Figure):
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.virginity = 0  #смещалася ли король/ 1-да/ 0 - нет
        self.rook = 0 #состояние рокировки

    @property
    def gettype(self):
        return "King"

    def motion(self, game):
        position_new_array = []
        num = 1
        # для диагонали
        if self.position[0] + 1 < 8 and self.position[1] + 1 < 8:
            if game.tegs[
                self.position[0] + num, self.position[1] + num
            ] == -game.status_game:
                right_bot = 0
                position_new_array += [[self.position[0] + num, self.position[1] + num]]
            elif game.tegs[
                self.position[0] + num, self.position[1] + num
            ] == 0:
                position_new_array += [[self.position[0] + num, self.position[1] + num]]
        # right_top
        if self.position[0] + num < 8 and self.position[1] - num >= 0:
            if game.tegs[
                self.position[0] + num, self.position[1] - num
            ] == -game.status_game:
                position_new_array += [[self.position[0] + num, self.position[1] - num]]
            elif game.tegs[
                self.position[0] + num, self.position[1] - num
            ] == 0:
                position_new_array += [[self.position[0] + num, self.position[1] - num]]
        # left bot
        if self.position[0] - num >= 0 and self.position[1] + num < 8:
            if game.tegs[
                self.position[0] - num, self.position[1] + num
            ] == -game.status_game:
                position_new_array += [[self.position[0] - num, self.position[1] + num]]
            elif game.tegs[
                self.position[0] - num, self.position[1] + num
            ] == 0:
                position_new_array += [[self.position[0] - num, self.position[1] + num]]
        # left_top
        if self.position[0] - num >= 0 and self.position[1] - num >= 0:
            if game.tegs[
                self.position[0] - num, self.position[1] - num
            ] == -game.status_game:
                position_new_array += [[self.position[0] - num, self.position[1] - num]]
            elif game.tegs[
                self.position[0] - num, self.position[1] - num
            ] == 0:
                position_new_array += [[self.position[0] - num, self.position[1] - num]]

        #вертикали
        # для белых
        if self.color == 1:
            # клетки сверху
            if self.position[0] + num * self.color < 8:

                if game.tegs[
                    self.position[0] + num * self.color, self.position[1]
                ] == -game.status_game:
                    position_new_array += [[self.position[0] + num * self.color, self.position[1]]]
                elif game.tegs[
                    self.position[0] + num * self.color, self.position[1]
                ] == 0:
                    position_new_array += [[self.position[0] + num * self.color, self.position[1]]]
            # клетки снизу
            if self.position[0] - num * self.color >= 0:

                if game.tegs[
                    self.position[0] - num * self.color, self.position[1]
                ] == -game.status_game:
                    position_new_array += [[self.position[0] - num * self.color, self.position[1]]]
                elif game.tegs[
                    self.position[0] - num * self.color, self.position[1]
                ] == 0:
                    position_new_array += [[self.position[0] - num * self.color, self.position[1]]]
                    # клетки слева
            if self.position[1] - num * self.color >= 0:

                if game.tegs[
                    self.position[0], self.position[1] - num * self.color
                ] == -game.status_game:
                    position_new_array += [[self.position[0], self.position[1] - num * self.color]]
                elif game.tegs[
                    self.position[0], self.position[1] - num * self.color
                ] == 0:
                    position_new_array += [[self.position[0], self.position[1] - num * self.color]]
            # клетки справа
            if self.position[1] + num * self.color < 8:

                if game.tegs[
                    self.position[0], self.position[1] + num * self.color
                ] == -game.status_game:
                    position_new_array += [[self.position[0], self.position[1] + num * self.color]]
                elif game.tegs[
                    self.position[0], self.position[1] + num * self.color
                ] == 0:
                    position_new_array += [[self.position[0], self.position[1] + num * self.color]]
            if self.virginity == 0 and game.status_check == 0 and game.simulation == 0:
                # rакировка
                figure_right = game.search_board([0, 7])
                figure_left = game.search_board([0, 0])
                if figure_right != None:
                    if figure_right.gettype == "Rook":
                        if figure_right.virginity == 0:
                            if game.tegs[0, 6] == 0 and game.tegs[0, 5] == 0:
                                #проверяем под ударом ли ладья
                                new_white_stuff = []
                                for figure in game.white_stuff:
                                    new_white_stuff.append(copy.deepcopy(figure))
                                new_black_stuff = []
                                for figure in game.black_stuff:
                                    new_black_stuff.append(copy.deepcopy(figure))

                                new_game = Board(new_black_stuff, new_white_stuff)

                                new_game.status_game = 1  # 1 - white/ -1 - black

                                new_game.status_check = 1
                                new_game.simulation = 1
                                # находим эту фигурув новом списке и меняем координаты
                                figure = new_game.search_board([0, 7])
                                new_game.white_stuff.remove(figure)

                                figure = King([0, 5], 1)
                                new_game.white_stuff.insert(0, figure)
                                new_game.build()

                                check(new_game)
                                if new_game.status_check == 0:
                                    position_new_array += [[0, 6]]

                if figure_left != None:
                    if figure_left.gettype == "Rook":
                        if figure_left.virginity == 0:
                            if game.tegs[0, 1] == 0 and game.tegs[0, 2] == 0 and game.tegs[0, 3] == 0:
                                # проверяем под ударом ли ладья
                                new_white_stuff = []
                                for figure in game.white_stuff:
                                    new_white_stuff.append(copy.deepcopy(figure))
                                new_black_stuff = []
                                for figure in game.black_stuff:
                                    new_black_stuff.append(copy.deepcopy(figure))

                                new_game = Board(new_black_stuff, new_white_stuff)

                                new_game.status_game = 1  # 1 - white/ -1 - black

                                new_game.status_check = 1
                                new_game.simulation = 1
                                # находим эту фигурув новом списке и меняем координаты
                                figure = new_game.search_board([0, 0])

                                new_game.white_stuff.remove(figure)

                                figure = King([0, 3], 1)
                                new_game.white_stuff.insert(0, figure)
                                new_game.build()

                                check(new_game)
                                if new_game.status_check == 0:
                                    position_new_array += [[0, 2]]
        else:
            #для чёрных
            if self.position[0] + num * self.color >= 0:

                if game.tegs[
                    self.position[0] + num * self.color, self.position[1]
                ] == -game.status_game:
                    position_new_array += [[self.position[0] + num * self.color, self.position[1]]]
                elif game.tegs[
                    self.position[0] + num * self.color, self.position[1]
                ] == 0:
                    position_new_array += [[self.position[0] + num * self.color, self.position[1]]]
            # клетки сверху
            if self.position[0] - num * self.color < 8:

                if game.tegs[
                    self.position[0] - num * self.color, self.position[1]
                ] == -game.status_game:
                    top = 0
                    position_new_array += [[self.position[0] - num * self.color, self.position[1]]]

                elif game.tegs[
                    self.position[0] - num * self.color, self.position[1]
                ] == 0:
                    position_new_array += [[self.position[0] - num * self.color, self.position[1]]]
            # клетки справа
            if self.position[1] - num * self.color < 8:

                if game.tegs[
                    self.position[0], self.position[1] - num * self.color
                ] == -game.status_game:
                    position_new_array += [[self.position[0], self.position[1] - num * self.color]]

                elif game.tegs[
                    self.position[0], self.position[1] - num * self.color
                ] == 0:
                    position_new_array += [[self.position[0], self.position[1] - num * self.color]]

            # клетки слева
            if self.position[1] + num * self.color >= 0:

                if game.tegs[
                    self.position[0], self.position[1] + num * self.color
                ] == -game.status_game:
                    position_new_array += [[self.position[0], self.position[1] + num * self.color]]

                elif game.tegs[
                    self.position[0], self.position[1] + num * self.color
                ] == 0:
                    position_new_array += [[self.position[0], self.position[1] + num * self.color]]
            if self.virginity == 0 and game.status_check == 0  and game.simulation == 0:
                # rакировка
                figure_right = game.search_board([7, 7])
                figure_left = game.search_board([7, 0])
                if figure_right != None:
                    if figure_right.gettype == "Rook":
                        if figure_right.virginity == 0:
                            if game.tegs[7, 6] == 0 and game.tegs[7, 5] == 0:
                                # проверяем под ударом ли ладья
                                new_white_stuff = []
                                for figure in game.white_stuff:
                                    new_white_stuff.append(copy.deepcopy(figure))
                                new_black_stuff = []
                                for figure in game.black_stuff:
                                    new_black_stuff.append(copy.deepcopy(figure))

                                new_game = Board(new_black_stuff, new_white_stuff)

                                new_game.status_game = -1  # 1 - white/ -1 - black

                                new_game.status_check = 1
                                new_game.simulation = 1

                                # находим эту фигурув новом списке и меняем координаты
                                figure = new_game.search_board([7, 7])

                                new_game.black_stuff.remove(figure)

                                figure = King([7, 5], -1)
                                new_game.black_stuff.insert(0, figure)

                                new_game.build()

                                check(new_game)
                                if new_game.status_check == 0:
                                    position_new_array += [[7, 6]]

                if figure_left != None:
                    if figure_left.gettype == "Rook":
                        if figure_left.virginity == 0:
                            if game.tegs[7, 1] == 0 and game.tegs[7, 2] == 0 and game.tegs[7, 3] == 0:
                                position_new_array += [[7, 2]]
                                # проверяем под ударом ли ладья
                                new_white_stuff = []
                                for figure in game.white_stuff:
                                    new_white_stuff.append(copy.deepcopy(figure))
                                new_black_stuff = []
                                for figure in game.black_stuff:
                                    new_black_stuff.append(copy.deepcopy(figure))

                                new_game = Board(new_black_stuff, new_white_stuff)

                                new_game.status_game = -1  # 1 - white/ -1 - black

                                new_game.status_check = 1
                                new_game.simulation = 1

                                # находим эту фигурув новом списке и меняем координаты
                                figure = new_game.search_board([7, 0])
                                new_game.black_stuff.remove(figure)

                                figure = King([7, 3], -1)
                                new_game.black_stuff.insert(0, figure)
                                new_game.build()

                                check(new_game)
                                if new_game.status_check == 0:
                                    position_new_array += [[7, 2]]

        position_new_array = separeted(game, position_new_array, self.position, self.color)

        return position_new_array

    def interactive(self, new_position, last_position, game):
        self.rook = 0
        #была ли совершена рокирровка
        if new_position[1] - last_position[1] == 2 and game.simulation == 0:
            if self.color == 1:
                rook = game.search_board([0, 7])
                rook.interactive([0, 5], rook.position, game)
                game.status_game *= -1
            else:
                rook = game.search_board([7, 7])
                rook.interactive([7, 5], rook.position, game)
                game.status_game *= -1
            self.rook = 1
        elif new_position[1] - last_position[1] == -2 and game.simulation == 0:
            if self.color == 1:
                rook = game.search_board([0, 0])
                rook.interactive([0, 3], rook.position, game)
                game.status_game *= -1
            else:
                rook = game.search_board([7, 0])
                rook.interactive([7, 3], rook.position, game)
                game.status_game *= -1
            self.rook = 2
        else:
            pass

        #проверяем была ли вражеская пешка на новой позиции ладьи
        if game.status_game == 1:
            game.status_game *= -1
            figure = game.search_board([new_position[0], new_position[1]])
            if figure != None:
                game.black_stuff.remove(figure)
            game.status_game *= -1
        else:
            game.status_game *= -1
            figure = game.search_board([new_position[0], new_position[1]])
            if figure != None:
                game.white_stuff.remove(figure)
            game.status_game *= -1

        game.board[last_position[0], last_position[1]] = ""
        game.tegs[last_position[0], last_position[1]] = 0
        self.position = new_position
        game.board[new_position[0], new_position[1]] = self.gettype
        game.tegs[new_position[0], new_position[1]] = self.color
        self.virginity = 1

        #?)))
        if game.simulation == 0:
            check(game)
            pat(game)

        game.status_game *= -1

"""
black_stuff = [0]*16
for i in range(8):
    black_stuff[i] = Pawn([6, i], -1)

black_stuff[8] = Rook([7, 0], -1)
black_stuff[9] = Rook([7, 7], -1)
black_stuff[10] = Knight([7,1], -1)
black_stuff[11] = Knight([7,6], -1)
black_stuff[12] = Bishop([7,2], -1)
black_stuff[13] = Bishop([7,5], -1)
black_stuff[14] = Queen([7,3], -1)
black_stuff[15] = King([7,4], -1)

white_stuff = [0]*16
for i in range(8):
    white_stuff[i] = Pawn([1, i], 1)

white_stuff[8] = Rook([0,0], 1)
white_stuff[9] = Rook([0,7], 1)
white_stuff[10] = Knight([0,1], 1)
white_stuff[11] = Knight([0,6], 1)
white_stuff[12] = Bishop([0,2], 1)
white_stuff[13] = Bishop([0,5], 1)
white_stuff[14] = Queen([0,3], 1)
white_stuff[15] = King([0,4], 1)

game = Board(black_stuff, white_stuff)
game.build()"""

