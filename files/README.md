# Component Files

The following file references are used:

- [AppleMCEReporterDisabler](../../../../../acidanthera/bugtracker/issues/424#issuecomment-535624313)
- [ASPP-Override](../../../../../dortania/OpenCore-Legacy-Patcher/tree/main/payloads/Kexts/Misc) (required for macOS Monterey 12.3+)
- [NoAVXFSCompressionTypeZlib](../../../../../dortania/OpenCore-Legacy-Patcher/tree/main/payloads/Kexts/Misc) (recommended for macOS Monterey 12.4+)
- [OcBinaryData](../../../../../acidanthera/OcBinaryData)

Original `AppleMCEReporterDisabler` kext is zipped with the following command:

```sh
~$ zip -rX AppleMCEReporterDisabler-1.0.0-RELEASE.zip AppleMCEReporterDisabler.kext
```

Original `ASPP-Override` kext is zipped with the following command:

```sh
~$ zip -rX ASPP-Override-1.0.1-RELEASE.zip ASPP-Override.kext
```

Original `NoAVXFSCompressionTypeZlib` kext is zipped with the following command:

```sh
~$ zip -rX NoAVXFSCompressionTypeZlib-12.3.1-RELEASE.zip NoAVXFSCompressionTypeZlib.kext
```

OcBinaryData files are automatically refreshed, when `install_opencore()` function is executed. The commands listed below are detailed for general learning purpose only, they are automatically executed as part of the `OpenCoreBuild` class.

To import a Git repo as submodule into your repo, run the OcBinaryData import:

```sh
~$ git submodule add https://github.com/acidanthera/OcBinaryData.git files/OcBinaryData
```

To manually update the OcBinaryData submodule files to latest commit, run:

```sh
~$ git submodule update --init --remote --merge
```
