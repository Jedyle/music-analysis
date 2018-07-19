from constants import  *

class ButtonSet:
    """
    set of buttons linked to a track (increase volume, decrease volume, mute, delete)
    """

    def __init__(self, window, pos):
        """
        pos: top left corner of the track_bar position 
        """
        self.__size = TRACK_SIZE
        self.__buttons = []
        self.set_buttons_pos(window, pos)
    
    def set_buttons_pos(self, window, pos):
        """
        replace button set in case a previous track is deleted
        """
        self.__buttons = []
        x, y = TRACK_SIZE
        size = (x / 10, y / 2)
        delete = window.build_button("x", pos, size)
        self.__buttons.append(delete)
        pos_mute = (pos[0], pos[1] + y / 2)
        mute = window.build_button("M", pos_mute, size)
        mute.set_button_font_color(MUTE_OFF_COLOR)
        self.__buttons.append(mute)
        pos_vol_up = (pos[0] + x * 25 / 100, pos[1])
        vol_up = window.build_button("+", pos_vol_up, size)
        self.__buttons.append(vol_up)
        pos_vol_down = (pos[0] + x * 25 / 100, pos[1] + y / 2)
        vol_down = window.build_button("-", pos_vol_down, size)
        self.__buttons.append(vol_down)

    def get_buttons(self):
        return self.__buttons
