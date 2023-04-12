#!/usr/bin/env python3

from opencore.build import OpenCoreBuild


if __name__ == '__main__':
    build = OpenCoreBuild('Volumes/EFI')
    build.kexts = [
        {
            'project': 'ASPP-Override',
            'properties': {
                'ExecutablePath': '',
                'MinKernel': '21.4.0'
            },
            'repo': 'dortania',
            'version': '1.0.1'
        },
        {
            'project': 'Lilu',
            'repo': 'acidanthera',
            'version': '1.6.4'
        },
        {
            'project': 'FeatureUnlock',
            'repo': 'acidanthera',
            'version': '1.1.4'
        },
        {
            'project': 'WhateverGreen',
            'repo': 'acidanthera',
            'version': '1.6.4'
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
                'SetApfsTrimTimeout': 0
            }
        },
        'Misc': {
            'Boot': {
                'HideAuxiliary': True,
                'LauncherOption': 'Full',
                'PollAppleHotKeys': True,
                'PickerMode': 'External',
                'PickerVariant': 'Default',
                'ShowPicker': True,
                'Timeout': 15
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
                    'LoadEarly': False,
                    'Path': 'OpenCanopy.efi'
                },
                {
                    'Arguments': '',
                    'Comment': '',
                    'Enabled': True,
                    'LoadEarly': False,
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
