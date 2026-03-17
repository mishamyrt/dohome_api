"""DoIT API WiFi types"""

from typing import TypedDict

SetWiFiCredentialsParams = TypedDict(
    "SetWiFiCredentialsParams", {"ssid": str, "pass": str}
)

GetWiFiCredentialsResponse = TypedDict(
    "GetWiFiCredentialsResponse", {"dev_id": str, "ssid": str, "pass": str}
)
