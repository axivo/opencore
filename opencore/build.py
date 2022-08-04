#!/usr/bin/env python3

from binascii import Error, unhexlify
from collections import Mapping
from distutils.version import LooseVersion
from glob import glob
from io import BytesIO
from os import chmod, listdir, makedirs, path, remove, stat, walk
from plistlib import dump, FMT_XML
from shutil import copy2, rmtree
from subprocess import CalledProcessError, check_output
from urllib.request import URLError, urlretrieve
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
        self.kexts = []
        self.patches = []
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
                    'ResetLogoStatus': False,
                    'SyncTableIds': False
                }
            },
            'Booter': {
                'MmioWhitelist': [],
                'Patch': [],
                'Quirks': {
                    'AllowRelocationBlock': False,
                    'AvoidRuntimeDefrag': False,
                    'DevirtualiseMmio': False,
                    'DisableSingleUser': False,
                    'DisableVariableWrite': False,
                    'DiscardHibernateMap': False,
                    'EnableSafeModeSlide': False,
                    'EnableWriteUnprotector': False,
                    'ForceBooterSignature': False,
                    'ForceExitBootServices': False,
                    'ProtectMemoryRegions': False,
                    'ProtectSecureBoot': True,
                    'ProtectUefiServices': False,
                    'ProvideCustomSlide': False,
                    'ProvideMaxSlide': 0,
                    'RebuildAppleMemoryMap': False,
                    'ResizeAppleGpuBars': -1,
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
                'Emulate': {
                    'Cpuid1Data': b'',
                    'Cpuid1Mask': b'',
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
                    'CustomPciSerialDevice': False,
                    'CustomSMBIOSGuid': False,
                    'DisableIoMapper': False,
                    'DisableLinkeditJettison': False,
                    'DisableRtcChecksum': False,
                    'ExtendBTFeatureFlags': False,
                    'ExternalDiskIcons': False,
                    'ForceAquantiaEthernet': False,
                    'ForceSecureBootScheme': False,
                    'IncreasePciBarSize': False,
                    'LapicKernelPanic': False,
                    'LegacyCommpage': False,
                    'PanicNoKextDump': False,
                    'PowerTimeoutKernelPanic': False,
                    'ProvideCurrentCpuInfo': False,
                    'SetApfsTrimTimeout': -1,
                    'ThirdPartyDrives': False,
                    'XhciPortLimit': False
                },
                'Scheme': {
                    'CustomKernel': False,
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
                    'HideAuxiliary': False,
                    'LauncherOption': 'Disabled',
                    'LauncherPath': 'Default',
                    'PickerAttributes': 0,
                    'PickerAudioAssist': False,
                    'PickerMode': 'Builtin',
                    'PickerVariant': 'Auto',
                    'PollAppleHotKeys': False,
                    'ShowPicker': True,
                    'TakeoffDelay': 0,
                    'Timeout': 5
                },
                'Debug': {
                    'AppleDebug': False,
                    'ApplePanic': False,
                    'DisableWatchDog': False,
                    'DisplayDelay': 0,
                    'DisplayLevel': 0,
                    'LogModules': '*',
                    'SysReport': False,
                    'Target': 0
                },
                'Entries': [],
                'Security': {
                    'AllowSetDefault': False,
                    'ApECID': 0,
                    'AuthRestart': False,
                    'BlacklistAppleUpdate': False,
                    'DmgLoading': 'Signed',
                    'EnablePassword': False,
                    'ExposeSensitiveData': 6,
                    'HaltLevel': 2147483648,
                    'PasswordHash': b'',
                    'PasswordSalt': b'',
                    'ScanPolicy': 17760515,
                    'SecureBootModel': 'Default',
                    'Vault': 'Secure'
                },
                'Serial': {
                    'Init': False,
                    'Override': False
                },
                'Tools': []
            },
            'NVRAM': {
                'Add': {},
                'Delete': {},
                'LegacyOverwrite': False,
                'LegacySchema': {},
                'WriteFlash': False
            },
            'PlatformInfo': {
                'Automatic': False,
                'CustomMemory': False,
                'DataHub': {
                    'ARTFrequency': 0,
                    'BoardProduct': '',
                    'BoardRevision': b'',
                    'DevicePathsSupported': 0,
                    'FSBFrequency': 0,
                    'InitialTSC': 0,
                    'PlatformName': '',
                    'SmcBranch': b'',
                    'SmcPlatform': b'',
                    'SmcRevision': b'',
                    'StartupPowerEvents': 0,
                    'SystemProductName': '',
                    'SystemSerialNumber': '',
                    'SystemUUID': ''
                },
                'Generic': {
                    'AdviseFeatures': False,
                    'MaxBIOSVersion': False,
                    'MLB': '',
                    'ProcessorType': 0,
                    'ROM': b'',
                    'SpoofVendor': False,
                    'SystemMemoryStatus': 'Auto',
                    'SystemProductName': '',
                    'SystemSerialNumber': '',
                    'SystemUUID': ''
                },
                'Memory': {
                    'DataWidth': 0,
                    'Devices': [],
                    'ErrorCorrection': 3,
                    'FormFactor': 2,
                    'MaxCapacity': 0,
                    'TotalWidth': 0,
                    'Type': 2,
                    'TypeDetail': 4
                },
                'PlatformNVRAM': {
                    'BID': '',
                    'FirmwareFeatures': b'',
                    'FirmwareFeaturesMask': b'',
                    'MLB': '',
                    'ROM': b'',
                    'SystemSerialNumber': '',
                    'SystemUUID': ''
                },
                'SMBIOS': {
                    'BIOSReleaseDate': '',
                    'BIOSVendor': '',
                    'BIOSVersion': '',
                    'BoardAssetTag': '',
                    'BoardLocationInChassis': '',
                    'BoardManufacturer': '',
                    'BoardProduct': '',
                    'BoardSerialNumber': '',
                    'BoardType': 0,
                    'BoardVersion': '',
                    'ChassisAssetTag': '',
                    'ChassisManufacturer': '',
                    'ChassisSerialNumber': '',
                    'ChassisType': 0,
                    'ChassisVersion': '',
                    'FirmwareFeatures': b'',
                    'FirmwareFeaturesMask': b'',
                    'PlatformFeature': -1,
                    'ProcessorType': 0,
                    'SmcVersion': b'',
                    'SystemFamily': '',
                    'SystemManufacturer': '',
                    'SystemProductName': '',
                    'SystemSKUNumber': '',
                    'SystemSerialNumber': '',
                    'SystemUUID': '',
                    'SystemVersion': ''
                },
                'UpdateDataHub': False,
                'UpdateNVRAM': False,
                'UpdateSMBIOS': False,
                'UpdateSMBIOSMode': 'Create',
                'UseRawUuidEncoding': False
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
                'AppleInput': {
                    'AppleEvent': 'Auto',
                    'CustomDelays': False,
                    'KeyInitialDelay': 50,
                    'KeySubsequentDelay': 5,
                    'GraphicsInputMirroring': False,
                    'PointerPollMask': -1,
                    'PointerPollMax': 0,
                    'PointerPollMin': 0,
                    'PointerSpeedDiv': 1,
                    'PointerSpeedMul': 1
                },
                'Audio': {
                    'AudioCodec': 0,
                    'AudioDevice': '',
                    'AudioOutMask': -1,
                    'AudioSupport': False,
                    'DisconnectHda': False,
                    'MaximumGain': -15,
                    'MinimumAssistGain': -30,
                    'MinimumAudibleGain': -128,
                    'PlayChime': 'Auto',
                    'ResetTrafficClass': False,
                    'SetupDelay': 0
                },
                'ConnectDrivers': False,
                'Drivers': [],
                'Input': {
                    'KeyFiltering': False,
                    'KeyForgetThreshold': 0,
                    'KeySupport': False,
                    'KeySupportMode': 'Auto',
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
                    'GopPassThrough': 'Disabled',
                    'IgnoreTextInGraphics': False,
                    'ProvideConsoleGop': False,
                    'ReconnectGraphicsOnConnect': False,
                    'ReconnectOnResChange': False,
                    'ReplaceTabWithSpace': False,
                    'Resolution': '',
                    'SanitiseClearScreen': False,
                    'UIScale': -1,
                    'TextRenderer': 'BuiltinGraphics',
                    'UgaPassThrough': False
                },
                'ProtocolOverrides': {
                    'AppleAudio': False,
                    'AppleBootPolicy': False,
                    'AppleDebugLog': False,
                    'AppleEg2Info': False,
                    'AppleFramebufferInfo': False,
                    'AppleImageConversion': False,
                    'AppleImg4Verification': False,
                    'AppleKeyMap': False,
                    'AppleRtcRam': False,
                    'AppleSecureBoot': False,
                    'AppleSmcIo': False,
                    'AppleUserInterfaceTheme': False,
                    'DataHub': False,
                    'DeviceProperties': False,
                    'FirmwareVolume': False,
                    'HashServices': False,
                    'OSInfo': False,
                    'UnicodeCollation': False
                },
                'Quirks': {
                    'ActivateHpetSupport': False,
                    'EnableVectorAcceleration': False,
                    'EnableVmx': False,
                    'DisableSecurityPolicy': False,
                    'ExitBootServicesDelay': 0,
                    'ForceOcWriteFlash': False,
                    'ForgeUefiSupport': False,
                    'IgnoreInvalidFlexRatio': False,
                    'ReleaseUsbOwnership': False,
                    'ReloadOptionRoms': False,
                    'RequestBootVarRouting': False,
                    'ResizeGpuBars': -1,
                    'TscSyncTimeout': 0,
                    'UnblockFsConnect': False
                },
                'ReservedMemory': []
            }
        }
        self.version = '0.8.3'


    def configure_kexts(self, kexts=[]):
        """
        Inserts kexts into kernel 'Add' data settings.

        :param kexts: List of kext properties to be applied
        :return: List of dictionaries
        """
        result = []
        if kexts:
            for i in kexts:
                properties = {
                    'Arch': 'x86_64',
                    'BundlePath': '{0}.kext'.format(i['project']),
                    'Comment': '',
                    'Enabled': True,
                    'ExecutablePath': 'Contents/MacOS/{0}'.format(i['project']),
                    'MaxKernel': '',
                    'MinKernel': '',
                    'PlistPath': 'Contents/Info.plist'
                }
                if 'properties' in i:
                    for key, value in i['properties'].items():
                        properties[key] = value
                result.append(properties)

        return result


    def configure_patches(self, patches=[]):
        """
        Inserts patches into kernel 'Patch' data settings.

        :param patches: List of patch properties to be applied
        :return: List of dictionaries
        """
        result = []
        if patches:
            for i in patches:
                properties = {
                    'Arch': 'x86_64',
                    'Base': '',
                    'Comment': '',
                    'Count': 1,
                    'Enabled': True,
                    'Find': b'',
                    'Identifier': '',
                    'Limit': 0,
                    'Mask': b'',
                    'MaxKernel': '',
                    'MinKernel': '',
                    'Replace': b'',
                    'ReplaceMask': b'',
                    'Skip': 0
                }
                for key, value in i.items():
                    properties[key] = value
                result.append(properties)

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
        if not local:
            try:
                print('  - downloading component...', end=' ')
                file, _ = urlretrieve(file)
            except URLError:
                raise
            else:
                print('OK')

        print('  - building files structure...', end=' '),
        with ZipFile(file, 'r') as zip:
            zip.extractall(directory)
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
        directory = '{0}/EFI/OC/Kexts'.format(self.directory)
        release_type = 'DEBUG' if debug else 'RELEASE'
        release = '{0}-{1}-{2}.zip'.format(project, version, release_type)
        url = 'https://github.com/{0}/{1}/releases'.format(repo, project)
        file = 'files/{0}'.format(release)
        local = True
        if not path.isfile(file):
            file = '{0}/download/{1}/{2}'.format(url, version, release)
            local = False

        self.print_bold('* {0} {1}'.format(project, version))
        self.extract_files(file, directory, local)
        for i in ['app', 'dsl', 'dSYM']:
            try:
                files = glob('{0}/*.{1}'.format(directory, i))
            except OSError:
                raise
            else:
                for j in files:
                    remove(j) if i == 'dsl' else rmtree(j)


    def install_opencore(self, version, debug=False):
        """
        Builds the OpenCore files structure.

        :param version: Project version
        :param debug: Install DEBUG release
        :return: Nothing
        """
        release_type = 'DEBUG' if debug else 'RELEASE'
        release = 'OpenCore-{0}-{1}.zip'.format(version, release_type)
        url = 'https://github.com/acidanthera/OpenCorePkg/releases'
        file = 'files/{0}'.format(release)
        local = True
        if not path.isfile(file):
            file = '{0}/download/{1}/{2}'.format(url, version, release)
            local = False

        self.print_bold('* OpenCore {0}'.format(version))
        if path.isdir(self.directory):
            print('  - cleaning directory...', end=' ')
            rmtree(self.directory)
            print('OK')
        self.extract_files(file, self.directory, local)
        print('  - cleaning directory...', end=' ')
        source = '{0}/X64/EFI'.format(self.directory)
        destination = '{0}/EFI'.format(self.directory)
        self.copy_tree(source, destination)
        copy2('{0}/Utilities//ocvalidate/ocvalidate'.format(self.directory), './')
        chmod('./ocvalidate', 0o755)
        for i in ['Docs', 'IA32', 'Utilities', 'X64']:
            rmtree('{0}/{1}'.format(self.directory, i))
        print('OK')

        print('  - copying OcBinaryData files...', end=' ')
        try:
            check_output(['git', 'submodule', 'update', '--init', '--remote', '--merge'], encoding='UTF-8')
        except CalledProcessError as e:
            print(e.output)
        source = 'files/OcBinaryData'
        destination = '{0}/EFI/OC'.format(self.directory)
        self.copy_tree('{0}/Drivers'.format(source), '{0}/Drivers'.format(destination))
        self.copy_tree('{0}/Resources'.format(source), '{0}/Resources'.format(destination))
        print('OK')


    def print_bold(self, string):
        """
        Prints bold text.

        :param string: String to print in bold
        :return: Nothing
        """
        print('\033[1m{0}\033[0m'.format(string))


    def run_misc_tasks(self):
        """
        Runs miscellaneous post install tasks.

        :return: Nothing
        """
        self.print_bold('* Miscellaneous Tasks')
        print('  - fixing file permissions...', end=' ')
        for root, directories, files in walk(self.directory):
            for i in directories:
                chmod(path.join(root, i), 0o755)
            for j in files:
                if j == '.DS_Store':
                    remove(path.join(root, j))
                chmod(path.join(root, j), 0o644)
        try:
            check_output(['xattr', '-rc', self.directory], encoding='UTF-8')
        except CalledProcessError as e:
            print(e.output)
        print('OK')
        file = '{0}/EFI/OC/config.plist'.format(self.directory)
        if path.isfile(file) and LooseVersion(self.version) > LooseVersion('0.6.5'):
            print('  - validating config.plist...')
            try:
                print(check_output(['./ocvalidate', file], encoding='UTF-8'))
            except CalledProcessError as e:
                print(e.output)


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

        return bytes(result)


    def update_settings(self, result, settings):
        """
        Updates existing settings with new settings.

        :param result: Default settings
        :param settings: Settings to update
        :return: Dictionary of settings
        """
        for key, value in iter(settings.items()):
            if key == 'Kernel':
                kexts = self.configure_kexts(self.kexts)
                settings[key].update({'Add': kexts})
                patches = self.configure_patches(self.patches)
                settings[key].update({'Patch': patches})
            if isinstance(value, Mapping):
                result[key] = self.update_settings(result.get(key, {}), value)
            else:
                result[key] = value

        return result


    def write_plist(self, settings):
        """
        Generates the OpenCore configuration file.

        :param settings: Settings to be updated
        :return: Nothing
        """
        try:
            self.update_settings(self.settings, settings)
        except KeyError:
            raise
        else:
            self.print_bold('* OpenCore Configuration')
            print('  - generating config.plist...', end=' ')
            directory = '{0}/EFI/OC'.format(self.directory)
            file = '{0}/config.plist'.format(directory)
            if not path.isdir(directory):
                makedirs(directory)
            with open(file, 'wb') as plist:
                dump(self.settings, plist, fmt=FMT_XML, sort_keys=True)
            try:
                check_output(['plutil', '-convert', 'xml1', file], encoding='UTF-8')
            except CalledProcessError as e:
                print(e.output)
            print('OK')


    def write_tree(self, debug=False):
        """
        Generates the OpenCore files structure.

        :param debug: Install DEBUG release
        :return: Nothing
        """
        self.install_opencore(self.version, debug)
        cpu_count = check_output(['sysctl', '-n', 'hw.ncpu'], encoding='UTF-8')
        if int(cpu_count) > 15:
            kext = {
                'project': 'AppleMCEReporterDisabler',
                'properties': {
                    'ExecutablePath': ''
                },
                'repo': 'acidanthera',
                'version': '1.0.0'
            }
            self.kexts.insert(0, kext)
        for i in self.kexts:
            self.install_kext(i['repo'], i['project'], i['version'], debug)
