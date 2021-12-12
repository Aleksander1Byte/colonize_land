import pygame


class Statistics:
    def __init__(self, WINDOW_SIZE_X, WINDOW_SIZE_Y, players):
        self.width = WINDOW_SIZE_X
        self.height = WINDOW_SIZE_Y
        self.players = players

    def draw(self, screen):
        x = self.width // 15
        y = self.height - self.height * 0.15
        w = self.width - self.width // 7.5
        h = self.height * 0.13
        pygame.draw.rect(
            screen, pygame.Color('white'),
            ((x, y), (w, h)))

        font = pygame.font.Font(None, 36)
        counter = 0
        for player in self.players:
            line = f'{player.name}. Золото: {player.treasury};' \
                   f' Доход: {player.income}'
            text = font.render(str(line), True, player.getColor())
            screen.blit(text, ((x + 3), (y + 3) + (h // 3) * counter))
            counter += 1
