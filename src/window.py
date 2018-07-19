import pygame as pg
from constants import *
import button as bt

class Window:


    def __init__(self):        
        self._window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__background = pg.transform.scale(pg.image.load(IMG_PATH + "background.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__init_player()
        self.__init_buttons()
        self.__icon = pg.image.load(IMG_PATH + "icon.png").convert()
        pg.display.set_icon(self.__icon)
        pg.display.set_caption(WINDOW_TITLE)
        

    def __init_player(self):
        self.__player_but_len = min(TRACK_WIDTH / 3, TRACK_HEIGHT)
        self.__track_bar = pg.transform.scale(pg.image.load(IMG_PATH + "track_bar.png").convert(), (TRACK_WIDTH, TRACK_HEIGHT))
        self.__play_img = pg.transform.scale(pg.image.load(IMG_PATH + "play_button.png").convert(), (self.__player_but_len, self.__player_but_len))
        self.__play_img.set_colorkey(GREEN)
        self.__pause_img = pg.transform.scale(pg.image.load(IMG_PATH + "pause_button.png").convert(), (self.__player_but_len, self.__player_but_len))
        self.__pause_img.set_colorkey(GREEN)
        self.__stop_img = pg.transform.scale(pg.image.load(IMG_PATH + "stop_button.png").convert(), (self.__player_but_len, self.__player_but_len))
        self.__stop_img.set_colorkey(GREEN)

    def _get_player_action(self, pos, play, pause, stop, state):
        pos_stop = self.__get_player_button_pos(self.__stop_img)
        pos_play = self.__get_player_button_pos(self.__play_img)
        l = self.__player_but_len
        if pos[1] > TRACK_INDENT and pos[1] < TRACK_INDENT + TRACK_HEIGHT and pos[0] < TRACK_WIDTH: 
            if pos[0] > pos_stop[0] and pos[0] < pos_stop[0] + l and pos[1] > pos_stop[1] and pos[1] < pos_stop[1] + l:
                stop()
            elif pos[0] > pos_play[0] and pos[0] < pos_play[0] + l and pos[1] > pos_play[1] and pos[1] < pos_play[1] + l:
                if state == PLAYER_STOPPED:
                    play()
                else:
                    pause()

    def __get_player_button_pos(self, button_img):
        start = TRACK_WIDTH / 2 - self.__player_but_len
        if button_img == self.__stop_img:
            return (start, TRACK_INDENT)
        elif button_img == self.__play_img or button_img == self.__pause_img:
            return (start + self.__player_but_len, TRACK_INDENT)

    def __draw_player(self, state):
        self._window.blit(self.__track_bar, (0, TRACK_INDENT))
        self._window.blit(self.__stop_img , (self.__get_player_button_pos(self.__stop_img)))
        if state == PLAYER_STOPPED or state == PLAYER_PAUSED:
            self._window.blit(self.__play_img , (self.__get_player_button_pos(self.__play_img)))
        else:
            self._window.blit(self.__pause_img, (self.__get_player_button_pos(self.__pause_img)))

    def _draw_window(self, state):
        self._window.blit(self.__background, (0,0))
        self.draw_rectangle((0,0), (SCREEN_WIDTH, BUTTON_SIZE[1]), LIGHTGRAY)
        for b in self._buttons:
            self.draw_button(b)
        self.__draw_player(state)

    def __init_buttons(self):
        self._buttons = []
        add = self.build_button("Add file", (0,0), BUTTON_SIZE)
        self._buttons.append(add)
        rhythm = self.build_button("track rhythm", (BUTTON_SIZE[0],0), BUTTON_SIZE)
        self._buttons.append(rhythm)
        melody = self.build_button("track melody", (BUTTON_SIZE[0] * 2,0), BUTTON_SIZE)
        self._buttons.append(melody)
        rhythm_global = self.build_button("global rhythm", (BUTTON_SIZE[0] * 3,0), BUTTON_SIZE)
        self._buttons.append(rhythm_global)
        
    def build_button(self, text, pos, size, font = None):
        b = bt.PygButton(pg.Rect(pos, size), text, LIGHTGRAY, BLACK, font)
        return b
 
    def draw_rectangle(self, pos, size, color=bt.LIGHTGRAY):
        surface = pg.Surface(size)
        surface.fill(color)
        self._window.blit(surface, pos)

    def draw_line(self, pos1, pos2, color=bt.RED):
        pg.draw.line(self._window, color, pos1, pos2)

    def draw_button(self, button):
        button.draw(self._window)

    def get_buttons(self):
        return self._buttons
                
    def blit_surface(self, surf, pos):
        """
        pos = (x, y) indicating the top left corner of the image to display
        """
        self._window.blit(surf, pos)

    def blit_text(self, text, pos):
        """
        pos = (x, y) indicating the top left corner of the text to display
        """
        label = TRACK_FONT.render(text, 1, (0,0,0))
        self._window.blit(label, pos)
