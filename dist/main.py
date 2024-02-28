import random

import pygame

pygame.init()

size = 1280, 720
width, height = size[0], size[1]
screen = pygame.display.set_mode(size)

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
black_shadow = (51, 51, 51)

high = pygame.font.Font("freesansbold.ttf", 52)
low = pygame.font.Font("freesansbold.ttf", 26)
memory_image = pygame.image.load('memory.png')
touch_sound = pygame.mixer.music.load('touch.mp3')
FPS = 60
timer = pygame.time.Clock()
board_with_numbers = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]
numbers_list = []
numbers_used = []
interval_list = []
main_game = True
guess1 = False
guess2 = False
retry = True
game_over = False
score_in_game = 0
matches = 0
guess1_num = 0
guess2_num = 0
rows_numbers = 6
cols_numbers = 8


def draw_menu():
    global exit_button
    global game_button
    screen.fill(orange)
    menu_boards = pygame.draw.rect(screen, black, [390, 0, 520, height], 0)
    background_menu = pygame.draw.rect(screen, white, [400, 0, 500, height], 0)
    screen.blit(memory_image, (450, 50))
    game_button = pygame.draw.rect(screen, red, [450, 300, 400, 80], 0, 5)
    game_text = high.render('Начать', True, white)
    screen.blit(game_text, (555, 315))
    exit_button = pygame.draw.rect(screen, red, [450, 400, 400, 80], 0, 5)
    exit_text = high.render('Выход', True, white)
    screen.blit(exit_text, (555, 415))


def generate_numbers():
    for n in range(rows_numbers * cols_numbers // 2):
        numbers_list.append(n)
    for n in range(rows_numbers * cols_numbers):
        cell = numbers_list[random.randint(0, len(numbers_list) - 1)]
        interval_list.append(cell)
        if cell in numbers_used:
            numbers_used.remove(cell)
            numbers_list.remove(cell)
        else:
            numbers_used.append(cell)


def backgrounds():
    global back_button
    background = pygame.draw.rect(screen, orange, [0, 0, width, height], 0)
    right_board = pygame.draw.rect(screen, white, [850, 0, width, height], 0)
    screen.blit(memory_image, (870, 10))
    restart_button = pygame.draw.rect(screen, red, [1070, height - 90, 200, 80], 0, 5)
    back_button = pygame.draw.rect(screen, red, [860, height - 90, 200, 80], 0, 5)
    back_button_text = high.render('Назад', True, white)
    screen.blit(back_button_text, (876, 645))
    restart_text = high.render('Заново', True, white)
    screen.blit(restart_text, (1075, 645))
    score_text = low.render(f'Текущее количество шагов: {score_in_game}', True, black)
    screen.blit(score_text, (870, 220))
    return restart_button


def generate_board():
    board_list = []
    for h in range(cols_numbers):
        for j in range(rows_numbers):
            shadow = pygame.draw.rect(screen, black_shadow, [h * 100 + 36, j * 100 + 74, 80, 80], 0, 4)
            cell = pygame.draw.rect(screen, black, [h * 100 + 32, j * 100 + 70, 80, 80], 0, 4)
            board_list.append(cell)
    for k in range(rows_numbers):
        for p in range(cols_numbers):
            if board_with_numbers[k][p] == 1:
                correct_answer = pygame.draw.rect(screen, green, [p * 100 + 30, k * 100 + 70, 82, 82], 3, 4)
    return board_list


def checking_guess(a, b):
    global score_in_game
    global matches
    if interval_list[a] == interval_list[b]:
        cols_numbers1 = a // rows_numbers
        cols_numbers2 = b // rows_numbers
        rows_numbers1 = a - (cols_numbers1 * rows_numbers)
        rows_numbers2 = b - (cols_numbers2 * rows_numbers)
        if board_with_numbers[rows_numbers1][cols_numbers1] == 0 \
                and board_with_numbers[rows_numbers2][cols_numbers2] == 0:
            board_with_numbers[rows_numbers1][cols_numbers1] = 1
            board_with_numbers[rows_numbers2][cols_numbers1] = 1
            score_in_game += 1
            matches += 1
    else:
        score_in_game += 1


running = True
while running:
    if main_game:
        draw_menu()
        pygame.display.set_caption('МЕМОРИ: Главное меню')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_button.collidepoint(event.pos):
                    pygame.mixer.music.play(0)
                    pygame.display.set_caption('МЕМОРИ: Идёт игра')
                    main_game = False
                if exit_button.collidepoint(event.pos) and pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pygame.mixer.music.play(0)
                    pygame.display.set_caption('МЕМОРИ: ВЫХОД')
                    pygame.time.delay(1000)
                    pygame.quit()
    else:
        timer.tick(FPS)
        if retry:
            generate_numbers()
            retry = False
        restart = backgrounds()
        board = generate_board()
        if guess1 and guess2:
            checking_guess(guess1_num, guess2_num)
            speed = pygame.time.delay(500)
            guess1 = False
            guess2 = False
        if matches == rows_numbers * cols_numbers // 2:
            game_over = True
            win = pygame.draw.rect(screen, black, [20, height - 300, width - 300, 80], 0)
            win_text = high.render(f'Победа! {score_in_game} шага(-ов) было сделано!', True, white)
            screen.blit(win_text, (30, height - 290))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(board)):
                    button = board[i]
                    if not game_over:
                        if button.collidepoint(event.pos) and not guess1:
                            pygame.mixer.music.play(0)
                            guess1 = True
                            guess1_num = i
                        if button.collidepoint(event.pos) and not guess2 and guess1 and i != guess1_num:
                            pygame.mixer.music.play(0)
                            guess2 = True
                            guess2_num = i
                        if back_button.collidepoint(event.pos) and pygame.MOUSEBUTTONDOWN and event.button == 1:
                            pygame.mixer.music.play(0)
                            main_game = True
                if restart.collidepoint(event.pos):
                    pygame.mixer.music.play(0)
                    interval_list = []
                    numbers_list = []
                    numbers_used = []
                    score_in_game = 0
                    matches = 0
                    retry = True
                    guess1 = False
                    guess2 = False
                    board_with_numbers = [[0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0]]
                    game_over = False
        if guess1:
            cell_text = low.render(f'{interval_list[guess1_num]}', True, gray)
            a = (guess1_num // rows_numbers * 100 + 38,
                 (guess1_num - (guess1_num // rows_numbers * rows_numbers)) * 100 + 80)
            screen.blit(cell_text, a)
        if guess2:
            cell_text = low.render(f'{interval_list[guess2_num]}', True, gray)
            a = (guess2_num // rows_numbers * 100 + 38,
                 (guess2_num - (guess2_num // rows_numbers * rows_numbers)) * 100 + 80)
            screen.blit(cell_text, a)
    pygame.display.flip()
pygame.quit()
