# -*- coding: utf-8 -*-
import os
import subprocess
import psutil
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash

mod = Blueprint('system', __name__)

@mod.route('/')
def index():
    uptime = datetime.now() - datetime.fromtimestamp(psutil.get_boot_time())
    return render_template('system/system.html',
            uptime = str(uptime).split('.')[0],
            load = os.getloadavg(),
            net = psutil.net_io_counters(),
            memory = psutil.virtual_memory(),
            swap = psutil.swap_memory(),
        )

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
