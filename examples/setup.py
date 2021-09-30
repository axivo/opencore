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
            'project': 'FeatureUnlock',
            'repo': 'acidanthera',
            'version': '1.0.3'
        },
        {
            'project': 'WhateverGreen',
            'repo': 'acidanthera',
            'version': '1.5.3'
        }
    ]
    build.patches = [
        {
            'Arch': 'x86_64',
            'Base': '_early_random',
            'Comment': '',
            'Count': 1,
            'Enabled': True,
            'Find': build.unhexlify('00 74 23 48 8B'),
            'Identifier': 'kernel',
            'Limit': 800,
            'Mask': build.unhexlify(''),
            'MaxKernel': '',
            'MinKernel': '20.4.0',
            'Replace': build.unhexlify('00 EB 23 48 8B'),
            'ReplaceMask': build.unhexlify(''),
            'Skip': 0
        },
        {
            'Arch': 'x86_64',
            'Base': '_register_and_init_prng',
            'Comment': '',
            'Count': 1,
            'Enabled': True,
            'Find': build.unhexlify('BA 48 01 00 00 31 F6'),
            'Identifier': 'kernel',
            'Limit': 256,
            'Mask': build.unhexlify(''),
            'MaxKernel': '',
            'MinKernel': '20.4.0',
            'Replace': build.unhexlify('BA 48 01 00 00 EB 05'),
            'ReplaceMask': build.unhexlify(''),
            'Skip': 0
        }
    ]
    build.write_tree()

    settings = {
        'DeviceProperties': {
            'Add': {
                'PciRoot(0x0)/Pci(0x3,0x0)/Pci(0x0,0x0)': {
                    'agdpmod': build.unhexlify('70 69 6B 65 72 61 00'),
                    'rebuild-device-tree': build.unhexlify('00'),
                    'shikigva': build.unhexlify('50'),
                    'unfairgva': build.unhexlify('01 00 00 00')
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
            'Add': build.configure_kexts([i['project'] for i in build.kexts]),
            'Patch': build.configure_patches(build.patches),
            'Quirks': {
                'DisableLinkeditJettison': True,
                'SetApfsTrimTimeout': 9999999
            },
            'Scheme': {
                'KernelArch': 'x86_64'
            }
        },
        'Misc': {
            'Boot': {
                'ConsoleAttributes': 15,
                'HideAuxiliary': True,
                'PollAppleHotKeys': True,
                'PickerMode': 'External',
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
        'NVRAM': {
            'Add': {
                '4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14': {
                    'DefaultBackgroundColor': build.unhexlify('00 00 00 00'),
                    'UIScale': build.unhexlify('01')
                }
            },
            'Delete': {
                '4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14': [
                    'DefaultBackgroundColor',
                    'UIScale'
                ]
            }
        },
        'PlatformInfo': {
            'SMBIOS': {
                'BIOSVersion': '9999.0.0.0.0',
                'BoardProduct': 'Mac-7BA5B2D9E42DDD94'
            },
            'UpdateSMBIOS': True
        },
        'UEFI': {
            'AppleInput': {
                'AppleEvent': 'Builtin'
            },
            'ConnectDrivers': True,
            'Drivers': [
                {
                    'Path': 'OpenCanopy.efi',
                    'Enabled': True,
                    'Arguments': ''
                },
                {
                    'Path': 'OpenRuntime.efi',
                    'Enabled': True,
                    'Arguments': ''
                }
            ],
            'Output': {
                'ProvideConsoleGop': True,
                'Resolution': 'Max'
            },
            'ProtocolOverrides': {
                'AppleBootPolicy': True,
                'AppleUserInterfaceTheme': True
            },
            'Quirks': {
                'RequestBootVarRouting': True
            }
        }
    }
    build.write_plist(settings)
    build.run_misc_tasks()
