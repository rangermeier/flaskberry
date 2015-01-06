import struct, os

class OSFile:
    def __init__(self, path):
        self.path = path
        self.size = long(os.path.getsize(path))

    # source:  http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes#Python
    def hash_file(self):
        try:

            longlongformat = '<q'  # little-endian long long
            bytesize = struct.calcsize(longlongformat)

            f = open(self.path, "rb")

            filesize = int(self.size)
            hash = filesize

            if filesize < 65536 * 2:
                return "SizeError"

            for x in range(65536/bytesize):
                buffer = f.read(bytesize)
                (l_value,)= struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number

            f.seek(max(0,filesize-65536),0)
            for x in range(65536/bytesize):
                buffer = f.read(bytesize)
                (l_value,)= struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF

            f.close()
            returnedhash =  "%016x" % hash
            return returnedhash

        except(IOError):
            return "IOError"
