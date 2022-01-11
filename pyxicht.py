#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# PyXicht - Visual CPU load monitoring tool using a HUD face display
# Main script
# Copyright (C) 2022 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/pyxicht
# GitLab: https://gitlab.com/urbanware-org/pyxicht
#


__version__ = "1.0.0"

import os
import psutil
import random
import sys

from core import images
from PyQt4 import QtCore, QtGui, uic


script_dir = os.path.dirname(sys.argv[0])
image_dir = os.path.join(script_dir, "images")
iface_dir = os.path.join(script_dir, "ui")

interface = os.path.join(iface_dir, "main.ui")
qtCreatorFile = interface
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class PyXicht(QtGui.QMainWindow, Ui_MainWindow):
    """
        Visual CPU load monitoring class.
    """
    health = 100
    health_before = 100
    images.face_direction = 0
    measure_skip_loop = 0   # count of skipped loops
    measure_skip_limit = 3

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.setWindowTitle("pyxicht")
        self.setStyleSheet("background-color: black;")
        set_pixmap(self.face, images.face_invincible)

    def face_hurt(self):
        """
            Method to show the corresponding hurt face depending on direction
            and health.
        """
        if self.health > 80:
            if self.face_direction == 1:
                set_pixmap(self.face, images.face_hurt_left_100)
            elif self.face_direction == 2:
                set_pixmap(self.face, images.face_hurt_right_100)
            else:
                set_pixmap(self.face, images.face_hurt_center_100)
        elif self.health > 60:
            if self.face_direction == 1:
                set_pixmap(self.face, images.face_hurt_left_80)
            elif self.face_direction == 2:
                set_pixmap(self.face, images.face_hurt_right_80)
            else:
                set_pixmap(self.face, images.face_hurt_center_80)
        elif self.health > 40:
            if self.face_direction == 1:
                set_pixmap(self.face, images.face_hurt_left_60)
            elif self.face_direction == 2:
                set_pixmap(self.face, images.face_hurt_right_60)
            else:
                set_pixmap(self.face, images.face_hurt_center_60)
        elif self.health > 20:
            if self.face_direction == 1:
                set_pixmap(self.face, images.face_hurt_left_40)
            elif self.face_direction == 2:
                set_pixmap(self.face, images.face_hurt_right_40)
            else:
                set_pixmap(self.face, images.face_hurt_center_40)
        else:
            if self.face_direction == 1:
                set_pixmap(self.face, images.face_hurt_left_20)
            elif self.face_direction == 2:
                set_pixmap(self.face, images.face_hurt_right_20)
            else:
                set_pixmap(self.face, images.face_hurt_center_20)

    def face_look(self):
        """
            Method to show the corresponding "normal" face depending on
            direction and health.
        """
        if self.health > 80:
            if self.face_direction == 1:
                set_pixmap(self.face, images.face_look_left_100)
            elif self.face_direction == 2:
                set_pixmap(self.face, images.face_look_right_100)
            else:
                set_pixmap(self.face, images.face_look_center_100)
        elif self.health > 60:
            if self.face_direction == 1:
                set_pixmap(self.face, images.face_look_left_80)
            elif self.face_direction == 2:
                set_pixmap(self.face, images.face_look_right_80)
            else:
                set_pixmap(self.face, images.face_look_center_80)
        elif self.health > 40:
            if self.face_direction == 1:
                set_pixmap(self.face, images.face_look_left_60)
            elif self.face_direction == 2:
                set_pixmap(self.face, images.face_look_right_60)
            else:
                set_pixmap(self.face, images.face_look_center_60)
        elif self.health > 20:
            if self.face_direction == 1:
                set_pixmap(self.face, images.face_look_left_40)
            elif self.face_direction == 2:
                set_pixmap(self.face, images.face_look_right_40)
            else:
                set_pixmap(self.face, images.face_look_center_40)
        else:
            if self.face_direction == 1:
                set_pixmap(self.face, images.face_look_left_20)
            elif self.face_direction == 2:
                set_pixmap(self.face, images.face_look_right_20)
            else:
                set_pixmap(self.face, images.face_look_center_20)

    def face_shocked(self):
        """
            Method to show corresponding hurt face depending on health.
        """
        if self.health > 80:
            set_pixmap(self.face, images.face_shock_100)
        elif self.health > 60:
            set_pixmap(self.face, images.face_shock_80)
        elif self.health > 40:
            set_pixmap(self.face, images.face_shock_60)
        elif self.health > 20:
            set_pixmap(self.face, images.face_shock_40)
        else:
            set_pixmap(self.face, images.face_shock_20)

    def face_smile(self):
        """
            Method to show corresponding smile face depending on health.
        """
        if self.health > 80:
            set_pixmap(self.face, images.face_smile_100)
        elif self.health > 60:
            set_pixmap(self.face, images.face_smile_80)
        elif self.health > 40:
            set_pixmap(self.face, images.face_smile_60)
        elif self.health > 20:
            set_pixmap(self.face, images.face_smile_40)
        else:
            set_pixmap(self.face, images.face_smile_20)

    def main_loop(self):
        """
            Main loop connected with the timer.
        """
        random.seed()
        self.face_direction = random.randint(0, 2)

        if self.measure_skip_loop == 0:
            health = int(100 - psutil.cpu_percent())
            if health < 0:
                health = 0
            elif health > 100:
                health = 100
            self.health = health
            title = str(health) + " %"
            self.setWindowTitle(title)
            self.measure_skip_loop += 1
        else:
            health = self.health
            self.measure_skip_loop += 1
            if self.measure_skip_loop == self.measure_skip_limit:
                self.measure_skip_loop = 0

        if health == 0:
            set_pixmap(self.face, images.face_dead)
        elif health == 100:
            set_pixmap(self.face, images.face_invincible)
        else:
            if health > self.health_before:
                if (health - self.health_before) > 10:
                    self.face_smile()
            elif health < self.health_before:
                if (self.health_before - health) > 20:
                    self.face_shocked()
                elif (self.health_before - health) > 5:
                    self.face_hurt()
            else:
                self.face_look()
        self.health_before = health


def set_pixmap(obj, pixmap):
    """
        Method to simply set a pixmap for a QLabel object.
    """
    p = QtGui.QPixmap(pixmap)
    obj.setPixmap(p)


if __name__ == "__main__":
    print("PyXicht " + __version__)
    print("Image directory is '%s'" % image_dir)

    app = QtGui.QApplication(sys.argv)
    app_icon = QtGui.QIcon()
    app.setWindowIcon(app_icon)

    pyxicht = PyXicht()
    pyxicht.show()

    timer = QtCore.QTimer()
    timer.timeout.connect(pyxicht.main_loop)
    timer.start(480)

    sys.exit(app.exec_())

# EOF
