#!/usr/bin/python

import sys, pyexifinfo, datetime, os.path, shutil, logging, hashlib, exifread

datetag_exiftool = 'EXIF:DateTimeOriginal'
datetag_exifread = 'EXIF DateTimeOriginal'

logging.basicConfig()
log = logging.getLogger('manage_photos')
log.setLevel(logging.DEBUG)

month_map = {
    '1': '01_January',
    '2': '02_February',
    '3': '03_March',
    '4': '04_April',
    '5': '05_May',
    '6': '06_June',
    '7': '07_July',
    '8': '08_August',
    '9': '09_September',
    '10': '10_October',
    '11': '11_November',
    '12': '12_December'
    }

class MediaFile(object):
    def __init__(self, path):
        self.path = path
        self.md5 = None
        inputfile = None
        try:
            inputfile = open(path, 'r')
            # Take md5 of file for comparison with others
            self.md5 = hashlib.md5(inputfile.read()).hexdigest()
            log.debug("md5sum: %s", self.md5)
            # Use exifread on image files, it's faster.
            if self.path.endswith('.jpg') or self.path.endswith('.jpeg'):
                inputfile.seek(0)
                self.tags = exifread.process_file(inputfile,
                                                  details=False,
                                                  stop_tag=datetag_exifread)
            else:
                self.tags = pyexifinfo.get_json(self.path)[0]

            datestring = None
            if datetag_exiftool in self.tags:
                # Try two date formats.
                datestring = self.tags[datetag_exiftool].strip()
            elif datetag_exifread in self.tags:
                datestring = self.tags[datetag_exifread].printable.strip()

            if datestring:
                log.debug("date in exif looks like this: '%s'", datestring)
                try:
                    log.debug("trying first format")
                    self.dt = datetime.datetime.strptime(
                        datestring,
                        "%Y:%m:%d %H:%M:%S")
                except:
                    log.debug("First date format failed, trying second")
                    self.dt = datetime.datetime.strptime(
                        datestring,
                        "%Y-%m-%d %H:%M:%S")
            else:
                self.dt = None

        except Exception as err:
            log.exception("Error processing %s: %s\n", path, str(err))
            sys.exit(1)
        finally:
            if inputfile is not None:
                inputfile.close()

    def __str__(self):
        return "MediaFile: %s, %s" % (self.path, self.dt)

    def __repr__(self):
        return str(self)

def visit(media_files, dirname, names):
    extensions = ['jpg', 'jpeg', 'mp4', 'avi']
    for name in names:
        path = os.path.join(dirname, name)
        if not os.path.isfile(path):
            continue
        try:
            pieces = name.split('.')
            extension = pieces[-1]
            if extension not in extensions:
                log.info("Unsupported file type: %s", path)
                continue

        except IndexError:
            log.info("Unsupported file: %s", path)
            continue

        log.info("Processing media_file: %s", path)
        media_file = MediaFile(path)
        if media_file.dt:
            media_files.setdefault(str(media_file.dt.year),
                              {}).setdefault(str(media_file.dt.month),
                                             []).append(media_file)
        else:
            log.warn("No datetime found for %s", media_file.path)
            media_files.setdefault('unsorted', []).append(media_file)

def copy_media_files(media_files, output_path):
    log.info("Copying media_files to %s", output_path)
    if not os.path.exists(output_path):
        log.info("Creating", output_path)
        os.mkdir(output_path)
    elif not os.path.isdir(output_path):
        raise IOError, "%s is not a directory" % output_path

    for year in media_files:
        year_path = os.path.join(output_path, year)
        if not os.path.exists(year_path):
            log.info("Creating", year_path)
            os.mkdir(year_path)
        elif not os.path.isdir(year_path):
            raise IOError, "%s is not a directory" % year_path

        if year == 'unsorted':
            for media_file in media_files[year]:
                dest = os.path.join(year_path, os.path.basename(media_file.path))
                log.info("Copying %s to %s...", media_file.path, dest)
                shutil.copy(media_file.path, dest)

        else:
            # Otherwise, we make a directory by the month name and copy the
            # files there.
            for month in media_files[year]:
                month_path = os.path.join(year_path, month_map[month])
                if not os.path.exists(month_path):
                    log.info("Creating %s", month_path)
                    os.mkdir(month_path)
                elif not os.path.isdir(month_path):
                    raise IOError, "%s is not a directory" % month_path

                for media_file in media_files[year][month]:
                    dest = os.path.join(month_path, os.path.basename(media_file.path))
                    log.info("Copying %s to %s...", media_file.path, dest)
                    shutil.copy(media_file.path, dest)

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: %s <input paths> <output dir>\n" % sys.argv[0])
        sys.exit(1)

    input_paths = sys.argv[1:-1]
    output_path = sys.argv[-1]

    media_files = {}

    for path in input_paths:
        if os.path.isfile(path):
            visit(media_files, os.path.dirname(path), [os.path.basename(path)])
        elif os.path.isdir(path):
            os.path.walk(path, visit, media_files)
        else:
            log.warn("Skipping non-file, non-dir", path)

    # Look for duplicate files.
    hashmap = {}
    for year in media_files:
        if year == 'unsorted':
            continue
        for month in media_files[year]:
            for media_file in media_files[year][month]:
                hashmap.setdefault(media_file.md5, []).append(media_file)
    for md5 in hashmap:
        if len(hashmap[md5]) > 1:
            log.warn("duplicate media_files found:")
            for i, media_file in enumerate(sorted(hashmap[md5])):
                log.warn("    %s", media_file)
                if i != 0:
                    log.warn("    suggest deletion: %s", media_file.path)

    copy_media_files(media_files, output_path)

main()
