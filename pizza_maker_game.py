import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pizza Maker Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BROWN = (165, 42, 42)
LIGHT_GRAY = (200, 200, 200)

# Load background image
background = pygame.image.load('kitchen.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Pizza and ingredients
pizza_base = pygame.Rect(300, 200, 200, 200)

ingredient_categories = {
    "Sauces": [
        {"name": "Tomato Sauce", "color": (255, 99, 71)},
        {"name": "BBQ Sauce", "color": (128, 0, 0)},
        {"name": "Alfredo Sauce", "color": (255, 250, 220)},
        {"name": "Pesto Sauce", "color": (0, 128, 0)},
        {"name": "Buffalo Sauce", "color": (255, 102, 0)},
        {"name": "Garlic Sauce", "color": (255, 255, 200)},
        {"name": "Olive Oil", "color": (223, 217, 180)},
        {"name": "Ranch Sauce", "color": (255, 253, 208)}
    ],
    "Cheeses": [
        {"name": "Mozzarella", "color": (255, 255, 224)},
        {"name": "Cheddar", "color": (255, 165, 0)},
        {"name": "Parmesan", "color": (255, 250, 205)},
        {"name": "Gouda", "color": (255, 204, 153)},
        {"name": "Blue Cheese", "color": (240, 248, 255)},
        {"name": "Feta", "color": (255, 255, 255)},
        {"name": "Goat Cheese", "color": (255, 250, 240)},
        {"name": "Provolone", "color": (255, 255, 204)}
    ],
    "Meats": [
        {"name": "Pepperoni", "color": (205, 38, 38)},
        {"name": "Bacon", "color": (168, 67, 0)},
        {"name": "Ham", "color": (255, 150, 150)},
        {"name": "Sausage", "color": (139, 69, 19)},
        {"name": "Chicken", "color": (255, 229, 180)},
        {"name": "Meatballs", "color": (165, 42, 42)},
        {"name": "Prosciutto", "color": (255, 192, 203)},
        {"name": "Salami", "color": (200, 63, 73)}
    ],
    "Vegetables": [
        {"name": "Jalapeno", "color": (0, 128, 0)},
        {"name": "Mushroom", "color": (128, 64, 0)},
        {"name": "Bell Pepper", "color": (255, 0, 0)},
        {"name": "Onion", "color": (255, 255, 255)},
        {"name": "Tomato", "color": (255, 99, 71)},
        {"name": "Spinach", "color": (0, 100, 0)},
        {"name": "Garlic", "color": (245, 245, 220)},
        {"name": "Artichoke", "color": (154, 205, 50)}
    ],
    "Fruits": [
        {"name": "Pineapple", "color": (255, 223, 0)},
        {"name": "Olives", "color": (0, 0, 0)},
        {"name": "Sun-Dried Tomatoes", "color": (178, 34, 34)},
        {"name": "Roasted Red Peppers", "color": (178, 34, 34)},
        {"name": "Figs", "color": (128, 0, 0)},
        {"name": "Grapes", "color": (128, 0, 128)},
        {"name": "Mandarin Oranges", "color": (255, 165, 0)},
        {"name": "Peaches", "color": (255, 218, 185)}
    ]
}

pizza_layers = {
    "base": (255, 200, 150),
    "sauce": None,
    "cheese": [],
    "toppings": []
}

# Dropdown menu
dropdown_rect = pygame.Rect(50, 50, 200, 30)
dropdown_options = list(ingredient_categories.keys())
dropdown_open = False
selected_category = None

def add_ingredient(ingredient, category):
    if category == "Sauces":
        pizza_layers["sauce"] = ingredient["color"]
    elif category == "Cheeses":
        pizza_layers["cheese"].append({"color": ingredient["color"], "positions": generate_positions(40)})
    else:
        pizza_layers["toppings"].append({"color": ingredient["color"], "positions": generate_positions(15)})

def generate_positions(count):
    positions = []
    for _ in range(count):
        x = random.randint(20, 180)
        y = random.randint(20, 180)
        if (x - 100)**2 + (y - 100)**2 <= 90**2:
            positions.append((x, y))
    return positions

def draw_pizza():
    # Draw base
    pygame.draw.ellipse(screen, pizza_layers["base"], pizza_base)
    
    # Draw sauce
    if pizza_layers["sauce"]:
        sauce_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.ellipse(sauce_surface, (*pizza_layers["sauce"], 200), (10, 10, 180, 180))
        screen.blit(sauce_surface, (pizza_base.x, pizza_base.y))
    
    # Draw cheese
    for cheese in pizza_layers["cheese"]:
        for pos in cheese["positions"]:
            pygame.draw.circle(screen, cheese["color"], (pizza_base.x + pos[0], pizza_base.y + pos[1]), 5)
    
    # Draw toppings
    for topping in pizza_layers["toppings"]:
        for pos in topping["positions"]:
            pygame.draw.circle(screen, topping["color"], (pizza_base.x + pos[0], pizza_base.y + pos[1]), 5)

def draw_dropdown():
    pygame.draw.rect(screen, LIGHT_GRAY, dropdown_rect)
    font = pygame.font.Font(None, 24)
    text = font.render(selected_category or "Select Category", True, BLACK)
    screen.blit(text, (dropdown_rect.x + 10, dropdown_rect.y + 5))
    
    if dropdown_open:
        for i, option in enumerate(dropdown_options):
            option_rect = pygame.Rect(dropdown_rect.x, dropdown_rect.y + (i+1)*30, 200, 30)
            pygame.draw.rect(screen, WHITE, option_rect)
            text = font.render(option, True, BLACK)
            screen.blit(text, (option_rect.x + 10, option_rect.y + 5))

# Game loop
running = True
scroll_y = 0
max_scroll = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if dropdown_rect.collidepoint(event.pos):
                    dropdown_open = not dropdown_open
                elif dropdown_open:
                    for i, option in enumerate(dropdown_options):
                        option_rect = pygame.Rect(dropdown_rect.x, dropdown_rect.y + (i+1)*30, 200, 30)
                        if option_rect.collidepoint(event.pos):
                            selected_category = option
                            dropdown_open = False
                            scroll_y = 0
                elif selected_category:
                    for i, ingredient in enumerate(ingredient_categories[selected_category]):
                        ingredient_rect = pygame.Rect(600, 50 + i*35 - scroll_y, 180, 30)
                        if ingredient_rect.collidepoint(event.pos):
                            add_ingredient(ingredient, selected_category)
            elif event.button == 4:  # Scroll up
                scroll_y = max(0, scroll_y - 20)
            elif event.button == 5:  # Scroll down
                scroll_y = min(max_scroll, scroll_y + 20)

    # Draw everything
    screen.blit(background, (0, 0))
    
    # Draw pizza
    draw_pizza()
    
    # Draw dropdown
    draw_dropdown()
    
    # Draw ingredients if category is selected
    if selected_category:
        max_scroll = max(0, len(ingredient_categories[selected_category]) * 35 - 500)
        for i, ingredient in enumerate(ingredient_categories[selected_category]):
            ingredient_rect = pygame.Rect(600, 50 + i*35 - scroll_y, 180, 30)
            if 50 <= ingredient_rect.y <= 550:
                base_color = ingredient["color"]
                text_color = BLACK if sum(base_color) > 382 else WHITE
                pygame.draw.rect(screen, (*base_color, 180), ingredient_rect)
                pygame.draw.rect(screen, (*text_color, 50), ingredient_rect, 1)
                font = pygame.font.Font(None, 24)
                text = font.render(ingredient["name"], True, text_color)
                screen.blit(text, (ingredient_rect.x + 10, ingredient_rect.y + 5))

    pygame.display.flip()

pygame.quit()
sys.exit()