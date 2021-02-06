#!/usr/bin/env python

from opencore.build import OpenCoreBuild


if __name__ == '__main__':
    kexts = [
        {
            'project': 'Lilu',
            'repo': 'acidanthera',
            'version': '1.5.1'
        },
        {
            'project': 'NightShiftEnabler',
            'repo': 'cdf',
            'version': '1.1.0'
        },
        {
            'project': 'WhateverGreen',
            'repo': 'acidanthera',
            'version': '1.4.7'
        }
    ]
    build = OpenCoreBuild('Volumes/EFI', kexts)
    build.write_tree()

    settings = {
        'Booter': {
            'Quirks': {
                'ProtectSecureBoot': True
            }
        },
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
            'Emulate': {
                'Cpuid1Data': build.unhexlify('00 00 00 00 00 00 00 00 00 00 00 80 00 00 00 00'),
                'Cpuid1Mask': build.unhexlify('00 00 00 00 00 00 00 00 00 00 00 80 00 00 00 00')
            },
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
                'ShowPicker': False
            },
            'Security': {
                'BlacklistAppleUpdate': True,
                'ExposeSensitiveData': 3,
                'ScanPolicy': 0,
                'SecureBootModel': 'Disabled',
                'Vault': 'Optional'
            }
        },
        'NVRAM': {
            'Add': {
                '4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14': {
                    'DefaultBackgroundColor': build.unhexlify('00 00 00 00'),
                    'UIScale': build.unhexlify('02')
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
            'ConnectDrivers': True,
            'Drivers': [
                'ExFatDxeLegacy.efi',
                'OpenCanopy.efi',
                'OpenRuntime.efi'
            ],
            'Output': {
                'DirectGopRendering': True,
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
