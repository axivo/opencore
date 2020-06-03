#!/usr/bin/env python

from multiprocessing import cpu_count
from os import makedirs, path
from plistlib import Data, writePlist


def main(directory):
    ACPI = {
        'Add': [],
        'Delete': [],
        'Patch': [],
        'Quirks': {
            'FadtEnableReset': False,
            'NormalizeHeaders': False,
            'RebaseRegions': False,
            'ResetHwSig': False,
            'ResetLogoStatus': False
        }
    }

    Booter = {
        'MmioWhitelist': [],
        'Quirks': {
            'AvoidRuntimeDefrag': False,
            'DevirtualiseMmio': False,
            'DisableSingleUser': False,
            'DisableVariableWrite': False,
            'DiscardHibernateMap': False,
            'EnableSafeModeSlide': False,
            'EnableWriteUnprotector': False,
            'ForceExitBootServices': False,
            'ProtectMemoryRegions': False,
            'ProtectSecureBoot': True,
            'ProtectUefiServices': False,
            'ProvideCustomSlide': False,
            'RebuildAppleMemoryMap': False,
            'SetupVirtualMap': False,
            'SignalAppleOS': False,
            'SyncRuntimePermissions': False
        }
    }

    DeviceProperties = {
        'Add': {
            'PciRoot(0x0)/Pci(0x3,0x0)/Pci(0x0,0x0)': {
                'agdpmod': Data('pikera\0'),
                'rebuild-device-tree': Data('\x00'),
                'shikigva': Data('\x50')
            },
            'PciRoot(0x0)/Pci(0x7,0x0)/Pci(0x0,0x0)/Pci(0x0,0x0)/Pci(0x0,0x0)': {
                'built-in': Data('\x00')
            },
            'PciRoot(0x0)/Pci(0x7,0x0)/Pci(0x0,0x0)/Pci(0x8,0x0)/Pci(0x0,0x0)': {
                'built-in': Data('\x00')
            }
        },
        'Delete': {}
    }

    Kernel = {
        'Add': [
            {
                'BundlePath': 'Lilu.kext',
                'Comment': '',
                'Enabled': True,
                'ExecutablePath': 'Contents/MacOS/Lilu',
                'MaxKernel': '',
                'MinKernel': '',
                'PlistPath': 'Contents/Info.plist'
            },
            {
                'BundlePath': 'NightShiftEnabler.kext',
                'Comment': '',
                'Enabled': True,
                'ExecutablePath': 'Contents/MacOS/NightShiftEnabler',
                'MaxKernel': '',
                'MinKernel': '',
                'PlistPath': 'Contents/Info.plist'
            },
            {
                'BundlePath': 'WhateverGreen.kext',
                'Comment': '',
                'Enabled': True,
                'ExecutablePath': 'Contents/MacOS/WhateverGreen',
                'MaxKernel': '',
                'MinKernel': '',
                'PlistPath': 'Contents/Info.plist'
            }
        ],
        'Block': [],
        'Emulate': {
            'Cpuid1Data': Data('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00'),
            'Cpuid1Mask': Data('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00')
        },
        'Patch': [],
        'Quirks': {
            'AppleCpuPmCfgLock': False,
            'AppleXcpmCfgLock': False,
            'AppleXcpmExtraMsrs': False,
            'AppleXcpmForceBoost': False,
            'CustomSMBIOSGuid': False,
            'DisableIoMapper': False,
            'DisableRtcChecksum': False,
            'DummyPowerManagement': False,
            'ExternalDiskIcons': False,
            'IncreasePciBarSize': False,
            'LapicKernelPanic': False,
            'PanicNoKextDump': False,
            'PowerTimeoutKernelPanic': False,
            'ThirdPartyDrives': False,
            'XhciPortLimit': False
        }
    }
    if cpu_count > 15:
        Kernel['Add'].append(
            {
                'BundlePath': 'AppleMCEReporterDisabler.kext',
                'Comment': '',
                'Enabled': True,
                'ExecutablePath': '',
                'MaxKernel': '',
                'MinKernel': '',
                'PlistPath': 'Contents/Info.plist'
            }
        )

    Misc = {
        'BlessOverride': [],
        'Boot': {
            'ConsoleAttributes': 0,
            'HibernateMode': 'None',
            'HideAuxiliary': True,
            'PickerAttributes': 0,
            'PickerAudioAssist': False,
            'PickerMode': 'External',
            'PollAppleHotKeys': True,
            'ShowPicker': False,
            'TakeoffDelay': 0,
            'Timeout': 10
        },
        'Debug': {
            'AppleDebug': False,
            'ApplePanic': False,
            'DisableWatchDog': False,
            'DisplayDelay': 0,
            'DisplayLevel': 0,
            'SysReport': False,
            'Target': 0
        },
        'Entries': [],
        'Security': {
            'AllowNvramReset': False,
            'AllowSetDefault': False,
            'AuthRestart': False,
            'BlacklistAppleUpdate': False,
            'BootProtect': 'None',
            'ExposeSensitiveData': 2,
            'HaltLevel': 2147483648,
            'ScanPolicy': 0,
            'Vault': 'Optional'
        },
        'Tools': []
    }

    NVRAM = {
        'Add': {
            '4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14': {
                'DefaultBackgroundColor': Data('\x00\x00\x00\x00'),
                'UIScale': Data('\x02')
            }
        },
        'Delete': {
            '4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14': [
                'DefaultBackgroundColor',
                'UIScale',
            ]
        },
        'LegacyEnable': False,
        'LegacyOverwrite': False,
        'LegacySchema': {},
        'WriteFlash': False
    }

    PlatformInfo = {
        'Automatic': False,
        'DataHub': {},
        'Generic': {},
        'PlatformNVRAM': {},
        'SMBIOS': {
            'BoardProduct': 'Mac-7BA5B2D9E42DDD94'
        },
        'UpdateDataHub': False,
        'UpdateNVRAM': False,
        'UpdateSMBIOS': True,
        'UpdateSMBIOSMode': 'Create'
    }

    UEFI = {
        'APFS': {
            'EnableJumpstart': False,
            'HideVerbose': False,
            'JumpstartHotPlug': False,
            'MinDate': 0,
            'MinVersion': 0
        },
        'Audio': {
            'AudioCodec': 0,
            'AudioDevice': '',
            'AudioOut': 0,
            'AudioSupport': False,
            'MinimumVolume': 0,
            'PlayChime': False,
            'VolumeAmplifier': 0
        },
        'ConnectDrivers': True,
        'Drivers': [
            'OpenCanopy.efi',
            'OpenRuntime.efi'
        ],
        'Input': {
            'KeyFiltering': False,
            'KeyForgetThreshold': 0,
            'KeyMergeThreshold': 0,
            'KeySupport': False,
            'KeySupportMode': '',
            'KeySwap': False,
            'PointerSupport': False,
            'PointerSupportMode': '',
            'TimerResolution': 0
        },
        'Output': {
            'ClearScreenOnModeSwitch': False,
            'ConsoleMode': '',
            'DirectGopRendering': False,
            'IgnoreTextInGraphics': False,
            'ProvideConsoleGop': True,
            'ReconnectOnResChange': False,
            'ReplaceTabWithSpace': False,
            'Resolution': 'Max',
            'SanitiseClearScreen': False,
            'TextRenderer': 'BuiltinGraphics'
        },
        'ProtocolOverrides': {
            'AppleAudio': False,
            'AppleBootPolicy': True,
            'AppleDebugLog': False,
            'AppleEvent': False,
            'AppleImageConversion': False,
            'AppleKeyMap': False,
            'AppleRtcRam': False,
            'AppleSmcIo': False,
            'AppleUserInterfaceTheme': True,
            'DataHub': False,
            'DeviceProperties': False,
            'FirmwareVolume': False,
            'HashServices': False,
            'OSInfo': False,
            'UnicodeCollation': False
        },
        'Quirks': {
            'DeduplicateBootOrder': False,
            'ExitBootServicesDelay': 0,
            'IgnoreInvalidFlexRatio': False,
            'ReleaseUsbOwnership': False,
            'RequestBootVarRouting': True,
            'TscSyncTimeout': 0,
            'UnblockFsConnect': False
        },
        'ReservedMemory': []
    }

    plist = {
        'ACPI': ACPI,
        'Booter': Booter,
        'DeviceProperties': DeviceProperties,
        'Kernel': Kernel,
        'Misc': Misc,
        'NVRAM': NVRAM,
        'PlatformInfo': PlatformInfo,
        'UEFI': UEFI
    }
    writePlist(plist, '{}/config.plist'.format(directory))


def root_directory(directory='Volumes/EFI'):
    """ Defines the default root directory. """
    return directory


if __name__ == '__main__':
    directory = '{}/EFI/OC'.format(root_directory())
    if not path.isdir(directory):
        makedirs(directory)
    main(directory)
