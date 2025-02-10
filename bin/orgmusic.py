#!/usr/bin/python3

from pymediainfo import MediaInfo
import sys
import os
import re
import shutil

class MusicFile:
    def __init__(self, path, ext):
        self.path = path
        self.ext = ext
        self.album = None
        self.performer = None
        self.genre = None
        self.title = None
        self.track_name_position = None
        self.year = None
        self.info = None
        self.fields = ["album", "performer", "genre", "title", "track_name_position"]
        self.load()

    def __str__(self):
        buf = ''
        for field in self.fields:
            value = getattr(self, field)
            buf += "%s: %s" % (field, value)
            buf += "\n"
        return buf

    def load(self):
        self.info = MediaInfo.parse(self.path)
        general = self.info.general_tracks[0]
        for field in self.fields:
            value = getattr(general, field)
            setattr(self, field, value)

def mkdirp(path):
    """Create the full path provided, including any parent directories,
    much like mkdir -p works in Linux."""
    # No spaces allowed.
    print("mkdirp: path is", path)
    assert( path.find(' ') < 0 )
    path = os.path.abspath(path)
    pieces = path.split(os.sep)
    pieces.reverse()
    full_pieces = []
    if pieces[-1] == '':
        pieces.pop()
    while True:
        full_pieces.append(pieces.pop())
        full_path = "/" + os.sep.join(full_pieces)
        print("mkdirp:", full_path)
        if not os.path.exists(full_path):
            print("creating", full_path)
            os.mkdir(full_path)
        if len(pieces) == 0:
            break

def cleanstring(dirty):
    dirty = dirty.strip()
    dirty = dirty.lower()
    dirty = re.sub(r'/', '', dirty)
    dirty = re.sub('\s+', '_', dirty)
    dirty = re.sub('^_+', '', dirty)
    dirty = re.sub('_+$', '', dirty)
    dirty = re.sub('(\(|\))', '', dirty)
    dirty = re.sub('(\[|\])', '', dirty)
    dirty = re.sub("'", '', dirty)
    dirty = re.sub('\*', '-', dirty)
    dirty = re.sub('!', '', dirty)
    dirty = re.sub('&', 'and', dirty)
    return dirty

def manage(out_root, fobj):
    if fobj.performer and fobj.album and fobj.track_name_position and fobj.title:
        title = cleanstring(fobj.title)
        track = int(fobj.track_name_position)
        outpath = os.path.join(out_root, 
                               cleanstring(fobj.performer),
                               cleanstring(fobj.album),
                               "%02d_%s.%s" % (track, title, fobj.ext))
        # The last directory should be the album name.
        pieces = outpath.split(os.sep)
        print("copying", fobj.path, "to", outpath)
        assert( pieces[-2] == cleanstring(fobj.album) )
        mkdirp(os.path.dirname(outpath))
        shutil.copy(fobj.path, outpath)
        return True

    else:
        print("*** data missing needed to compose new path ***")
        return False

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: %s <input dir> <output dir>\n" % sys.argv[0])
        sys.exit(1)

    in_root = sys.argv[1]
    out_root = sys.argv[2]

    unmanaged = []

    for dirpath, dirnames, filenames in os.walk(in_root):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            print("opening", path)
            if filename.endswith('.mp3'):
                fobj = MusicFile(path, 'mp3')
            elif filename.endswith('.m4a'):
                fobj = MusicFile(path, 'm4a')
            else:
                unmanaged.append(path)
                continue
            handled = manage(out_root, fobj)
            if handled:
                print(fobj)
                print('')
            else:
                unmanaged.append(path)

    print("Unmanaged files:")
    for path in unmanaged:
        print("    ", path)

main()
