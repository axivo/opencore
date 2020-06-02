#!/usr/bin/env python

from io import BytesIO
from multiprocessing import cpu_count
from os import chmod, listdir, makedirs, path, remove, stat, walk
from shutil import copy2, rmtree
from subprocess import check_output
from urllib2 import urlopen
from zipfile import BadZipfile, ZipFile


def main(directory):
    install_opencore('0.5.9', directory)
    install_lilu('1.4.5', '{}/EFI/OC/Kexts'.format(directory))
    install_night_shift_enabler('1.0.0', '{}/EFI/OC/Kexts'.format(directory))
    install_whatevergreen('1.4.0', '{}/EFI/OC/Kexts'.format(directory))
    run_post_install_tasks(directory)


def copytree(source, destination):
    """ Copies directories and files recursively. """
    if not path.exists(destination):
        makedirs(destination)
    for item in listdir(source):
        s = path.join(source, item)
        d = path.join(destination, item)
        if path.isdir(s):
            copytree(s, d)
        else:
            if not path.exists(d) or stat(s).st_mtime - stat(d).st_mtime > 1:
                copy2(s, d)


def extract_files(file, directory):
    """ Extracts the contents of a zip file directly from Internet. """
    try:
        print('  - downloading component...'),
        response = urlopen(file)
    except Exception as e:
        print(e)

    try:
        print('OK')
        print('  - building files structure...'),
        zipfile = ZipFile(BytesIO(response.read()))
    except BadZipfile as e:
        print(e)
 
    for i in zipfile.namelist():
        zipfile.extract(i, directory)
    zipfile.close()
    print('OK')


def install_lilu(version, directory, debug=False):
    """ Builds the Lilu files structure. """
    release_type = 'DEBUG' if debug else 'RELEASE'
    release = 'Lilu-{}-{}.zip'.format(version, release_type)
    repo = 'https://github.com/acidanthera/Lilu/releases'
    file = '{}/download/{}/{}'.format(repo, version, release)

    print_bold('* Lilu {}'.format(version))
    extract_files(file, directory)
    rmtree('{}/{}'.format(directory, 'Lilu.kext.dSYM'))


def install_night_shift_enabler(version, directory, debug=False):
    """ Builds the NightShiftEnabler plugin files structure. """
    release_type = 'DEBUG' if debug else 'RELEASE'
    release = 'NightShiftEnabler-{}-{}.zip'.format(version, release_type)
    repo = 'https://github.com/cdf/NightShiftEnabler/releases'
    file = '{}/download/{}/{}'.format(repo, version, release)

    print_bold('* NightShiftEnabler {}'.format(version))
    extract_files(file, directory)
    rmtree('{}/{}'.format(directory, 'NightShiftEnabler.kext.dSYM'))


def install_opencore(version, directory, debug=False):
    """ Builds the OpenCore files structure. """
    release_type = 'DEBUG' if debug else 'RELEASE'
    release = 'OpenCore-{}-{}.zip'.format(version, release_type)
    repo = 'https://github.com/acidanthera/OpenCorePkg/releases'
    file = '{}/download/{}/{}'.format(repo, version, release)

    print_bold('* OpenCore {}'.format(version))
    if path.isdir(directory):
        print('  - cleaning directory...'),
        rmtree(directory)
        print('OK')
    extract_files(file, directory)
    for i in ['Docs', 'Utilities']:
        rmtree('{}/{}'.format(directory, i))

    if cpu_count() > 15:
        print('  - installing AppleMCEReporterDisabler...'),
        source = 'files/AppleMCEReporterDisabler.kext'
        destination = '{}/EFI/OC/Kexts/AppleMCEReporterDisabler.kext'.format(directory)
        copytree(source, destination)
        print('OK')

    source = 'files/OcBinaryData'
    destination = '{}/EFI/OC'.format(directory)
    print('  - copying OcBinaryData files...'),
    check_output(['git', 'submodule', 'update', '--init', '--remote', '--merge'])
    copytree('{}/Resources'.format(source), '{}/Resources'.format(destination))
    print('OK')


def install_whatevergreen(version, directory, debug=False):
    """ Builds the WhateverGreen files structure. """
    release_type = 'DEBUG' if debug else 'RELEASE'
    release = 'WhateverGreen-{}-{}.zip'.format(version, release_type)
    repo = 'https://github.com/acidanthera/WhateverGreen/releases'
    file = '{}/download/{}/{}'.format(repo, version, release)

    print_bold('* WhateverGreen {}'.format(version))
    extract_files(file, directory)
    for i in ['WhateverGreen.kext.dSYM', 'WhateverName.app']:
        rmtree('{}/{}'.format(directory, i))
    remove('{}/{}'.format(directory, 'SSDT-PNLF.dsl'))


def print_bold(string):
    """ Prints bold text. """
    print('\033[1m{}\033[0m'.format(string))


def root_directory(directory='Volumes/EFI'):
    """ Defines the default root directory. """
    return directory


def run_post_install_tasks(directory):
    """ Runs miscellaneous post install tasks. """
    print_bold('* Miscellaneous')
    print('  - fixing file permissions...'),
    for root, directories, files in walk(directory):
        for i in directories:
            chmod(path.join(root, i), 0o755)
        for j in files:
            if j == '.DS_Store':
                remove(path.join(root, j))
            chmod(path.join(root, j), 0o644)
    print('OK')


if __name__ == '__main__':
    main(root_directory())
