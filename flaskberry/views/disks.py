# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash
import subprocess
import re
import glob
import psutil
from flaskberry.models.disk import Disk

mod = Blueprint('disks', __name__)

@mod.route('/')
def index():
    disks = []
    regexp = re.compile("^/dev/sd.[1-9]")
    for md in psutil.disk_partitions(all=False):
        if re.match(regexp, md.device):
            disk = Disk(partition=md)
            disk.get_usage()
            disks.append(disk)

    devices = glob.glob("/dev/sd*[0-9]")
    mounted_devices = [disk.dev for disk in disks]
    for dev in devices:
        if not dev in mounted_devices:
            disk = Disk(dev=dev)
            if disk.is_mountable():
                disks.append(disk)

    return render_template('disks/disks.html', disks=disks)

@mod.route('/<uuid>/mount')
def mount(uuid):
    disk = Disk(uuid=uuid)
    print disk.mount()
    flash("Mounting %s" % disk.dev)
    return redirect(url_for('.index'))

@mod.route('/<uuid>/unmount')
def unmount(uuid):
    disk = Disk(uuid=uuid)
    if disk.is_mounted:
        disk.unmount()
        flash("Unmounting %s" % disk.dev)
    else:
        flash("Disk not mounted")
    return redirect(url_for('.index'))

