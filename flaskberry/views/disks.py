# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash
import subprocess
import re
import glob
from flaskberry.models.disks import Disk

mod = Blueprint('disks', __name__)

@mod.route('/')
def index():
    disks = []
    mounts = subprocess.check_output(["/bin/mount", "-l"]).splitlines( )
    regexp = re.compile("^/dev/sd.[1-9]")
    for mount in mounts:
        if re.match(regexp, mount):
            disk = Disk(mount_info=mount)
            disk.get_stats()
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

