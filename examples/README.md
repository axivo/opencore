# Usage Examples

The setup file used in this example implements the following customizations:

- OpenCanopy implementation on a black boot screen
- Pulse RX580 GPU hardware acceleration support, through iMacPro hybridization (system specific device path)
- NVMe external disks displayed as internal disks (system specific device path)
- Software Updates enabled (VMM flag set to On with `Cpuid1Mask`)
- Night Shift enabled

For various setting changes, consult the OpenCore [documentation](../../../../acidanthera/OpenCorePkg/tree/master/Docs) and the [wiki](../../../wiki).

For example, if you don't have a Pulse RX580 GPU, add the `DirectGopRendering` key into configuration and set its value to `True` (defaults to failsafe `False` value):

```python
        'UEFI': {
            'Output': {
                'DirectGopRendering': True,
                'ProvideConsoleGop': True,
                'Resolution': 'Max'
            }
        }
```
