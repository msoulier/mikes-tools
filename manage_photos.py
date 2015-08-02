#!/usr/bin/python

import sys, exifread, datetime, os.path, shutil

datetag = 'EXIF DateTimeOriginal'

class Image(object):
    def __init__(self, path):
        self.path = path
        inputfile = None
        try:
            inputfile = open(path, 'r')
            self.tags = exifread.process_file(inputfile, stop_tag=datetag)
            if datetag in self.tags:
                self.dt = datetime.datetime.strptime(
                    self.tags[datetag].printable,
                    "%Y:%m:%d %H:%M:%S")
            else:
                self.dt = None

        except Exception as err:
            sys.stderr.write("Error processing %s: %s\n" % (path, str(err)))
            sys.exit(1)
        finally:
            if inputfile is not None:
                inputfile.close()

    def __str__(self):
        return "Image: %s, %s" % (self.path, self.dt)

    def __repr__(self):
        return str(self)

def visit(images, dirname, names):
    for name in names:
        path = os.path.join(dirname, name)
        # We only care about .jpg or .jpeg files.
        if name[-4:] != '.jpg' and name[-5:] != '.jpeg':
            print "Skipping", path
            continue
        print "Processing image", path
        image = Image(path)
        if image.dt:
            images.setdefault(str(image.dt.year),
                              {}).setdefault(str(image.dt.month),
                                             []).append(image)
        else:
            images.setdefault('unsorted', []).append(image)

def copy_images(images, output_path):
    print "Copying images to", output_path
    if not os.path.exists(output_path):
        print "Creating", output_path
        os.mkdir(output_path)
    elif not os.path.isdir(output_path):
        raise IOError, "%s is not a directory" % output_path

    for year in images:
        year_path = os.path.join(output_path, year)
        if not os.path.exists(year_path):
            print "Creating", year_path
            os.mkdir(year_path)
        elif not os.path.isdir(year_path):
            raise IOError, "%s is not a directory" % year_path

        if year == 'unsorted':
            for image in images[year]:
                dest = os.path.join(year_path, os.path.basename(image.path))
                print "Copying %s to %s..." % (image.path, dest)
                shutil.copy(image.path, dest)

        else:
            # Otherwise, we make a directory by the month name and copy the
            # files there.
            for month in images[year]:
                month_path = os.path.join(year_path, month)
                if not os.path.exists(month_path):
                    print "Creating", month_path
                    os.mkdir(month_path)
                elif not os.path.isdir(month_path):
                    raise IOError, "%s is not a directory" % month_path

                for image in images[year][month]:
                    dest = os.path.join(month_path, os.path.basename(image.path))
                    print "Copying %s to %s..." % (image.path, dest)
                    shutil.copy(image.path, dest)

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: %s <input paths> <output dir>\n" % sys.argv[0])
        sys.exit(1)

    input_paths = sys.argv[1:-1]
    output_path = sys.argv[-1]

    images = {}

    for path in input_paths:
        if os.path.isfile(path):
            visit(images, os.path.dirname(path), [os.path.basename(path)])
        elif os.path.isdir(path):
            os.path.walk(path, visit, images)
        else:
            print "Skipping non-file, non-dir", path

    copy_images(images, output_path)

main()
