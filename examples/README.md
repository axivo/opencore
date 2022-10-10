# Usage Examples

The setup file used in this example implements the following customizations:

- OpenCanopy implementation on a black boot screen
- Pulse RX580 GPU hardware acceleration support, through Mac Pro hybridization (system specific device path)
- NVMe external disks displayed as internal disks (system specific device path)
- Night Shift enabled with `FeatureUnlock` Lilu plugin

## Quick Setting Changes

For various setting changes, consult the OpenCore [documentation](../../../../../acidanthera/OpenCorePkg/tree/master/Docs) and the [wiki](../../../wiki).

If you want to enable the mouse functionality into OpenCanopy, add the `PickerAttributes` key into configuration and set its value to `16` (defaults to failsafe `0` value):

```python
        'Misc': {
            'Boot': {
                'PollAppleHotKeys': True,
                'PickerAttributes': 16
            }
```

If you want to increase the OpenCanopy piker timeout, add the `Timeout` key into configuration and set its value to `15` (defaults to failsafe `5` value):

```python
        'Misc': {
            'Boot': {
                'ShowPicker': True,
                'Timeout': 15
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
