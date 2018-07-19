from multirhythm import *
from tools import *
from correlate import coeff_correl

class VisuMulti :

    def __init__ (self, monoTab):
        """
        monoTab: a list of (MonoRhythm, MonoMelody) elements
        """
        monoRtab = []
        self.__nb_tracks = len(monoTab)
        self.__duration = 0 #tracks max duration
        for m in monoTab :
            monoRtab.append(m)
            if m.get_duration() > self.__duration:
                self.__duration = m.get_duration()
        self.__multirhythm = MultiRhythm(monoRtab)
        self.__rect_built = False
        self.__rect_rhythm = [[[0 for y in range(self.__nb_tracks)] for x in range(self.__nb_tracks)] for t in range(int(floor(self.__duration * MATRIX_FPS)))]

    def is_visu_ended(self, t):
        """
        given t the index of __rect_rhythm, 
        return 1 if t >=  int(floor(self.__duration * MATRIX_FPS)),
        i.e if tracks are ended;
        else return 0
        """
        return t >= floor(self.__duration * MATRIX_FPS)

    def __compute_interval(self, oframe, frame, length):
        if frame - CORREL_INTERVAL < 0:
            a = 0
        else:
            a = oframe[frame - CORREL_INTERVAL]
        if frame + CORREL_INTERVAL < len(oframe):
            b = oframe[frame + CORREL_INTERVAL]
        else:
            b = length
        return (a, b)


    def __coeff_to_color(self, coeff):
        """
        return a rgb triplet, given a coeff between 0 and 1
        """
        if coeff < 0.5:
            r = 250
            g = int(235 * (coeff * 2)) + 20
        else:
            r = int(235 * ((1 - coeff) * 2)) + 20
            g = 250
        b = 20
        return (r, g, b)
        

    def get_shade_list(self):
        rect_list = []
        step = max(1, MATRIX_SIZE / NB_COLORS) #1 pixel minimum required
        size = (MATRIX_SIZE, step)
        for i in range(0, MATRIX_SIZE, step):
            pos = (SCREEN_WIDTH - MATRIX_SIZE + i, TRACK_INDENT)
            surf = pg.Surface(size)            
            color = self.__coeff_to_color(1.0 * i / MATRIX_SIZE)
            surf.fill(color)
            rect_list.append((surf, pos))
        return rect_list
        

    def get_rect_rhythm(self):
        """
        size: size of the surface (correlation matrix) to display
        timer: media player current time
        """
        if self.__rect_built == False:
            self.__build_rect_rhythm(coeff_correl)
            self.__rect_built = True
        return self.__rect_rhythm


    def __build_rect_rhythm(self, correl_coeff):
        """
        creates a table img[t][x][y] of elements (surf, pos) where
        surf is the surface to blit and pos the position of the blitting
        the matrix image list is saved on the self.__rect_rhythm surface
        for each chosen frame, we display an image composed of (i, j) rectangles
        with different colours:
        - black if the track i or j has ended
        - green if the track i is in time compared to j
        - red if the track i is out of time compared to j
        (the colour ranges from green to red depending on the tardiness between i and j)
        correl_coeff: function computing a correlation coefficient list
                      given two onsets lists and a time frame
        """
        step = MATRIX_SIZE / self.__nb_tracks
        size = (step, step)
        beat = self.__multirhythm.get_beat()
        length = floor(self.__duration * MATRIX_FPS)
        nbframes = int(time_to_frame(length))
        monolist = self.__multirhythm.get_mono_list() 
        x = 0

        for m1 in monolist:            
            oenv1 = m1.get_onset_envelope() #computed only once
            sr = m1.get_sample_rate()
            hl = m1.get_hop_length()
            y = x

            while y < self.__nb_tracks:
            #m2 serves as reference to m1 / m2 comparison
                t = 0 #time index of the rect matrix
                time = 0 #real time corresponding to t
                oenv2 = monolist[y].get_onset_envelope()
                frame = 0 #index of oenv2
                
                if x != y:#black squares on the diagonal
                    while time < length and frame < len(beat):
                        interval = self.__compute_interval(beat, frame, nbframes)
                        #third argument must be in frames to compare with beat
                        time = self.__rect_index_to_time(t)
                        if m1.get_duration() < time:
                            #if the compared track is ended, show black squares until the end
                            t = self.__draw_rect_colors(t, x, y, BLACK, length)
                        else:
                            coeff = correl_coeff(oenv1, oenv2, interval)
                            if coeff < CORREL_THRESHOLD:
                                color = BLACK
                            else:
                                color = self.__coeff_to_color(coeff)
                            t = self.__draw_rect_colors(t, x, y, color, frame_to_time(beat[frame], hl, sr))
                        frame += 1
                #fill the remaining time in black
                surf = pg.Surface(size)
                surf.fill(BLACK)
                while t < floor(self.__duration * MATRIX_FPS):
                    pos = ((x * step, y * step))
                    self.__rect_rhythm[t][x][y] = (surf, pos)
                    pos = ((y * step, x * step))
                    self.__rect_rhythm[t][y][x] = (surf, pos)
                    t += 1            
                y += 1
            x += 1

    def __rect_index_to_time(self, t):
        return (t * 1.0) / MATRIX_FPS

    def __draw_rect_colors(self, t, x, y, color, max_time):
        step = MATRIX_SIZE / self.__nb_tracks
        size = (step, step)
        surf = pg.Surface(size)
        surf.fill(color)
        while self.__rect_index_to_time(t) < max_time:
            #blit the color while the current time (t / MATRIX_FPS) is inferior to
            #the time of the current oenv2 frame
            pos = ((x * step, y * step))
            self.__rect_rhythm[t][x][y] = (surf, pos)
            pos = ((y * step, x * step))
            self.__rect_rhythm[t][y][x] = (surf, pos)
            t += 1
        return t        
        
