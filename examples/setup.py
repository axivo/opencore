#!/usr/bin/env python

from opencore.build import OpenCoreBuild


if __name__ == '__main__':
    build = OpenCoreBuild('Volumes/EFI')
    build.kexts = [
        {
            'project': 'Lilu',
            'repo': 'acidanthera',
            'version': '1.5.6'
        },
        {
            'project': 'NightShiftEnabler',
            'repo': 'cdf',
            'version': '1.1.1'
        },
        {
            'project': 'WhateverGreen',
            'repo': 'acidanthera',
            'version': '1.5.4'
        }
    ]
    build.patches = [
        {
            'Base': '_early_random',
            'Comment': 'SurPlus 1',
            'Find': build.unhexlify('00 74 23 48 8B'),
            'Identifier': 'kernel',
            'Limit': 800,
            'MinKernel': '20.4.0',
            'Replace': build.unhexlify('00 EB 23 48 8B')
        },
        {
            'Base': '_register_and_init_prng',
            'Comment': 'SurPlus 2',
            'Find': build.unhexlify('BA 48 01 00 00 31 F6'),
            'Identifier': 'kernel',
            'Limit': 256,
            'MinKernel': '20.4.0',
            'Replace': build.unhexlify('BA 48 01 00 00 EB 05')
        }
    ]
    build.write_tree()

    settings = {
        'DeviceProperties': {
            'Add': {
                'PciRoot(0x0)/Pci(0x3,0x0)/Pci(0x0,0x0)': {
                    'rebuild-device-tree': 0,
                    'unfairgva': 1
                },
                'PciRoot(0x0)/Pci(0x7,0x0)/Pci(0x0,0x0)/Pci(0x0,0x0)/Pci(0x0,0x0)': {
                    'built-in': build.unhexlify('00')
                },
                'PciRoot(0x0)/Pci(0x7,0x0)/Pci(0x0,0x0)/Pci(0x8,0x0)/Pci(0x0,0x0)': {
                    'built-in': build.unhexlify('00')
                }
            }
        },
        'Kernel': {
            'Quirks': {
                'DisableLinkeditJettison': True,
                'SetApfsTrimTimeout': 9999999
            }
        },
        'Misc': {
            'Boot': {
                'HideAuxiliary': True,
                'LauncherOption': 'Full',
                'PollAppleHotKeys': True,
                'PickerMode': 'External',
                'PickerVariant': 'Default',
                'ShowPicker': True
            },
            'Security': {
                'AllowSetDefault': True,
                'BlacklistAppleUpdate': True,
                'ExposeSensitiveData': 3,
                'ScanPolicy': 0,
                'Vault': 'Optional'
            }
        },
        'PlatformInfo': {
            'PlatformNVRAM': {
                'FirmwareFeatures': build.unhexlify('03 54 0C C0 08 00 00 00'),
                'FirmwareFeaturesMask': build.unhexlify('3F FF 1F FF 08 00 00 00')
            },
            'SMBIOS': {
                'BoardProduct': 'Mac-27AD2F918AE68F61'
            },
            'UpdateNVRAM': True,
            'UpdateSMBIOS': True
        },
        'UEFI': {
            'AppleInput': {
                'AppleEvent': 'Builtin'
            },
            'ConnectDrivers': True,
            'Drivers': [
                {
                    'Arguments': '',
                    'Comment': '',
                    'Enabled': True,
                    'Path': 'OpenCanopy.efi'
                },
                {
                    'Arguments': '',
                    'Comment': '',
                    'Enabled': True,
                    'Path': 'OpenRuntime.efi'
                }
            ],
            'Output': {
                'ProvideConsoleGop': True,
                'Resolution': 'Max'
            },
            'ProtocolOverrides': {
                'AppleUserInterfaceTheme': True
            },
            'Quirks': {
                'RequestBootVarRouting': True
            }
        }
    }
    build.write_plist(settings)
    build.run_misc_tasks()
