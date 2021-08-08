# Component Files

The following file references are used:

- [AppleMCEReporterDisabler](../../../../../acidanthera/bugtracker/issues/424#issuecomment-535624313)
- [Latebloom](https://forums.macrumors.com/threads/2303986) for macOS Big Sur 11.3+
- [OcBinaryData](../../../../../acidanthera/OcBinaryData)

Original AppleMCEReporterDisabler and Latebloom kexts are zipped with the following command:

```sh
~$ zip -rX AppleMCEReporterDisabler-1.0.0-RELEASE.zip AppleMCEReporterDisabler.kext
~$ zip -rX latebloom-<version>-RELEASE.zip latebloom.kext
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
