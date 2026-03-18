"""Doit WiFi types"""

from typing import TypedDict, TypeGuard

from dohome.types.common import DoDict

DoWiFiCredentials = TypedDict("DoWiFiCredentials", {"ssid": str, "pass": str})


class DoWiFiCredentialsResponse(DoWiFiCredentials):
    dev_id: str


def is_doit_wifi_credentials_response(
    x: DoDict,
) -> TypeGuard[DoWiFiCredentialsResponse]:
    return (
        isinstance(x["dev_id"], str)
        and isinstance(x["ssid"], str)
        and isinstance(x["pass"], str)
    )
