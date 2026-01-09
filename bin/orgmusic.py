#!/usr/bin/python3

from pymediainfo import MediaInfo
import sys
import os
import os.path
import re
import shutil
import argparse

class MusicFile:
    def __init__(self, path):
        self.path = path
        self.path_no_ext, self.ext = self.parse_path()
        if self.ext is None:
            return None
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

    def parse_path(self):
        file_types = ["mp3", "m4a"]
        for ftype in file_types:
            if self.path.endswith("." + ftype):
                no_ext = self.path[:-4]
                ext = ftype
                return (no_ext, ext)
        return None, None

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
    dirty = re.sub(r'\s+', '_', dirty)
    dirty = re.sub(r'^_+', '', dirty)
    dirty = re.sub(r'_+$', '', dirty)
    dirty = re.sub(r'(\(|\))', '', dirty)
    dirty = re.sub(r'(\[|\])', '', dirty)
    dirty = re.sub(r"'", '', dirty)
    dirty = re.sub(r'\*', '-', dirty)
    dirty = re.sub(r'!', '', dirty)
    dirty = re.sub(r'&', 'and', dirty)
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

def parse_options():
    parser = argparse.ArgumentParser(description="Music manager")
    parser.add_argument('-g',
                        '--genre-report',
                        dest='genre',
                        action='store_true',
                        default=False,
                        help='Just query music and generate a genre report')
    parser.add_argument('input',
                        action='append',
                        nargs='+',
                        default=[],
                        help="Directories of files or files")
    options = parser.parse_args()
    return options

def main():
    options = parse_options()
    if len(options.input) < 1:
        sys.stderr.write("Usage: %s [options] <input dir or files> [output dir]\n" % sys.argv[0])
        sys.exit(1)

    input_files = options.input[0]
    if len(input_files) > 1:
        in_roots = input_files[:-1]
        out_root = input_files[-1]
    else:
        in_roots = input_files[0]
        out_root = None

    unmanaged = []
    all_files = []

    for in_root in in_roots:
        if os.path.isdir(in_root):
            for dirpath, dirnames, filenames in os.walk(in_root):
                for filename in filenames:
                    path = os.path.join(dirpath, filename)
                    fobj = MusicFile(path)
                    if fobj is not None:
                        all_files.append(fobj)
                    else:
                        unmanaged.append(path)
        else:
            fobj = MusicFile(in_root)
            if fobj is not None:
                all_files.append(fobj)
            else:
                unmanaged.append(path)

    print("All files:")
    for fobj in all_files:
        print(fobj)

    #for fobj in all_files:
    #    handled = manage(out_root, fobj)
    #    if handled:
    #        print(fobj)
    #        print('')
    #    else:
    #        unmanaged.append(path)

    #print("Unmanaged files:")
    #for path in unmanaged:
    #    print("    ", path)

main()
