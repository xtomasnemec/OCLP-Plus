"""
application_entry.py: Project entry point
"""

import os
import sys
import time
import logging
import threading

from pathlib import Path

from . import constants

from .detections import (
    device_probe,
    os_probe
)
from .support import (
    utilities,
    defaults,
    arguments,
    reroute_payloads,
    commit_info,
    logging_handler,
    analytics_handler
)


class OpenCoreLegacyPatcher:
    """
    Initial entry point for starting OCLP-Plus
    """

    def __init__(self) -> None:
        self.constants: constants.Constants = constants.Constants()

        logging_handler.InitializeLoggingSupport(self.constants)

        self._generate_base_data()

        if utilities.check_cli_args() is None:
            from .wx_gui import gui_entry
            gui_entry.EntryPoint(self.constants).start()


    def _fix_cwd(self) -> None:
        """
        In some extreme scenarios, our current working directory may disappear
        """
        _test_dir = None
        try:
            _test_dir = Path.cwd()
            logging.info(f"Current working directory: {_test_dir}")
        except FileNotFoundError:
            _test_dir = Path(__file__).parent.parent.resolve()
            os.chdir(_test_dir)
            logging.warning(f"Current working directory was invalid, switched to: {_test_dir}")


    def _generate_base_data(self) -> None:
        """
        Generate base data required for the patcher to run
        """

        self.constants.wxpython_variant = True

        # Ensure we live after parent process dies (ie. LaunchAgent)
        if hasattr(os, "setpgrp"):
            os.setpgrp()

        args = utilities.check_cli_args()
        offline_build_mode = (
            args is not None
            and getattr(args, "build", False) is True
            and getattr(args, "model", None)
            and sys.platform != "darwin"
        )

        if offline_build_mode:
            logging.info("Non-macOS host detected, enabling offline build mode")

            # OS / host probing is macOS-specific; keep values minimal.
            self.constants.detected_os = 0
            self.constants.detected_os_minor = 0
            self.constants.detected_os_build = ""
            self.constants.detected_os_version = ""

            # Provide a minimal computer object so builders can reference it.
            self.constants.computer = device_probe.Computer()
            self.computer = self.constants.computer
            self.constants.booted_oc_disk = None

            # Generate environment data
            self.constants.recovery_status = False
            utilities.disable_cls()
            self._fix_cwd()

            # Generate binary data
            launcher_script = None
            launcher_binary = sys.executable
            if "python" in launcher_binary:
                launcher_script = __file__
            self.constants.launcher_binary = launcher_binary
            self.constants.launcher_script = launcher_script

            # Initialize working directory (no-op for source builds)
            self.constants.unpack_thread = threading.Thread(target=reroute_payloads.RoutePayloadDiskImage, args=(self.constants,))
            self.constants.unpack_thread.start()

            # Generate commit info
            self.constants.commit_info = commit_info.ParseCommitInfo(self.constants.launcher_binary).generate_commit_info()

            # Defaults for target model
            defaults.GenerateDefaults(args.model, False, self.constants, ignore_settings_file=True)

            self.constants.cli_mode = True
            self.constants.gui_mode = True  # Assumes no user interaction is required

            # Wait for unpack thread if needed
            while self.constants.unpack_thread.is_alive():
                time.sleep(self.constants.thread_sleep_interval)

            arguments.arguments(self.constants)
            return

        # Generate OS data
        os_data = os_probe.OSProbe()
        self.constants.detected_os = os_data.detect_kernel_major()
        self.constants.detected_os_minor = os_data.detect_kernel_minor()
        self.constants.detected_os_build = os_data.detect_os_build()
        self.constants.detected_os_version = os_data.detect_os_version()

        # Generate computer data
        self.constants.computer = device_probe.Computer.probe()
        self.computer = self.constants.computer
        self.constants.booted_oc_disk = utilities.find_disk_off_uuid(utilities.clean_device_path(self.computer.opencore_path))
        if self.constants.computer.firmware_vendor:
            if self.constants.computer.firmware_vendor != "Apple":
                self.constants.host_is_hackintosh = True

        # Generate environment data
        self.constants.recovery_status = utilities.check_recovery()
        utilities.disable_cls()
        self._fix_cwd()

        # Generate binary data
        launcher_script = None
        launcher_binary = sys.executable
        if "python" in launcher_binary:
            # We're running from source
            launcher_script =  __file__
            if "main.py" in launcher_script:
                launcher_script = launcher_script.replace("/resources/main.py", "/OCLP-Plus-GUI.command")
        self.constants.launcher_binary = launcher_binary
        self.constants.launcher_script = launcher_script

        # Initialize working directory
        self.constants.unpack_thread = threading.Thread(target=reroute_payloads.RoutePayloadDiskImage, args=(self.constants,))
        self.constants.unpack_thread.start()

        # Generate commit info
        self.constants.commit_info = commit_info.ParseCommitInfo(self.constants.launcher_binary).generate_commit_info()
        if self.constants.commit_info[0] not in ["Running from source", "Built from source"]:
            # Now that we have commit info, update nightly link
            branch = self.constants.commit_info[0]
            branch = branch.replace("refs/heads/", "")
            self.constants.installer_pkg_url_nightly = self.constants.installer_pkg_url_nightly.replace("main", branch)

        # Generate defaults
        defaults.GenerateDefaults(self.computer.real_model, True, self.constants)
        threading.Thread(target=analytics_handler.Analytics(self.constants).send_analytics).start()

        if args is None:
            self.constants.cli_mode = False
            return

        logging.info("Detected arguments, switching to CLI mode")
        self.constants.gui_mode = True  # Assumes no user interaction is required

        ignore_args = ["--auto_patch", "--gui_patch", "--gui_unpatch", "--update_installed"]
        if not any(x in sys.argv for x in ignore_args):
            self.constants.current_path = Path.cwd()
        ignore_args = ignore_args.pop(0)

        if not any(x in sys.argv for x in ignore_args):
            while self.constants.unpack_thread.is_alive():
                time.sleep(self.constants.thread_sleep_interval)

        arguments.arguments(self.constants)

def main():
    """
    Main entry point
    """
    OpenCoreLegacyPatcher()