"""oclp_plus.detections.ioreg

PyObjC handling for IOKit.

OCLP-Plus is primarily intended to run on macOS. Some repo workflows (ex. CI or
building OpenCore for an external model) benefit from being able to *import*
the codebase on non-macOS platforms.

On non-macOS platforms this module provides import-safe stubs. Any attempt to
call IOKit functions will raise a RuntimeError.
"""

from __future__ import annotations

import sys
from typing import Any, NewType, Union


IOREG_AVAILABLE: bool = sys.platform == "darwin"


# Shared type aliases (used for typing across the codebase)
kern_return_t = NewType("kern_return_t", int)
boolean_t = int

io_object_t = NewType("io_object_t", object)
io_registry_entry_t = io_object_t
io_iterator_t = NewType("io_iterator_t", io_object_t)

io_name_t = bytes
io_string_t = bytes

CFTypeRef = Union[int, float, bytes, dict, list]

IOOptionBits = int
mach_port_t = int

NULL = 0

# IOKitLib.h
kIORegistryIterateRecursively = 1
kIORegistryIterateParents = 2


def _unavailable(*_args: Any, **_kwargs: Any):
    raise RuntimeError("IOKit/ioreg is only available on macOS (PyObjC required)")


if not IOREG_AVAILABLE:
    # Constants referenced by callers.
    kIOMasterPortDefault: mach_port_t = 0
    kNilOptions: IOOptionBits = 0

    # API surface used by OCLP on macOS.
    IORegistryEntryCreateCFProperties = _unavailable
    IOServiceMatching = _unavailable
    IOServiceGetMatchingServices = _unavailable
    IOIteratorNext = _unavailable
    IORegistryEntryGetParentEntry = _unavailable
    IOObjectRelease = _unavailable
    IORegistryEntryGetName = _unavailable
    IOObjectGetClass = _unavailable
    IOObjectCopyClass = _unavailable
    IOObjectCopySuperclassForClass = _unavailable
    IORegistryEntryGetChildIterator = _unavailable
    IORegistryCreateIterator = _unavailable
    IORegistryEntryCreateIterator = _unavailable
    IORegistryIteratorEnterEntry = _unavailable
    IORegistryIteratorExitEntry = _unavailable
    IORegistryEntryCreateCFProperty = _unavailable
    IORegistryEntryGetPath = _unavailable
    IORegistryEntryCopyPath = _unavailable
    IOObjectConformsTo = _unavailable
    IORegistryEntryGetLocationInPlane = _unavailable
    IOServiceNameMatching = _unavailable
    IORegistryEntryGetRegistryEntryID = _unavailable
    IORegistryEntryIDMatching = _unavailable
    IORegistryEntryFromPath = _unavailable


    def ioiterator_to_list(_iterator: io_iterator_t):
        return []


    def corefoundation_to_native(_collection: Any):
        return None


    def native_to_corefoundation(native: Any):
        return native


    def io_name_t_to_str(name: bytes) -> str:
        return name.partition(b"\0")[0].decode(errors="ignore")


    def get_class_inheritance(_io_object: io_object_t):
        return []


else:
    import objc
    from CoreFoundation import CFRelease, kCFAllocatorDefault  # type: ignore # pylint: disable=no-name-in-module
    from Foundation import NSBundle  # type: ignore # pylint: disable=no-name-in-module
    from PyObjCTools import Conversion

    IOKit_bundle = NSBundle.bundleWithIdentifier_("com.apple.framework.IOKit")

    # pylint: disable=invalid-name
    io_name_t_ref_out = b"[128c]"  # io_name_t is char[128]
    const_io_name_t_ref_in = b"r*"
    CFStringRef = b"^{__CFString=}"
    CFDictionaryRef = b"^{__CFDictionary=}"
    CFAllocatorRef = b"^{__CFAllocator=}"
    # pylint: enable=invalid-name

    # https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtTypeEncodings.html
    functions = [
        ("IORegistryEntryCreateCFProperties", b"IIo^@" + CFAllocatorRef + b"I"),
        ("IOServiceMatching", CFDictionaryRef + b"r*"),
        ("IOServiceGetMatchingServices", b"II" + CFDictionaryRef + b"o^I"),
        ("IOIteratorNext", b"II"),
        ("IORegistryEntryGetParentEntry", b"IIr*o^I"),
        ("IOObjectRelease", b"II"),
        ("IORegistryEntryGetName", b"IIo" + io_name_t_ref_out),
        ("IOObjectGetClass", b"IIo" + io_name_t_ref_out),
        ("IOObjectCopyClass", CFStringRef + b"I"),
        ("IOObjectCopySuperclassForClass", CFStringRef + CFStringRef),
        ("IORegistryEntryGetChildIterator", b"IIr*o^I"),
        ("IORegistryCreateIterator", b"IIr*Io^I"),
        ("IORegistryEntryCreateIterator", b"IIr*Io^I"),
        ("IORegistryIteratorEnterEntry", b"II"),
        ("IORegistryIteratorExitEntry", b"II"),
        ("IORegistryEntryCreateCFProperty", b"@I" + CFStringRef + CFAllocatorRef + b"I"),
        ("IORegistryEntryGetPath", b"IIr*oI"),
        ("IORegistryEntryCopyPath", CFStringRef + b"Ir*"),
        ("IOObjectConformsTo", b"II" + const_io_name_t_ref_in),
        ("IORegistryEntryGetLocationInPlane", b"II" + const_io_name_t_ref_in + b"o" + io_name_t_ref_out),
        ("IOServiceNameMatching", CFDictionaryRef + b"r*"),
        ("IORegistryEntryGetRegistryEntryID", b"IIo^Q"),
        ("IORegistryEntryIDMatching", CFDictionaryRef + b"Q"),
        ("IORegistryEntryFromPath", b"II" + const_io_name_t_ref_in),
    ]

    variables = [("kIOMasterPortDefault", b"I")]

    # Exported symbols expected by callers.
    kIOMasterPortDefault: mach_port_t
    kNilOptions: IOOptionBits = NULL

    objc.loadBundleFunctions(IOKit_bundle, globals(), functions)  # type: ignore # pylint: disable=no-member
    objc.loadBundleVariables(IOKit_bundle, globals(), variables)  # type: ignore # pylint: disable=no-member


    def ioiterator_to_list(iterator: io_iterator_t):
        item = IOIteratorNext(iterator)  # noqa: F821
        while item:
            yield item
            item = IOIteratorNext(iterator)  # noqa: F821
        IOObjectRelease(iterator)  # noqa: F821


    def corefoundation_to_native(collection):
        if collection is None:  # nullptr
            return None
        native = Conversion.pythonCollectionFromPropertyList(collection)
        CFRelease(collection)
        return native


    def native_to_corefoundation(native):
        return Conversion.propertyListFromPythonCollection(native)


    def io_name_t_to_str(name):
        return name.partition(b"\0")[0].decode()


    def get_class_inheritance(io_object):
        classes = []
        cls = IOObjectCopyClass(io_object)
        while cls:
            classes.append(cls)
            CFRelease(cls)
            cls = IOObjectCopySuperclassForClass(cls)
        return classes
