#!/usr/bin/python2

import argparse
import os
import json
from subprocess import Popen, PIPE

import pygtk  
pygtk.require('2.0')  
import gtk  
import wnck  

script_path = os.path.dirname(os.path.realpath(__file__))
settings = "{}/data".format(script_path)
script = os.path.realpath(__file__)
icon_path = '/tmp/winman'

def load_vals():
    f = open(settings, 'r')
    line = f.readline()
    return json.loads(line) if line else {}

def save_vals(data):
    f = open(settings, 'w')
    f.write(json.dumps(data))

def save(n):
    wins = load_vals()
    if not n in wins:
        wins[n] = {}

    screen = wnck.screen_get_default()  
    while gtk.events_pending():  
        gtk.main_iteration(False)  
    w = screen.get_active_window()
    wins[n]['name'] = w.get_name()  
    wins[n]['app'] = w.get_application().get_name()
    if not os.path.exists(icon_path):
        os.mkdir(icon_path)
    icon_file = "{}/icon-{}.png".format(icon_path, n)
    icon_pixbuf = w.get_icon()
    icon_pixbuf.save(icon_file, "png")
    wins[n]['icon'] = icon_file
    wins[n]['xid'] = w.get_xid()
    # print wins
    save_vals(wins)


def config():
    for x in xrange(0,10):
        out, err = Popen("xfconf-query -c xfce4-keyboard-shortcuts -p '/commands/custom/<Primary><Super>{}' -s '{} -s {}'".format(x, script, x), stderr=PIPE, shell=True).communicate()
        if err:
            Popen("xfconf-query -c xfce4-keyboard-shortcuts -p '/commands/custom/<Primary><Super>{}' -n -t string -s '{} -s {}'".format(x, script, x), stderr=PIPE, shell=True)
        out, err = Popen("xfconf-query -c xfce4-keyboard-shortcuts -p '/commands/custom/<Super>{}' -s '{} -a {}'".format(x, script, x), stderr=PIPE, shell=True).communicate()
        if err:
            Popen("xfconf-query -c xfce4-keyboard-shortcuts -p '/commands/custom/<Super>{}' -n -t string -s '{} -a {}'".format(x, script, x), stderr=PIPE, shell=True)
            


def activate(n):
    wins = load_vals()
    if n in wins:
        out, err = Popen("wmctrl -i -a {}".format(wins[n]['xid']), stderr=PIPE, shell=True).communicate()
        if err:
            Popen(["notify-send", "Unknown window", "{} <b>[{}]</b>".format(wins[n]['name'], n), "-u", "low", "-i", "{}/xfce-square.png".format(script_path)])
            removed = wins.pop(n, None)
            if removed:
                save_vals(wins)
    else:
        Popen(["notify-send", "Window manager", "No saved window <b>[{}]</b>".format(n), "-u", "low", "-i", "{}/xfce-square.png".format(script_path)])


def list_windows():
    print load_vals()


def touch_data_file():
    if not os.path.exists(settings):
        os.mknod(settings)
        f = open(settings, 'w')
        f.write("{}")

def delete_data():
    os.unlink(settings)
    touch_data_file()


if __name__ == "__main__":
    touch_data_file()
    parser = argparse.ArgumentParser(description='Window manager')
    parser.add_argument('-s', '--save', required=False)
    parser.add_argument('-a', '--activate', required=False)
    parser.add_argument('-l', '--list', required=False, action='store_true')
    parser.add_argument('-c', '--config', required=False, action='store_true')
    parser.add_argument('-d', '--delete', required=False, action='store_true')
    args = parser.parse_args()
    if args.save:
        save(args.save)
    elif args.activate:
        activate(args.activate)
    elif args.list:
        list_windows()
    elif args.config:
        config()
    elif args.delete:
        delete_data()
