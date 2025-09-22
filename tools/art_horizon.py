import pygame
import math
import sys

# Инициализация PyGame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Искусственный авиагоризонт")

# Цвета
SKY_COLOR = (0, 120, 215)      # Голубой (небо)
GROUND_COLOR = (101, 67, 33)   # Коричневый (земля)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GRAY = (40, 40, 40)

# Размеры элементов
HORIZON_RADIUS = int(WIDTH * 0.8)  # Радиус горизонта
PITCH_SCALE_RANGE = 20              # Диапазон шкалы тангажа (градусы)
MARK_SPACING = 30                   # Расстояние между метками (пиксели)

# Шрифт
font = pygame.font.SysFont('Arial', 16)

def draw_artificial_horizon(surface, pitch, roll):
    """Отрисовка искусственного горизонта."""
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    
    # Сохраняем исходное состояние
    surface_orig = surface.copy()
    
    # Создаем поверхность для горизонта с альфа-каналом
    horizon_surf = pygame.Surface((WIDTH * 2, HEIGHT * 2), pygame.SRCALPHA)
    horizon_rect = horizon_surf.get_rect(center=(center_x, center_y))
    
    # Рассчитываем смещение горизонта из-за тангажа
    pitch_offset = pitch * MARK_SPACING / 10
    
    # Рисуем небо и землю с учетом крена
    pygame.draw.rect(horizon_surf, SKY_COLOR, (0, 0, WIDTH * 2, HEIGHT + pitch_offset))
    pygame.draw.rect(horizon_surf, GROUND_COLOR, (0, HEIGHT + pitch_offset, WIDTH * 2, HEIGHT))
    
    # Поворачиваем горизонт согласно крену
    rotated_horizon = pygame.transform.rotate(horizon_surf, roll)
    rot_rect = rotated_horizon.get_rect(center=(center_x, center_y))
    
    # Рисуем фон (корпус прибора)
    pygame.draw.rect(surface, GRAY, (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(surface, BLACK, (50, 50, WIDTH - 100, HEIGHT - 100), 0, 20)
    
    # Отображаем повернутый горизонт
    surface.blit(rotated_horizon, rot_rect)
    
    # Рисуем шкалу тангажа
    draw_pitch_scale(surface, pitch)
    
    # Рисуем индикатор крена
    draw_roll_scale(surface, roll)
    
    # Рисуем крестовину прицела
    draw_reticle(surface)

def draw_pitch_scale(surface, pitch):
    """Отрисовка шкалы тангажа."""
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    
    # Вертикальные линии шкалы
    pygame.draw.line(surface, WHITE, (center_x - 150, 100), (center_x - 150, HEIGHT - 100), 2)
    pygame.draw.line(surface, WHITE, (center_x + 150, 100), (center_x + 150, HEIGHT - 100), 2)
    
    # Горизонтальные метки и цифры
    for i in range(-PITCH_SCALE_RANGE, PITCH_SCALE_RANGE + 1, 5):
        y_pos = center_y - i * MARK_SPACING
        if 100 < y_pos < HEIGHT - 100:
            # Длинные метки для десятков
            if i % 10 == 0:
                pygame.draw.line(surface, WHITE, (center_x - 170, y_pos), (center_x - 130, y_pos), 2)
                pygame.draw.line(surface, WHITE, (center_x + 130, y_pos), (center_x + 170, y_pos), 2)
                text = font.render(str(i), True, WHITE)
                surface.blit(text, (center_x - 190, y_pos - 10))
                surface.blit(text, (center_x + 175, y_pos - 10))
            # Короткие метки для пятерок
            else:
                pygame.draw.line(surface, WHITE, (center_x - 160, y_pos), (center_x - 140, y_pos), 1)
                pygame.draw.line(surface, WHITE, (center_x + 140, y_pos), (center_x + 160, y_pos), 1)

def draw_roll_scale(surface, roll):
    """Отрисовка шкалы крена."""
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    radius = 120
    
    # Внешний круг
    pygame.draw.circle(surface, WHITE, (center_x, 100), radius, 2)
    
    # Метки крена
    for angle in range(-180, 181, 15):
        rad_angle = math.radians(angle)
        x_inner = center_x + (radius - 20) * math.sin(rad_angle)
        y_inner = 100 + (radius - 20) * math.cos(rad_angle)
        
        # Длина метки зависит от значимости угла
        mark_length = 15 if angle % 45 == 0 else 10
        
        x_outer = center_x + (radius - mark_length) * math.sin(rad_angle)
        y_outer = 100 + (radius - mark_length) * math.cos(rad_angle)
        
        pygame.draw.line(surface, WHITE, (x_inner, y_inner), (x_outer, y_outer), 2)
        
        # Подписи для основных углов
        if angle % 45 == 0:
            text = font.render(str(abs(angle)), True, WHITE)
            text_rect = text.get_rect(center=(x_outer - 10 * math.sin(rad_angle), 
                                            y_outer - 10 * math.cos(rad_angle)))
            surface.blit(text, text_rect)
    
    # Треугольный указатель
    pygame.draw.polygon(surface, RED, [(center_x, 60), (center_x - 10, 75), (center_x + 10, 75)])

def draw_reticle(surface):
    """Отрисовка крестовины прицела."""
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    
    # Горизонтальная линия
    pygame.draw.line(surface, WHITE, (center_x - 50, center_y), (center_x + 50, center_y), 2)
    # Вертикальная линия
    pygame.draw.line(surface, WHITE, (center_x, center_y - 50), (center_x, center_y + 50), 2)
    
    # Угловые маркеры
    pygame.draw.rect(surface, WHITE, (center_x - 80, center_y - 10, 20, 20), 2)
    pygame.draw.rect(surface, WHITE, (center_x + 60, center_y - 10, 20, 20), 2)

# Основной цикл
clock = pygame.time.Clock()
pitch, roll = 0, 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Управление для тестирования
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: pitch = min(20, pitch + 2)
            elif event.key == pygame.K_DOWN: pitch = max(-20, pitch - 2)
            elif event.key == pygame.K_LEFT: roll = (roll - 10) % 360
            elif event.key == pygame.K_RIGHT: roll = (roll + 10) % 360
            elif event.key == pygame.K_r: pitch, roll = 0, 0
    
    # Отрисовка
    screen.fill(GRAY)
    draw_artificial_horizon(screen, pitch, roll)
    
    # Вывод значений для отладки
    pitch_text = font.render(f"Тангаж: {pitch}°", True, WHITE)
    roll_text = font.render(f"Крен: {roll}°", True, WHITE)
    screen.blit(pitch_text, (20, 20))
    screen.blit(roll_text, (20, 50))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()