# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash
import subprocess

def check_output(*args):
    return subprocess.Popen(*args, stdout=subprocess.PIPE).communicate()[0]

mod = Blueprint('system', __name__)

@mod.route('/')
def index():
    uptime = check_output(["uptime"])
    return render_template('system/system.html', uptime=uptime)

@mod.route('/shutdown')
def shutdown():
    flash("Shutting down.<br>When the LEDs on the board stop flashing, \
    it should be safe to unplug your Raspberry Pi.")
    subprocess.call(["sudo", "halt"])
    return redirect(url_for('system.index'))

@mod.route('/reboot')
def reboot():
    flash("Rebooting... please wait.<br>This will take approx. one minute.")
    subprocess.call(["sudo", "reboot"])
    return redirect(url_for('system.index'))
