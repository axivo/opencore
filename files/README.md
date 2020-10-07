# Component Files

The following file references are used:

- [AppleMCEReporterDisabler.kext](https://github.com/acidanthera/bugtracker/issues/424#issuecomment-535624313)
- [OcBinaryData](https://github.com/acidanthera/OcBinaryData)

OcBinaryData files are automatically refreshed, when `tree.py` command is executed. The commands listed below are listed for general learning purpose only.

To import a Git repo as submodule into your repo, run the OcBinaryData import as example:

```sh
~$ git submodule add https://github.com/acidanthera/OcBinaryData.git files/OcBinaryData
```

To manually update the OcBinaryData submodule files to latest commit, run:

```sh
~$ git submodule update --init --remote --merge
```
