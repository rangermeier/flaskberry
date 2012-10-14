# -*- coding: utf-8 -*-
import subprocess
import re
import os

MOUNTPOINTS = ["/home/media/disks/usb%s" % i for i in range(8)]

class Disk(dict):
    def __init__(self, **args):
        if args.has_key("uuid"):
            self.uuid = args["uuid"]
            if self.uuid_exists():
                self.get_device()
                self.get_id()
        if args.has_key("dev"):
            self.dev = args["dev"]
            self.get_id()
        if args.has_key("mount_info"):
            self.parse_info(args["mount_info"])
            self.get_id();
    def parse_info(self, info):
        # info: "/dev/sda2 on / type ext4 (rw,relatime) [Fedora-16]"
        regexp = "^(/.+?)\son\s(/.*?)\stype\s(.+?)\s\((.+?)\)(\s\[(.+)\])?$"
        parts = re.match(regexp, info)
        if parts:
            self.dev = parts.groups()[0]
            self.mountpoint = parts.groups()[1]
            self.type = parts.groups()[2]
            self.options = parts.groups()[3]
            self.label = parts.groups()[5]
            self.mounted = True
    def get_stats(self):
        if not self.mounted:
            return
        df = subprocess.check_output(["df", "-hT", self.dev]).splitlines()
        #/dev/sda7      ext4  424G    340G   63G   85% /home
        parts = re.split("\s+", df[1])
        if parts:
            self.type = parts[1]
            self.size = parts[2]
            self.used = parts[3]
            self.available = parts[4]
            self.usage = parts[5]
            self.mountpoint = parts[6]
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
            else: self.mounted = True
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
        while not os.listdir(mountpoint) == []:
            try:
                mountpoint.next()
            except StopIteration:
                flash("no empty mountpoints")
                return
        return mountpoint
    def mount(self):
        if not self.is_mounted() and self.uuid_exists():
            return subprocess.call(["sudo", "/bin/mount",
                "/dev/disk/by-uuid/%s" % self.uuid, self.find_mountpoint()])
    def unmount(self):
        if self.uuid_exists():
            return subprocess.call(["sudo", "/bin/umount", "/dev/disk/by-uuid/%s" % self.uuid])
