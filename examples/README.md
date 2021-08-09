# Usage Examples

The setup file used in this example implements the following customizations:

- OpenCanopy implementation on a black boot screen
- Pulse RX580 GPU hardware acceleration support, through iMac Pro hybridization (system specific device path)
- NVMe external disks displayed as internal disks (system specific device path)
- Night Shift enabled with `FeatureUnlock` Lilu plugin
- Experimental `Latebloom` fix for macOS Big Sur 11.3+ race condition
- Software Updates enabled

## Quick Setting Changes

For various setting changes, consult the OpenCore [documentation](../../../../acidanthera/OpenCorePkg/tree/master/Docs) and the [wiki](../../../wiki).

If you want to enable the mouse functionality into OpenCanopy, add the `PickerAttributes` key into configuration and set its value to `16` (defaults to failsafe `0` value):

```python
        'Misc': {
            'Boot': {
                'ConsoleAttributes': 15,
                'HideAuxiliary': True,
                'PollAppleHotKeys': True,
                'PickerAttributes': 16,
                'PickerMode': 'External',
                'ShowPicker': False
            }
        }
```

If you're using a non-HiDPI display, set the `UIScale` value to `02`:

```python
        'NVRAM': {
            'Add': {
                '4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14': {
                    'DefaultBackgroundColor': build.unhexlify('00 00 00 00'),
                    'UIScale': build.unhexlify('02')
                }
            }
        }
```

If you have a Radeon VII or 5700 XT GPU installed instead of a Pulse RX580, add the `DirectGopRendering` key into configuration and set its value to `True` (defaults to failsafe `False` value):

```python
        'UEFI': {
            'Output': {
                'DirectGopRendering': True,
                'ProvideConsoleGop': True,
                'Resolution': 'Max'
            }
        }
```
