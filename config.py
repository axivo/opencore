#!/usr/bin/env python

from binascii import Error, unhexlify
from multiprocessing import cpu_count
from os import makedirs, path
from plistlib import Data, writePlist


def main(directory):
    config = set_configuration()
    writePlist(config, '{}/config.plist'.format(directory))


def set_configuration():
    """ Sets the OpenCore configuration file format """
    config = {}

    """ Discover and configure computer hardware """
    config['ACPI'] = {
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

    """ Apply different kinds of UEFI modifications on Apple bootloader """
    config['Booter'] = {
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
            'ProvideMaxSlide': 0,
            'RebuildAppleMemoryMap': False,
            'SetupVirtualMap': False,
            'SignalAppleOS': False,
            'SyncRuntimePermissions': False
        }
    }

    """ Device properties are part of the IODeviceTree plane """
    config['DeviceProperties'] = {
        'Add': {
            'PciRoot(0x0)/Pci(0x3,0x0)/Pci(0x0,0x0)': {
                'agdpmod': unhexlify_data('70 69 6B 65 72 61 00'),
                'rebuild-device-tree': unhexlify_data('00'),
                'shikigva': unhexlify_data('50')
            },
            'PciRoot(0x0)/Pci(0x7,0x0)/Pci(0x0,0x0)/Pci(0x0,0x0)/Pci(0x0,0x0)': {
                'built-in': unhexlify_data('00')
            },
            'PciRoot(0x0)/Pci(0x7,0x0)/Pci(0x0,0x0)/Pci(0x8,0x0)/Pci(0x0,0x0)': {
                'built-in': unhexlify_data('00')
            }
        },
        'Delete': {}
    }

    """ Apply different kinds of kernelspace modifications on Apple Kernel """
    kernel_kexts = []
    kexts = [
        'Lilu',
        'NightShiftEnabler',
        'WhateverGreen'
    ]
    if cpu_count > 15:
        kexts.insert(0, 'AppleMCEReporterDisabler')
    for i in kexts:
        kext = {
            'Arch': 'x86_64',
            'BundlePath': '{}.kext'.format(i),
            'Comment': '',
            'Enabled': True,
            'ExecutablePath': 'Contents/MacOS/{}'.format(i),
            'MaxKernel': '',
            'MinKernel': '',
            'PlistPath': 'Contents/Info.plist'
        }
        if i == 'AppleMCEReporterDisabler':
            kext['ExecutablePath'] = ''
        kernel_kexts.append(dict(kext))

    config['Kernel'] = {
        'Add': kernel_kexts,
        'Block': [],
        'Emulate': {
            'Cpuid1Data': unhexlify_data('00 00 00 00 00 00 00 00 00 00 00 80 00 00 00 00'),
            'Cpuid1Mask': unhexlify_data('00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'),
            'DummyPowerManagement': False,
            'MaxKernel': '',
            'MinKernel': ''
        },
        'Force': [],
        'Patch': [],
        'Quirks': {
            'AppleCpuPmCfgLock': False,
            'AppleXcpmCfgLock': False,
            'AppleXcpmExtraMsrs': False,
            'AppleXcpmForceBoost': False,
            'CustomSMBIOSGuid': False,
            'DisableIoMapper': False,
            'DisableLinkeditJettison': False,
            'DisableRtcChecksum': False,
            'ExtendBTFeatureFlags': False,
            'ExternalDiskIcons': False,
            'ForceSecureBootScheme': False,
            'IncreasePciBarSize': False,
            'LapicKernelPanic': False,
            'LegacyCommpage': False,
            'PanicNoKextDump': False,
            'PowerTimeoutKernelPanic': False,
            'ThirdPartyDrives': False,
            'XhciPortLimit': False
        },
        'Scheme': {
            'FuzzyMatch': False,
            'KernelArch': 'x86_64',
            'KernelCache': 'Auto'
        }
    }

    """ Miscellaneous configuration affecting OpenCore loading behaviour """
    config['Misc'] = {
        'BlessOverride': [],
        'Boot': {
            'ConsoleAttributes': 0,
            'HibernateMode': 'None',
            'HideAuxiliary': True,
            'PickerAttributes': 0,
            'PickerAudioAssist': False,
            'PickerMode': 'External',
            'PollAppleHotKeys': True,
            'ShowPicker': True,
            'TakeoffDelay': 0,
            'Timeout': 10
        },
        'Debug': {
            'AppleDebug': False,
            'ApplePanic': False,
            'DisableWatchDog': False,
            'DisplayDelay': 0,
            'DisplayLevel': 0,
            'SerialInit': False,
            'SysReport': False,
            'Target': 0
        },
        'Entries': [],
        'Security': {
            'AllowNvramReset': False,
            'AllowSetDefault': False,
            'ApECID': 0,
            'AuthRestart': False,
            'BootProtect': 'None',
            'DmgLoading': 'Signed',
            'EnablePassword': False,
            'ExposeSensitiveData': 2,
            'HaltLevel': 2147483648,
            'PasswordHash': unhexlify_data(''),
            'PasswordSalt': unhexlify_data(''),
            'ScanPolicy': 0,
            'SecureBootModel': 'Disabled',
            'Vault': 'Optional'
        },
        'Tools': []
    }

    """ Set volatile UEFI variables """
    config['NVRAM'] = {
        'Add': {
            '4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14': {
                'DefaultBackgroundColor': unhexlify_data('00 00 00 00'),
                'UIScale': unhexlify_data('01')
            },
            '7C436110-AB2A-4BBB-A880-FE41995C9F82': {
                'run-efi-updater': 'No'
            }
        },
        'Delete': {
            '4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14': [
                'DefaultBackgroundColor',
                'UIScale',
            ],
            '7C436110-AB2A-4BBB-A880-FE41995C9F82': [
                'run-efi-updater'
            ]
        },
        'LegacyEnable': False,
        'LegacyOverwrite': False,
        'LegacySchema': {},
        'WriteFlash': False
    }

    """ Identification fields compatible with macOS services """
    config['PlatformInfo'] = {
        'Automatic': False,
        'CustomMemory': False,
        'DataHub': {},
        'Generic': {},
        'Memory': {},
        'PlatformNVRAM': {},
        'SMBIOS': {
            'BoardProduct': 'Mac-7BA5B2D9E42DDD94',
            'FirmwareFeatures': unhexlify_data('03 54 0C E0'),
            'FirmwareFeaturesMask': unhexlify_data('3F FF 1F FF')
        },
        'UpdateDataHub': False,
        'UpdateNVRAM': False,
        'UpdateSMBIOS': True,
        'UpdateSMBIOSMode': 'Create'
    }

    """ Allows to load additional UEFI modules and/or apply tweaks to onboard firmware """
    config['UEFI'] = {
        'APFS': {
            'EnableJumpstart': False,
            'GlobalConnect': False,
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
            'ExFatDxeLegacy.efi',
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
            'ForceResolution': False,
            'IgnoreTextInGraphics': False,
            'ProvideConsoleGop': True,
            'ReconnectOnResChange': False,
            'ReplaceTabWithSpace': False,
            'Resolution': 'Max',
            'SanitiseClearScreen': False,
            'TextRenderer': 'BuiltinGraphics',
            'UgaPassThrough': False
        },
        'ProtocolOverrides': {
            'AppleAudio': False,
            'AppleBootPolicy': True,
            'AppleDebugLog': False,
            'AppleEvent': False,
            'AppleFramebufferInfo': False,
            'AppleImageConversion': False,
            'AppleImg4Verification': False,
            'AppleKeyMap': False,
            'AppleRtcRam': False,
            'AppleSecureBoot': False,
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

    return config


def root_directory(directory='Volumes/EFI'):
    """ Defines the default root directory. """
    return directory


def unhexlify_data(string):
    """ Transforms the binary data represented by the hexadecimal string. """
    try:
        result = unhexlify(''.join(string.split()))
    except Error:
        raise

    return Data(result)


if __name__ == '__main__':
    directory = '{}/EFI/OC'.format(root_directory())
    if not path.isdir(directory):
        makedirs(directory)
    main(directory)
