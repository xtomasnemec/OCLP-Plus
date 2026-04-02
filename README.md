<div align="center">
<img src="https://github.com/YBronst/OCLP-Plus/blob/main/docs/images/OC-Patcher.png"  alt="OC-Patcher Logo" width="256" />

# [OCLP-Plus (Tahoe Patch Set)](https://github.com/xtomasnemec/OCLP-Plus/releases)

</div>

### Experimental macOS Tahoe support

## Compatible models:
```
MacBookPro14,x
MacBook10,1
iMac18,x - 19,1 (No Fusion drive support!)
```
> [!NOTE]
> Other Macs may be supported, newer Macs have the T2 chip and they can't boot MacOS via OpenCore. Older Macs do not support Metal 3. Your mileage may vary!

## Building EFI form Windows

Example build command for building OpenCore for MacBookPro14,1:

```
.\.venv\Scripts\python -c "from oclp_plus.application_entry import main; main()" --build --model MacBookPro14,1
```

### Wireless & Continuity Restoration
Restores full functionality for Broadcom-based wireless chipsets (BCM4360/4350/943224/94331):

### Modern Audio (AppleHDA Restoration)
Starting with macOS Tahoe Beta 2, Apple removed the legacy `AppleHDA.kext`. This patch set brings it back, ensuring built-in audio works on supported legacy systems.
*  **Manual Toggle:** A new "Modern Audio" toggle in the Root Patches menu allows you to enable or disable this restoration manually.
*  **KDK Integration:** Automatically handles the necessary Kernel Debug Kit (KDK) requirements for audio driver linking.

## Important Technical Notes
*  **Graphics patches for Non-Metal and Legacy Metal are not supported, only use this for Macs introduced in 2017 onwards**

### [`Build and run from source`](https://github.com/xtomasnemec/OCLP-Plus/blob/main/SOURCE.md)

### Installation Requirements
**Before Running Post-Install Patches:**
* **KDK is mandatory:** For macOS 13 through Tahoe (26.x), the Kernel Debug Kit must be installed for drivers like AppleHDA to link correctly. Use the Help > Download KDK button.

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
This is an **experimental Project** intended for advanced users and complex Hackintosh/Legacy Mac configurations. Use at your own risk.

**Community Discussion:** [`InsanelyMac Thread`](https://www.insanelymac.com/forum/topic/362543-the-latest-the-oclp-plus-318-tahoe-patch-set-is-out/)
