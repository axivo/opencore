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
        },
        {
            'Base': '_work_interval_port_type_render_server',
            'Comment': 'MonteRand 1',
            'Find': build.unhexlify('0F C7 F1 73 FB 21 F1 39 D1 73 F5 89 C9 48 8B 94 CD D0 FD FF FF'),
            'Identifier': 'kernel',
            'Limit': 3900,
            'MinKernel': '21.2.0',
            'Replace': build.unhexlify('31 C9 90 90 90 21 F1 39 D1 73 F5 89 C9 48 8B 94 CD D0 FD FF FF')
        },
        {
            'Base': '_panic_with_thread_context',
            'Comment': 'MonteRand 2',
            'Find': build.unhexlify('0F C7 F2 73 FB 83 E2 0F 83 FA 07 77 F3 0F B7 34 41'),
            'Identifier': 'kernel',
            'Limit': 10100,
            'MinKernel': '21.2.0',
            'Replace': build.unhexlify('31 D2 90 90 90 83 E2 0F 83 FA 07 77 F3 0F B7 34 41')
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
                'LauncherOption': 'Full',
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
            'PlatformNVRAM': {
                'FirmwareFeatures': build.unhexlify('03 54 0C C0 08 00 00 00'),
                'FirmwareFeaturesMask': build.unhexlify('3F FF 1F FF 08 00 00 00')
            },
            'SMBIOS': {
                'BIOSVersion': '9999.0.0.0.0',
                'BoardProduct': 'Mac-7BA5B2D9E42DDD94'
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
