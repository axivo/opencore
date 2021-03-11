# Usage Examples

The setup file used in this example implements the following customizations:

- OpenCanopy implementation on a black boot screen
- Pulse RX580 GPU hardware acceleration support, through iMac Pro hybridization (system specific device path)
- NVMe external disks displayed as internal disks (system specific device path)
- Software Updates enabled
- Night Shift enabled

For various setting changes, consult the OpenCore [documentation](../../../../acidanthera/OpenCorePkg/tree/master/Docs) and the [wiki](../../../wiki).

For example, if you have a Radeon VII or 5700 XT GPU installed instead of a Pulse RX580, add the `DirectGopRendering` key into configuration and set its value to `True` (defaults to failsafe `False` value):

```python
        'UEFI': {
            'Output': {
                'DirectGopRendering': True,
                'ProvideConsoleGop': True,
                'Resolution': 'Max'
            }
        }
```
