#!/usr/bin/env python3

import os
import distro
import wmctrl
import platform
import re
import subprocess
import json
import time
from subprocess import run

def term_run(command, arguments):
    output = subprocess.run([command, arguments],text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output.stdout

def get_os(architecture=False, remove_linux=False):
    os = distro.name()
    if remove_linux:
        os = re.sub('linux', '', os, flags=re.IGNORECASE)
    os = os.rstrip()
    if architecture:
        os += ' ' + platform.machine()
    os = os.lower()
    return os

def get_wm():
    try:
        return wmctrl.os.environ.get('DESKTOP_SESSION').lower()
    except:
       pass 
    try:
        return wmctrl.os.environ.get('XDG_SESSION_DESKTOP')
    except:
        return None

def get_kernel(full_name=True):
    kernel = platform.release()
    if not full_name:
        kernel = kernel.split('-')[0]
    return kernel

def get_packages(display_package_manager=False):
    try:
        packages = term_run('pacman', '-Qq')
        string = str(len(packages.split('\n')))
        if display_package_manager:
            string += ' (pacman)'
        return string
    except:
        return None


def check_colors(num: int):
    if num < 7:
        return True
    if num > 7 :
        return False

def trans_color(num: int):
    if num == 0:
        return '\033[30m'
    elif num == 1:
        return '\033[31m'
    elif num == 2:
        return '\033[32m'
    elif num == 3:
        return '\033[33m'
    elif num == 4:
        return '\033[34m'
    elif num == 5:
        return '\033[35m'
    elif num == 6:
        return '\033[36m'
    elif num == 7:
        return '\033[37m'
    else:
        return ''



def main(color_a:str, color_b:str):
    bold = "\u001b[1m"
    reset = "\033[0m"
    linux_os = get_os(remove_linux=True)
    wm = get_wm()
    de = subprocess.Popen(['wmctrl -m | grep "Name"'], stdout=subprocess.PIPE,shell=True).communicate()[0]
    de = str(de, "utf-8").strip("\n").strip("Name:").replace(" ","").lower()
    kernel = get_kernel(full_name=False)
    pkgs = get_packages(display_package_manager=False)
    shell = wmctrl.getoutput("echo $SHELL").replace("/","").replace("bin","")

    base = f""".
{reset}├─ {bold}{color_a}distro{reset}
{reset}│  ├─ {color_b}{linux_os}{reset}
{reset}│  └─ {color_b}{kernel}{reset}
{reset}├─ {bold}{color_a}pacman{reset}
{reset}│  └─ {bold}{color_a}packages{reset}
{reset}│     └─ {color_b}{pkgs}{reset}
{reset}├─ {bold}{color_a}env{reset}
{reset}│  ├─ {bold}{color_b}de{reset}
{reset}│  │  └─ {color_b}{de}{reset}
{reset}│  └─ {bold}{color_b}wm{reset}
{reset}│     └─ {color_b}{wm}{reset}
{reset}└─ {bold}{color_a}shell{reset}
{reset}   └─ {color_b}{shell}{reset}"""

    print(base)


if __name__ == '__main__':
    default = None
    try:
        with open('./config.json') as f:
            data = json.load(f)
    except:
        print(
            "Missing Config File (config.json).\n\n"
            "You can link the full path to it on line 114 of tfetch\n"
            "Example: /Users/Peregrine/Desktop/tfetch/config.json"
        )
        exit()

    # Check the data

    color1check = check_colors(data['color1'])
    color2check = check_colors(data['color2'])

    if color1check == True:
        color_a = trans_color(data['color1'])
    else:
        color_a = ""

    if color2check == True:
        color_b = trans_color(data['color2'])
    else:
        color_b = ""

    if color1check == True and color2check == True:
        main(color_a, color_b)
    else:
        print(" -> Using Default Config.")
        time.sleep(1)
        os.system("clear")
        main("\033[31m","\033[33m")

