import os
import re
from glob import glob
from urllib.request import urlopen, urlretrieve
from time import time
from zipfile import ZipFile
from collections import namedtuple
from wca_api.table import Table

def update_tsv_export(reporthook=None):
    """If export is missing or not current, download the current one.
       Returns True iff the export was updated."""

    # Is export file missing or older than 10 minutes?
    here = glob('WCA_export*_*.tsv.zip')
    if not here or time() - os.stat(max(here)).st_mtime > 10 * 60:

        # What's the current export on the WCA site?
        base = 'https://www.worldcubeassociation.org/results/misc/'
        try:
            print('downloading the newest export...')
            with urlopen(base + 'export.html') as file:
                current = re.search(r'WCA_export\d+_\d+.tsv.zip', str(file.read())).group(0)
        except:
            print('failed looking for the newest export')
            return

        # Download if necessary, otherwise mark local as up-to-date
        if not os.path.isfile(current):
            if not reporthook:
                print('downloading export', current, '...')
            urlretrieve(base + current, current, reporthook)
            for here_file in here:
                if here_file != current:
                    os.remove(here_file)
            return True
        else:
            os.utime(max(here))


def load(wanted_table, wanted_columns):
    with ZipFile(max(glob('WCA_export*_*.tsv.zip'))) as zipfile:
        with zipfile.open('WCA_export_' + wanted_table + '.tsv') as tablefile:
            column_names, *rows = [line.split('\t') for line in
                                   tablefile.read().decode().splitlines()]

            wanted_columns = wanted_columns.split()
            Type = namedtuple(wanted_table, wanted_columns)

            columns = []
            for name in wanted_columns:
                i = column_names.index(name)
                column = [row[i] for row in rows]
                try:
                    column = list(map(int, column))
                except:
                    pass
                columns.append(column)

            return Table([Type(*row) for row in zip(*columns)])
