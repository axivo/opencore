#!/usr/bin/env python

from opencore.build import OpenCoreBuild


if __name__ == '__main__':
    build = OpenCoreBuild('Volumes/EFI')
    build.kexts = []
    build.patches = []
    build.write_tree()

    settings = {}
    build.write_plist(settings)
    build.run_misc_tasks()
