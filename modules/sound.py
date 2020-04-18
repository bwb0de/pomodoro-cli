#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import vlc
import os

from time import sleep

from modules.cli_tools import write_to_file, read_from_file, pick_options

target_bg_snd = '.target_pomodoro_snd'
pasta_sons_de_fundo = 'snd/'
pasta_sons_fx = 'snd/'


def stop_bgsnd():
    try:
        old_pid = read_from_file(target_bg_snd)
        os.kill(int(old_pid), 15)
    except FileNotFoundError: pass
    except ProcessLookupError: pass


def play_bgsnd(filename, filefolder=pasta_sons_de_fundo, loop=False, alarm=False):
    def play(ilefolder, filename):
        stop_bgsnd()
        write_to_file(str(os.getpid()), target_bg_snd)
        filename_obj = vlc.MediaPlayer(filefolder+filename)
        filename_obj.play()
        sleep(2)
        duration = (filename_obj.get_length() / 1000)
        sleep(duration)
        os.remove(target_bg_snd)

    independent_process = os.fork()

    if independent_process == 0:
        if loop:
            while loop:
                loop -= 1
                play(filefolder, filename)
        else:
            play(filefolder, filename)
        
        if alarm:
            play(filefolder, "alarm-ring.ogg")


