<div align="center">
<img src="https://github.com/YBronst/OCLP-Plus/blob/main/docs/images/OC-Patcher.png"  alt="OC-Patcher Logo" width="256" />

# [OCLP-Plus (Tahoe Patch Set)](https://github.com/xtomasnemec/OCLP-Plus/releases)

</div>

### Experimental macOS Tahoe support

## Compatible models:
```
MacBookPro13,1 (Sppofed GPU, 13,2 - No T1 support! 13,3 - No T1 and dGPU support!)
MacBookPro14,1 (14,2 - No T1 support! 14,3 - No T1 and dGPU support!)
MacBook9,1 (Spoofed GPU)
MacBook10,1
iMac18,x - 19,x (No Fusion drive support! Upgrade to an SSD!)
```

**Graphics patches for Non-Metal, Legacy Metal and patches for T1 and T2 Macs are not supported**

> [!NOTE]
> Other Macs may be supported (the program doesn't block them and still *probably* creates a working OpenCore config), newer Macs have the T2 chip and they can't boot macOS via OpenCore. Older Macs do not support Metal 3 (so no graphics acceleration), 2016 Skylake Macs without dGPUs are partially supported with GPU spoofing. **Your mileage may vary!**
>
> You may also enable untested Root Patches, they probably won't work or they may break your macOS install. **Proceed with caution!**

## Building EFI form Windows

Example build command for building OpenCore for MacBookPro14,1:

```
.\.venv\Scripts\python -c "from oclp_plus.application_entry import main; main()" --build --model MacBookPro14,1
```
 
## Non-functional features
*  **On majority of patched Macs, iPhone Mirroring and Apple Intelligence won't be functional.**
  
   *  iPhone Mirroring requires T2 for attestation and Apple Intelligence requires an NPU only found in Apple Silicon.
   *  The patcher is unable to provide a fix for these as they're hardware requirements.

## Tested Root Patches:

### Wireless & Continuity Restoration
Restores full functionality for Broadcom-based wireless chipsets found in most 2009 - 2017 Macs (BRCM4360/4350 and BCM943224/94331):

## PCIe webcam
Restores full functionality for PCIe webcams found in MacBooks and iMacs before 2018

### Modern Audio (AppleHDA Restoration)
Restores the `AppleHDA.kext`. Works for all non-T2 Macs that had native audio in Sequoia. Requires the KDK.
*  **Manual Toggle:** A new "Modern Audio" toggle in the Root Patches menu allows you to enable or disable this restoration manually.
*  **KDK Integration:** Automatically handles the necessary Kernel Debug Kit (KDK) requirements for audio driver linking.

### Intel Wi-Fi (AirportItlwm) is NOT supported 
*  **This fork is exclusively optimized for Broadcom-based wireless chipsets.** If you require Intel Wi-Fi patches for Tahoe, please use [OCLP-Mod](https://github.com/laobamac/OCLP-Mod).

### [`Build and run from source`](https://github.com/xtomasnemec/OCLP-Plus/blob/main/SOURCE.md)


### Installation Requirements
**Before Running Post-Install Patches:**
**KDK is mandatory:** For macOS 13 through Tahoe (26.x), the Kernel Debug Kit must be installed for drivers like AppleHDA to link correctly. Use the Help > Download KDK button.

**Root Volume Dirty Error:**
If the patcher detects that the system volume has been modified (e.g., patches already applied or seal broken), it will block further patching to prevent system instability.
* **To re-patch:** You must first use the "Revert Root Patches" button to restore the original system state.
* **If no manifest is found:** If the volume is modified but the patcher cannot find a record of what was installed, it will display a "Root volume is modified" error. In this case, you should still attempt a "Revert Root Patches" or reinstall macOS to clean the volume.

<details>
<summary><b>Advanced: Manual Force Restore (Emergency only)</b></summary>

If the "Revert Root Patches" button fails to clear the dirty state, you can manually force macOS to boot from the last sealed snapshot via Terminal:

```bash
sudo bless --mount /Volumes/YourVolumeName --bootefi --last-sealed-snapshot
```
*Replace `YourVolumeName` with your actual system drive name (e.g., `Macintosh\ HD`).*
</details>
s
<br>

**Resource Dependency Notice**
* **Patcher Resources:** This version relies on the [`PatcherSupportPkg`](https://github.com/YBronst/PatcherSupportPkg) for native Tahoe binaries.

## Credits
*   [`Acidanthera`](https://github.com/Acidanthera) (OpenCorePkg, Lilu, etc.)
*   [`Dortania Team`](https://github.com/dortania) (Original OCLP authors)
*   [`lzhoang2801`](https://github.com/kgp-macPro/OCLP-lzhoang2801) (Original Tahoe patchset)
*   [`CloverHackyColor`](https://github.com/CloverHackyColor) (Hackintosh essentials and beyond)
*   [`laobamac`](https://github.com/laobamac) (Developer OCLP-Mod, Chinese language)
*   [`YBronst`](https://github.com/YBronst) (Original OCLP-PLUS developer)
*   [`xtomasnemec`](https://github.com/xtomasnemec)
*   *Full list of OCLP contributors can be found in the [`original repository`](https://github.com/dortania/OpenCore-Legacy-Patcher).*

## Disclaimer
This is an **experimental Project** intended for advanced users. **Use at your own risk!**
