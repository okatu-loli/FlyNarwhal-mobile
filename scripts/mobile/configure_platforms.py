#!/usr/bin/env python3
"""Add the permissions needed by generated Flutter mobile runners."""
from pathlib import Path
import plistlib
import sys
import xml.etree.ElementTree as ET

ANDROID = "http://schemas.android.com/apk/res/android"


def configure_android() -> None:
    manifest = Path("android/app/src/main/AndroidManifest.xml")
    ET.register_namespace("android", ANDROID)
    tree = ET.parse(manifest)
    root = tree.getroot()
    permission = f"{{{ANDROID}}}name"
    if not any(
        element.get(permission) == "android.permission.INTERNET"
        for element in root.findall("uses-permission")
    ):
        ET.Element(root, "uses-permission", {permission: "android.permission.INTERNET"})
    tree.write(manifest, encoding="utf-8", xml_declaration=True)


def configure_ios() -> None:
    info = Path("ios/Runner/Info.plist")
    with info.open("rb") as source:
        values = plistlib.load(source)
    values["NSLocalNetworkUsageDescription"] = "用于连接局域网中的飞牛 NAS"
    with info.open("wb") as destination:
        plistlib.dump(values, destination)


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"android", "ios"}:
        raise SystemExit("Usage: configure_platforms.py android|ios")
    {"android": configure_android, "ios": configure_ios}[sys.argv[1]]()
