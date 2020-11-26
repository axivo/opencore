#!/usr/bin/env python

from opencore.build import OpenCoreBuild


if __name__ == '__main__':
    build = OpenCoreBuild('Volumes/EFI')

    kexts = []

    settings = {}

    build.write_tree(kexts)
    build.write_plist(settings)
    build.run_misc_tasks()
