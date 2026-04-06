<div align="center">
<img src="https://github.com/YBronst/OCLP-Plus/blob/main/docs/images/OC-Patcher.png"  alt="OC-Patcher Logo" width="256" />

# [OCLP-Plus (Tahoe Patch Set)](https://github.com/xtomasnemec/OCLP-Plus/releases)

</div>

### Experimental macOS Tahoe support

## Compatible models:
```
MacBookPro14,1 (14,2 - No T1 support! 14,3 - No T1 and dGPU support!)
MacBook10,1
iMac18,x - 19,x (No Fusion drive support! Upgrade to an SSD!)
```

**Graphics patches for Non-Metal, Legacy Metal and patches for T1 and T2 Macs are not supported, only use this for the 12" MacBook 2017, 13" MacBook Pro 2017 (Function keys) or iMacs introduced in 2017 and 2019 (SSD models or SSD upgraded)**

> [!NOTE]
> Other Macs may be supported (the program doesn't block them and still *probably* creates a working OpenCore config), newer Macs have the T2 chip and they can't boot macOS via OpenCore. Older Macs do not support Metal 3 (so no graphics acceleration). **Your mileage may vary!**
>
> You may also enable untested Root Patches, they probably won't work or they may break your macOS install. **Proceed with caution!**

## Building EFI form Windows

Example build command for building OpenCore for MacBookPro14,1:

```
.\.venv\Scripts\python -c "from oclp_plus.application_entry import main; main()" --build --model MacBookPro14,1
```

## Tested Root Patches:

### Wireless & Continuity Restoration
Restores full functionality for Broadcom-based wireless chipsets found in most 2009 - 2017 Macs (BRCM4360/4350 and BCM943224/94331):

## PCIe webcam
Restores full functionality for PCIe webcams found in MacBooks and iMacs before 2018

### Modern Audio (AppleHDA Restoration)
Restores the `AppleHDA.kext`. Works for all non-T2 Macs that had native audio in Sequoia. Requires the KDK.
*  **Manual Toggle:** A new "Modern Audio" toggle in the Root Patches menu allows you to enable or disable this restoration manually.
*  **KDK Integration:** Automatically handles the necessary Kernel Debug Kit (KDK) requirements for audio driver linking.

### [`Build and run from source`](https://github.com/xtomasnemec/OCLP-Plus/blob/main/SOURCE.md)

### Installation Requirements
**Before Running Post-Install Patches:**
* **KDK is mandatory for some patches:** For macOS 13 through Tahoe (26.x), the Kernel Debug Kit must be installed for drivers like AppleHDA to link correctly. Use the Help > Download KDK button.

**Resource Dependency Notice**
* **Patcher Resources:** This version relies on the [`PatcherSupportPkg`](https://github.com/YBronst/PatcherSupportPkg) for native Tahoe binaries.

## Credits
*   [`Acidanthera`](https://github.com/Acidanthera) (OpenCorePkg, Lilu, etc.)
*   [`Dortania Team`](https://github.com/dortania) (Original OCLP authors)
*   [`lzhoang2801`](https://github.com/kgp-macPro/OCLP-lzhoang2801) (Original Tahoe patchset)
*   [`CloverHackyColor`](https://github.com/CloverHackyColor) (Hackintosh essentials and beyond)
*   [`YBronst`](https://github.com/YBronst) (Original OCLP-PLUS developer)
*   [`xtomasnemec`](https://github.com/xtomasnemec)
*   *Full list of OCLP contributors can be found in the [`original repository`](https://github.com/dortania/OpenCore-Legacy-Patcher).*

## Disclaimer
This is an **experimental Project** intended for advanced users. **Use at your own risk!**
