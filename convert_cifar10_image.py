import urllib
import os
import sys
import tarfile
import glob
import pickle


def download_and_uncompress_tarball(tarball_url, dataset_dir):
    filename = tarball_url.split("\\")[-1]
    filepath = os.path.join(dataset_dir, filename)

    def _progress(count, block_size, total_size):
        sys.stdout.write('\r>> Downloading %s %.1f%%' % (
            filename, float(count * block_size) / float(total_size) * 100.0))
        sys.stdout.flush()

    filepath, _ = urllib.request.urlretrieve(tarball_url, filepath, _progress)
    print()

