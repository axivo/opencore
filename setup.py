#!/usr/bin/env python

from opencore.build import OpenCoreBuild


if __name__ == '__main__':
    kexts = []
    build = OpenCoreBuild('Volumes/EFI', kexts)
    build.write_tree()

    settings = {}
    build.write_plist(settings)
    build.run_misc_tasks()
