import pygame


class Tutorial:
    def __init__(self):
        self.active = True
        self.current_step = 0
        self.steps = [
            {
                "text": "Добро пожаловать на Марс, командир.\nВаша задача сохранить колонию в живых.\nСледите за ресурсами вверху экрана.",
                "highlight": None,
                "highlight_type": "ui_top",
            },
            {
                "text": "Это ваши здания. Прямоугольники = здания.\nКружки внутри фиолетового модуля = колонисты.\nОни потребляют кислород и ресурсы.",
                "highlight": "habitat",
                "highlight_type": "building",
            },
            {
                "text": "Жёлтые здания = генераторы энергии.\nВсе здания нуждаются в энергии.\nЕсли энергии не хватает, здания отключаются.",
                "highlight": "power_generator",
                "highlight_type": "building",
            },
            {
                "text": "Голубые здания = генераторы кислорода.\nБез кислорода колонисты умирают.\nНе дайте кислороду упасть до нуля!",
                "highlight": "life_support",
                "highlight_type": "building",
            },
            {
                "text": "Зелёные здания = теплицы.\nОни производят ресурсы (еда, запчасти).\nРесурсы нужны для ремонта и строительства.",
                "highlight": "greenhouse",
                "highlight_type": "building",
            },
            {
                "text": "Красные здания = обогреватели.\nОни греют соседние клетки.\nТеплицы работают только в тепле!",
                "highlight": "heater",
                "highlight_type": "building",
            },
            {
                "text": "Нажмите клавиши 1-5 чтобы выбрать здание.\nКликните на сетку чтобы построить.\nСтроительство стоит ресурсы.",
                "highlight": None,
                "highlight_type": "grid",
            },
            {
                "text": "Здания изнашиваются со временем.\nПравый клик по зданию = ремонт (стоит 10 ресурсов).\nПолоска над зданием = его здоровье.",
                "highlight": None,
                "highlight_type": "building_health",
            },
            {
                "text": "Каждые 3 минуты происходит кризис:\nпыльная буря, поломка, утечка кислорода.\nБудьте готовы реагировать!",
                "highlight": None,
                "highlight_type": "event_area",
            },
            {
                "text": "Кнопка Research открывает дерево улучшений.\nИсследования стоят ресурсы и время.\nОни открывают новые здания и бонусы.",
                "highlight": None,
                "highlight_type": "research_button",
            },
            {
                "text": "Исследование Automatic Repair открывает\nремонтный дрон (клавиша 6).\nОн автоматически чинит соседние здания.",
                "highlight": None,
                "highlight_type": None,
            },
            {
                "text": "Исследование Backup Power открывает\nаккумулятор (клавиша 7).\nОн хранит энергию на ночь.",
                "highlight": None,
                "highlight_type": None,
            },
            {
                "text": "Ваша цель выжить как можно дольше.\nПробел = замедлить время.\nУдачи, командир. Марс не прощает ошибок.",
                "highlight": None,
                "highlight_type": None,
            },
        ]

    def next_step(self):
        self.current_step += 1
        if self.current_step >= len(self.steps):
            self.active = False

    def skip(self):
        self.active = False

    def restart(self):
        self.current_step = 0
        self.active = True

    def get_current_step(self):
        if self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None

    def render(self, screen, game_state):
        if not self.active:
            return
        step = self.get_current_step()
        if not step:
            return
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        if step["highlight_type"]:
            self._render_highlight(screen, step, game_state)
        box_width = 600
        box_height = 200
        box_x = (screen.get_width() - box_width) // 2
        box_y = (screen.get_height() - box_height) // 2
        pygame.draw.rect(screen, (40, 40, 40), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(
            screen, (100, 100, 255), (box_x, box_y, box_width, box_height), 3
        )
        font = pygame.font.Font(None, 24)
        y_offset = box_y + 20
        for line in step["text"].split("\n"):
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(
                center=(screen.get_width() // 2, y_offset)
            )
            screen.blit(text_surface, text_rect)
            y_offset += 30
        button_font = pygame.font.Font(None, 20)
        next_text = (
            "Понятно (Enter)"
            if self.current_step < len(self.steps) - 1
            else "Начать (Enter)"
        )
        next_surface = button_font.render(next_text, True, (0, 255, 0))
        next_rect = next_surface.get_rect(
            center=(screen.get_width() // 2, box_y + box_height - 30)
        )
        screen.blit(next_surface, next_rect)
        if self.current_step == 0:
            skip_surface = button_font.render("Пропустить (S)", True, (255, 100, 100))
            skip_rect = skip_surface.get_rect(
                center=(screen.get_width() // 2, box_y + box_height - 60)
            )
            screen.blit(skip_surface, skip_rect)

    def _render_highlight(self, screen, step, game_state):
        from renderer import GRID_OFFSET_X, GRID_OFFSET_Y, GRID_SIZE

        if step["highlight_type"] == "ui_top":
            highlight_rect = pygame.Rect(0, 0, screen.get_width(), 80)
            pygame.draw.rect(screen, (255, 255, 0), highlight_rect, 3)
        elif step["highlight_type"] == "building":
            building_type = step["highlight"]
            for building in game_state.buildings:
                if building.type == building_type:
                    x = GRID_OFFSET_X + building.x * GRID_SIZE
                    y = GRID_OFFSET_Y + building.y * GRID_SIZE
                    width = building.width * GRID_SIZE
                    height = building.height * GRID_SIZE
                    pygame.draw.rect(screen, (255, 255, 0), (x, y, width, height), 4)
                    break
        elif step["highlight_type"] == "grid":
            grid_rect = pygame.Rect(
                GRID_OFFSET_X, GRID_OFFSET_Y, 10 * GRID_SIZE, 10 * GRID_SIZE
            )
            pygame.draw.rect(screen, (255, 255, 0), grid_rect, 3)

    def handle_input(self, event):
        if not self.active:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.next_step()
                return True
            elif event.unicode.lower() == "s":
                if self.current_step == 0:
                    self.skip()
                    return True
        return False
