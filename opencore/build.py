#!/usr/bin/env python

from binascii import Error, unhexlify
from collections import Mapping
from glob import glob
from io import BytesIO
from multiprocessing import cpu_count
from os import chmod, listdir, makedirs, path, remove, stat, walk
from plistlib import Data, writePlist
from shutil import copy2, rmtree
from subprocess import check_output
from urllib2 import URLError, urlopen
from zipfile import BadZipfile, ZipFile


class OpenCoreBuild:
    """
    OpenCoreBuild generates the EFI tree and config.plist file.
    """
    def __init__(self, directory):
        """
        Constructs a new 'OpenCoreBuild' object.

        :param directory: Path of the build directory
        :return: Nothing
        """
        self.directory = directory
        self.settings = {
            'ACPI': {
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
            },
            'Booter': {
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
            },
            'DeviceProperties': {
                'Add': {},
                'Delete': {}
            },
            'Kernel': {
                'Add': [],
                'Block': [],
                'Emulate': {},
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
                    'KernelArch': 'Auto',
                    'KernelCache': 'Auto'
                }
            },
            'Misc': {
                'BlessOverride': [],
                'Boot': {
                    'ConsoleAttributes': 0,
                    'HibernateMode': 'None',
                    'HideAuxiliary': True,
                    'PickerAttributes': 0,
                    'PickerAudioAssist': False,
                    'PickerMode': 'Builtin',
                    'PollAppleHotKeys': True,
                    'ShowPicker': False,
                    'TakeoffDelay': 0,
                    'Timeout': 0
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
            },
            'NVRAM': {
                'Add': {},
                'Delete': {},
                'LegacyEnable': False,
                'LegacyOverwrite': False,
                'LegacySchema': {},
                'WriteFlash': False
            },
            'PlatformInfo': {
                'Automatic': False,
                'CustomMemory': False,
                'DataHub': {},
                'Generic': {},
                'Memory': {},
                'PlatformNVRAM': {},
                'SMBIOS': {},
                'UpdateDataHub': False,
                'UpdateNVRAM': False,
                'UpdateSMBIOS': False,
                'UpdateSMBIOSMode': 'Create'
            },
            'UEFI': {
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
        }
        self.version = '0.6.4'


    def configure_kexts(self, kexts=[]):
        """
        Configures the kext settings.

        :param kexts: List of kexts to be configured
        :return: Kext dictionaries
        """
        result = []
        if cpu_count > 15:
            kexts.append('AppleMCEReporterDisabler')
        kexts.sort()
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
            result.append(dict(kext))

        return result


    def copy_tree(self, source, destination):
        """
        Copies directories and files recursively.

        :param source: Source path
        :param destination: Destination path
        :return: Nothing
        """
        if not path.exists(destination):
            makedirs(destination)
        for item in listdir(source):
            s = path.join(source, item)
            d = path.join(destination, item)
            if path.isdir(s):
                self.copy_tree(s, d)
            else:
                if not path.exists(d) or stat(s).st_mtime - stat(d).st_mtime > 1:
                    copy2(s, d)


    def extract_files(self, file, directory, local=False):
        """
        Extracts the contents of a zip file directly from Internet.

        :param file: File name
        :param directory: Directory name where file will be extracted
        :param local: Local file will be extracted
        :return: Nothing
        """
        if local:
            try:
                response = open(file)
            except IOError:
                raise
        else:
            try:
                print('  - downloading component...'),
                response = urlopen(file)
            except URLError:
                raise
            else:
                print('OK')

        try:
            print('  - building files structure...'),
            zipfile = ZipFile(BytesIO(response.read()))
        except BadZipfile:
            raise
        else:
            for i in zipfile.namelist():
                zipfile.extract(i, directory)
            zipfile.close()
            print('OK')


    def install_kext(self, repo, project, version, debug=False):
        """
        Builds the kext files structure.

        :param repo: Repo name
        :param project: Project name
        :param version: Project version
        :param debug: Install DEBUG release
        :return: Nothing
        """
        directory = '{}/EFI/OC/Kexts'.format(self.directory)
        release_type = 'DEBUG' if debug else 'RELEASE'
        release = '{}-{}-{}.zip'.format(project, version, release_type)
        url = 'https://github.com/{}/{}/releases'.format(repo, project)
        file = 'files/{}'.format(release)
        local = True
        if not path.isfile(file):
            file = '{}/download/{}/{}'.format(url, version, release)
            local = False

        self.print_bold('* {} {}'.format(project, version))
        self.extract_files(file, directory, local)
        for i in ['app', 'dsl', 'dSYM']:
            try:
                files = glob('{}/*.{}'.format(directory, i))
            except OSError:
                raise
            else:
                for j in files:
                    remove(j) if i == 'dsl' else rmtree(j)


    def install_opencore(self, version, debug=False):
        """
        Builds the OpenCore files structure.

        :param version: Project version
        :return: Nothing
        """
        release_type = 'DEBUG' if debug else 'RELEASE'
        release = 'OpenCore-{}-{}.zip'.format(version, release_type)
        url = 'https://github.com/acidanthera/OpenCorePkg/releases'
        file = 'files/{}'.format(release)
        local = True
        if not path.isfile(file):
            file = '{}/download/{}/{}'.format(url, version, release)
            local = False

        self.print_bold('* OpenCore {}'.format(version))
        if path.isdir(self.directory):
            print('  - cleaning directory...'),
            rmtree(self.directory)
            print('OK')
        self.extract_files(file, self.directory, local)
        print('  - cleaning directory...'),
        source = '{}/X64/EFI'.format(self.directory)
        destination = '{}/EFI'.format(self.directory)
        self.copy_tree(source, destination)
        for i in ['Docs', 'IA32', 'Utilities', 'X64']:
            rmtree('{}/{}'.format(self.directory, i))
        print('OK')

        if cpu_count() > 15:
            print('  - installing AppleMCEReporterDisabler...'),
            source = 'files/AppleMCEReporterDisabler.kext'
            destination = '{}/EFI/OC/Kexts/AppleMCEReporterDisabler.kext'.format(self.directory)
            self.copy_tree(source, destination)
            print('OK')

        source = 'files/OcBinaryData'
        destination = '{}/EFI/OC'.format(self.directory)
        print('  - copying OcBinaryData files...'),
        check_output(['git', 'submodule', 'update', '--init', '--remote', '--merge'])
        self.copy_tree('{}/Drivers'.format(source), '{}/Drivers'.format(destination))
        self.copy_tree('{}/Resources'.format(source), '{}/Resources'.format(destination))
        print('OK')


    def print_bold(self, string):
        """
        Prints bold text.

        :param string: String to print in bold
        :return: Nothing
        """
        print('\033[1m{}\033[0m'.format(string))


    def run_misc_tasks(self):
        """
        Runs miscellaneous post install tasks.

        :return: Nothing
        """
        self.print_bold('* Miscellaneous')
        print('  - fixing file permissions...'),
        for root, directories, files in walk(self.directory):
            for i in directories:
                chmod(path.join(root, i), 0o755)
            for j in files:
                if j == '.DS_Store':
                    remove(path.join(root, j))
                chmod(path.join(root, j), 0o644)
        print('OK')


    def unhexlify(self, string):
        """
        Transforms the binary data represented by the hexadecimal string.

        :param string: String to transform
        :return: Base64 data
        """
        try:
            result = unhexlify(''.join(string.split()))
        except Error:
            raise

        return Data(result)


    def update_settings(self, result, settings):
        """
        Updates existing settings with new settings.

        :param result: Default settings
        :param settings: Settings to update
        :return: Dictionary of settings
        """
        for key, value in settings.iteritems():
            if isinstance(value, Mapping):
                result[key] = self.update_settings(result.get(key, {}), value)
            else:
                result[key] = value

        return result


    def write_plist(self, settings):
        """
        Generates the OpenCore configuration file.

        :param settings: Settings to update
        :return: Nothing
        """
        try:
            self.update_settings(self.settings, settings)
        except KeyError:
            raise
        else:
            self.print_bold('* OpenCore Configuration')
            print('  - generating config.plist...'),
            directory = '{}/EFI/OC'.format(self.directory)
            if not path.isdir(directory):
                makedirs(directory)
            writePlist(self.settings, '{}/config.plist'.format(directory))
            print('OK')


    def write_tree(self, kexts):
        """
        Generates the OpenCore files structure.

        :param kexts: List of kexts to be installed
        :return: Nothing
        """
        self.install_opencore(self.version)
        for i in kexts:
            self.install_kext(i['repo'], i['project'], i['version'])
