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
            'ProvideMaxSlide': 0,
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

    Kernel = {
        'Add': kernel_kexts,
        'Block': [],
        'Emulate': {
            'Cpuid1Data': Data('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00'),
            'Cpuid1Mask': Data('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
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
            'PasswordHash': Data(''),
            'PasswordSalt': Data(''),
            'ScanPolicy': 0,
            'SecureBootModel': 'Disabled',
            'Vault': 'Optional'
        },
        'Tools': []
    }

    NVRAM = {
        'Add': {
            '4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14': {
                'DefaultBackgroundColor': Data('\x00\x00\x00\x00'),
                'UIScale': Data('\x01')
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

    PlatformInfo = {
        'Automatic': False,
        'CustomMemory': False,
        'DataHub': {},
        'Generic': {},
        'Memory': {},
        'PlatformNVRAM': {},
        'SMBIOS': {
            'BoardProduct': 'Mac-7BA5B2D9E42DDD94',
            'FirmwareFeatures': Data('\x03\x54\x0C\xE0'),
            'FirmwareFeaturesMask': Data('\x3F\xFF\x1F\xFF')
        },
        'UpdateDataHub': False,
        'UpdateNVRAM': False,
        'UpdateSMBIOS': True,
        'UpdateSMBIOSMode': 'Create'
    }

    UEFI = {
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
