# -*- coding: utf-8 -*-
import subprocess
import re
import os
import psutil

MOUNTPOINTS = ["/home/media/disks/usb%s" % i for i in range(8)]

class Disk(dict):
    def __init__(self, **args):
        self.mounted = False
        if args.has_key("uuid"):
            self.uuid = args["uuid"]
            if self.uuid_exists():
                self.get_device()
                self.get_id()
        if args.has_key("dev"):
            self.dev = args["dev"]
            self.get_id()
        if args.has_key("partition"):
            self.set_partition_info(args["partition"])
            self.get_id();

    def set_partition_info(self, info):
        self.dev = info.device
        self.mountpoint = info.mountpoint
        self.type = info.fstype
        self.options = info.opts
        self.mounted = True

    def get_usage(self):
        if not self.is_mounted():
            return
        self.usage = psutil.disk_usage(self.mountpoint)

    def get_id(self):
        blkid = subprocess.check_output(["sudo", "blkid", "-p", self.dev])
        #/dev/sdb1: LABEL="Kingston" UUID="1C86-3319" VERSION="FAT32" TYPE="vfat"
        fields = ["label", "uuid", "version", "type"]
        for field in fields:
            regexp = '%s="(.+?)"' % field.upper()
            parts = re.search(regexp, blkid)
            if parts:
                self[field] = parts.groups()[0]

    def get_device(self):
        if not self.has_key("dev"):
            self.dev = subprocess.check_output(["sudo", "blkid", "-U", self.uuid]).rstrip()
        return self.dev

    def is_mounted(self):
        if not self.has_key("mounted"):
            df = subprocess.check_output(["df", "-hT", self.dev]).splitlines()[1]
            if re.search("/dev$", df):
                self.mounted = False
            else: 
                self.mounted = True
        return self.mounted

    def is_mountable(self):
        mountable = False;
        if self.has_key("uuid") and self.has_key("type"):
            if not self["type"].startswith("crypto_"):
                if self["type"] != "swap":
                    mountable = True
        return mountable

    def uuid_exists(self):
        return os.path.exists("/dev/disk/by-uuid/%s" % self.uuid)

    def find_mountpoint(self):
        # look for fstab entries
        with open("/etc/fstab") as fstab:
            regexp = re.compile("UUID=%s\s+?(/.*?)\s" % self.uuid)
            for line in fstab.readlines():
                match = regexp.match(line)
                if match:
                    return match.groups()[0]
        # try empty media directories
        mi = iter(MOUNTPOINTS)
        mountpoint = mi.next()
        while os.path.exists(mountpoint) and not os.listdir(mountpoint) == []:
            try:
                mountpoint.next()
            except StopIteration:
                return
        if not os.path.exists(mountpoint):
            return None
        return mountpoint

    def mount(self):
        mountpoint = self.find_mountpoint()
        if mountpoint and not self.is_mounted() and self.uuid_exists():
            subprocess.call(["sudo", "/bin/mount",
                "/dev/disk/by-uuid/%s" % self.uuid, mountpoint])
            self.mounted = True
            return True
        return False 

    def unmount(self):
        if self.uuid_exists():
            return subprocess.call(["sudo", "/bin/umount", "/dev/disk/by-uuid/%s" % self.uuid])
