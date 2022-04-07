import pygame


class Statistics:
    def __init__(self, WINDOW_SIZE_X, WINDOW_SIZE_Y, players):
        self.width = WINDOW_SIZE_X
        self.height = WINDOW_SIZE_Y
        self.players = players

    def draw(self, screen, step):
        x = self.width // 15
        y = self.height - self.height * 0.15
        w = self.width - self.width // 7.5
        h = self.height * 0.13

        font = pygame.font.Font(None, 36)
        stroke = pygame.font.Font(None, 36)
        counter = 0
        for player in self.players:
            line = f'{player.name}. Золото: {player.treasure};' \
                   f' Доход: {player.income}'
            text = font.render(str(line), True, player.getColor())
            textStroke = stroke.render(str(line), True, pygame.Color('black'))
            screen.blit(textStroke, ((x + 2), (y + 2) + (h // 3) * counter))
            screen.blit(text, ((x + 3), (y + 3) + (h // 3) * counter))
            counter += 1

        line = f'Ход игрока {self.players[step].name}'
        text = font.render(str(line), True, self.players[step].getColor())
        textStroke = font.render(str(line), True, pygame.Color('black'))
        screen.blit(textStroke, (x + self.width * 0.55 - 1, y + 2))
        screen.blit(text, (x + self.width * 0.55, y + 3))
