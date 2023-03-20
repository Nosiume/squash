# -*- coding: utf-8 -*-

import pytest
import squash as squash


def main():
    test_Ball()
    test_Racket()


class WindowInfosFake:
    def __init__(self):
        self.window_tk = "window_tk_fake"
        self.width = 400
        self.height = 400


class RacketFake:
    def __init__(self):
        self.x = 50
        self.y = 200
        self.step = 25
        self.length = 100
        self.width = 30
        self.image = "image_fake"


def test_Ball():
    print("test_ball: ")
    isOk = True
    image = "image_fake"

    window_infos = WindowInfosFake()
    ball = squash.Ball(100, 101, 20, 21, image)
    try:
        if (ball.x != 100
                or ball.y != 101
                or ball.dx != 20
                or ball.dy != 21
                or ball.image != image):
            print("    __init__ not ok")
            isOk = False
        else:
            print("    __init__ ok")
    except AttributeError:
        print("    __init__ not ok")
        print("Can't perform other tests before the constructor is implemented")
        isOk = False
        return

    ball.update_position()
    if (ball.x != 120 or ball.y != 122):
        print("    update_position not ok")
        isOk = False
    else:
        print("    update_position ok")

    racket = RacketFake()
    ball.update_direction(window_infos, racket)
    if (ball.dx != 20 or ball.dy != 21):
        print("    update_direction no collision not ok")
        isOk = False
    else:
        print("    update_direction no collision ok")
    ball.x = 49
    ball.y = 200
    ball.dx = -20
    ball.update_direction(window_infos, racket)
    if (ball.dx != 20 or ball.dy != 21):
        print("    update_direction collision racket not ok")
        isOk = False
    else:
        print("    update_direction collision racket ok")

    ball.y = -50
    ball.dy = -21
    ball.update_direction(window_infos, racket)
    if (ball.dx != 20 or ball.dy != 21):
        print("    update_direction collision up not ok")
        isOk = False
    else:
        print("    update_direction collision up ok")

    ball.y = 450
    ball.dy = 21
    ball.update_direction(window_infos, racket)
    if (ball.dx != 20 or ball.dy != -21):
        print("    update_direction collision down not ok")
        isOk = False
    else:
        print("    update_direction collision down ok")

    return isOk


def test_Racket():
    print("test_racket: ")
    isOk = True
    image = "image_fake"

    racket = squash.Racket(50, 200, 25, 100, 30, image)
    try:
        if (racket.x != 50
                or racket.y != 200
                or racket.step != 25
                or racket.length != 100
                or racket.width != 30
                or racket.image != image):
            print("    __init__ not ok")
            isOk = False
        else:
            print("    __init__ ok")
    except AttributeError:
        print("    __init__ not ok")
        print("Can't perform other tests before the constructor is implemented")
        isOk = False
        return

    racket.move(-1)
    if (racket.x != 50 or racket.y != 175):
        print("    move down not ok")
        isOk = False
    else:
        print("    move down ok")

    racket.y = 200
    racket.move(1)
    if (racket.x != 50 or racket.y != 225):
        print("    move up not ok")
        isOk = False
    else:
        print("    move up ok")

    return isOk

    def move(self, direction):
        self.y += self.step * direction


if __name__ == "__main__":
    main()
