# -*- coding: utf-8 -*-

import tkinter as tk
import time
import random


def main():
    width, height = 800, 600  # hauteur et largeur du dessin

    # Creation de la fenêtre :
    window_tk = tk.Tk()
    window_tk.title("Animation avec Tkinter")

    # creation du Canvas	avec un fond gris:
    canvas_tk = tk.Canvas(window_tk, bg='dark grey',
                          height=height, width=width)
    canvas_tk.pack()

    # PhotoImage chargement d'une image
    # l'image doit être dans le même répertoire que le programme
    # file : le nom du fichier image
    ball_photoImage = tk.PhotoImage(file="balle-jaune.gif")
    racket_photoImage = tk.PhotoImage(file="raquetteverte.gif")

    x_ball = width // 2
    y_ball = height // 2
    image_ball = canvas_tk.create_image(
        x_ball,
        y_ball,
        anchor=tk.CENTER,
        image=ball_photoImage
    )
    dx_ball = random.randint(10, 15)
    dy_ball = random.randint(10, 15)

    x_racket = 50
    y_racket = height // 2
    image_racket = canvas_tk.create_image(
        x_racket,
        y_racket,
        anchor=tk.CENTER,
        image=racket_photoImage
    )

    """
    TODO: Create or complete each of the class MoveCallable, Ball, Racket,
    and WindowInfos then uncomment
    """
    ball = Ball(x_ball, y_ball, dx_ball, dy_ball, image_ball)
    racket = Racket(x_racket, y_racket, 25, 100, 30, image_racket)
    window_infos = WindowInfos(window_tk, width, height)
    move_function = MoveCallable(ball, racket, canvas_tk, window_infos)

    button = tk.Button(
        window_tk,
        text='Demarrer',
        width=8,
        command=move_function)
    button.pack()

    def key_a(event):
        racket.move(-1)
    window_tk.bind("a", key_a)

    def key_q(event):
        racket.move(1)
    window_tk.bind("q", key_q)

    window_tk.mainloop()


class MoveCallable:
    """This is a callable object that will update moving objects and canvas_tk.

        Basically MoveCallable is a function and can be called as it thanks to
        the __call__ method defined in it that makes it "callable". It has
        the same utility as the function move() in the previous TP.
    """

    def __init__(self, ball, racket, canvas_tk, window_infos):
        """
        MoveCallable constructor

        Parameters
        ----------
        ball : Ball object
        racket : Racket object
        canvas_tk : tk.Canvas object
        window_infos : [windowObject, width, height]

        Returns
        -------
        self
        """
        self.ball = ball
        self.racket = racket
        self.canvas_tk = canvas_tk
        self.window_infos = window_infos
        self.__name__ = 'MoveCallable'

    def __call__(self):
        """Makes the class MoveCallable callable
        """
        t0 = time.perf_counter()
        # TODO: create and complete the class Ball
        lost = self.ball.update_direction(self.window_infos, self.racket)
        self.ball.update_position()

        self.canvas_tk.coords(self.ball.image, self.ball.x, self.ball.y)
        self.canvas_tk.coords(self.racket.image, self.racket.x, self.racket.y)

        elapsed_time = time.perf_counter() - t0

        if (lost):
            self.canvas_tk.create_text(
                250,
                300,
                text="PERDU",
                font="Arial 32 italic",
                fill="green"
            )
        if (not lost):
            # appel de la fonction apres 33 millisecondes
            # on tient compte du temps de traitement pour garantir un fps de 30
            self.window_infos.window_tk.after(
                round(max(0, 33-elapsed_time)), self)


class Ball:
    """
    Represents a ball

    A Ball has 5 attributes:
        - x: int -- the x position
        - y: int -- the y position
        - dx: int -- the displacement in x
        - dy: int -- the displacement in y
        - image: tk.Image -- the image drawn on the canvas that represents the
                            ball
    """

    def __init__(self, x, y, dx, dy, image):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.image = image

    def update_position(self):
        """Update the position (x and y) by adding the speed (dx and dy)"""
        self.x += self.dx
        self.y += self.dy

    def update_direction(self, window_infos, racket):
        """Checks for collision and inverse dx or dy if necessary

        args:
            window_infos -- everything relative to the tk window
            racket -- the racket object to check for collision
        return:
            lost -- a boolean to check if the player has lost.
        """
        
        xRacketCollide = racket.x <= self.x <= racket.x+racket.width
        yRacketCollide = racket.y <= self.y <= racket.y+racket.length
        
        if self.x < 0 or self.x > window_infos.width:
            self.dx *= -1
        if self.y < 0 or self.y > window_infos.height:
            self.dy *= -1
            
        if xRacketCollide and yRacketCollide:
            self.dx *= -1


class WindowInfos:
    """A structure to keep window_tk, width and height together

    WindowInfos has 3 attributes:
        - window_tk: tk.TK -- the window manager from the library TK
        - width: int -- the width of the window
        - height: int -- the height of the window
    """

    def __init__(self, window_tk, width, height):
        self.window_tk = window_tk
        self.width = width
        self.height = height


class Racket:
    """Represents the racket

    A Racket has 6 attributes:
        - x: int -- the x position
        - y: int -- the y position
        - step: int -- the displacement value each time 'a' or 'q' is typed
        - length: int -- the length of the Racket
        - width: int -- the width of the Racket
        - image: tk.Image -- the image drawn on the canvas that represents the
                            Racket

    A Racket has 2 methods:
        - __init__(self, x, y, step, length, width, image) -- the constructor
        - move(self, direction) -- move the racket up (direction = -1) or 
                                    down (direction = 1)
    """
    # TODO: implement the class and its methods

    def __init__(self, x, y, step, length, width, image):
        self.x = x
        self.y = y
        self.step = step
        self.length = length
        self.width = width
        self.image = image

    def move(self, direction):
        self.y += self.step * direction


if __name__ == "__main__":
    main()
