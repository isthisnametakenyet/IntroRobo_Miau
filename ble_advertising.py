# Helpers for generating BLE advertising payloads.

from micropython import const
import struct
import bluetooth

# Advertising payloads are repeated packets of the following form:
#   1 byte data length (N + 1)
#   1 byte type (see constants below)
#   N bytes type-specific data

# Constants for advertising packet types
_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)


# Generate a payload to be passed to gap_advertise(adv_data=...).
def advertising_payload(limited_disc=False, br_edr=False, name=None, services=None, appearance=0):
    """Generates a BLE advertising payload given the arguments, where:

            limited_disc (bool): Limited discovery mode flag that indicates whether the Bluetooth
                                    device is operating in limited discovery mode.
            br_edr (bool):       Bluetooth Enhanced Data Rate (EDR) flag which is a part of the Bluetooth
                                    advertising packet that indicates whether the Bluetooth device
                                    supports EDR.
            name (str):          Device name to be advertised.
            services (list):     List of Bluetooth UUIDs representing advertised services.
            appearance (int):    Bluetooth appearance value that's a standardized numerical
                                    representation that describes the physical appearance or role of a Bluetooth device.

        And it returns and advertising payload.
        """

    payload = bytearray()

    def _append(adv_type, value):
        nonlocal payload
        payload += struct.pack("BB", len(value) + 1, adv_type) + value

    _append(
        _ADV_TYPE_FLAGS,
        struct.pack("B", (0x01 if limited_disc else 0x02) + (0x18 if br_edr else 0x04)),
    )

    if name:
        _append(_ADV_TYPE_NAME, name)

    if services:
        for uuid in services:
            b = bytes(uuid)
            if len(b) == 2:
                _append(_ADV_TYPE_UUID16_COMPLETE, b)
            elif len(b) == 4:
                _append(_ADV_TYPE_UUID32_COMPLETE, b)
            elif len(b) == 16:
                _append(_ADV_TYPE_UUID128_COMPLETE, b)

    # See org.bluetooth.characteristic.gap.appearance.xml
    if appearance:
        _append(_ADV_TYPE_APPEARANCE, struct.pack("<h", appearance))

    return payload


def decode_field(payload, adv_type):
    """Decodes a specific field from the advertising payload, where:

            payload (bytearray): Advertising payload to be decoded.
            adv_type (int): Type of the advertising field.

        And it returns a list of decoded values for the specified advertising field.
    """

    i = 0
    result = []
    while i + 1 < len(payload):
        if payload[i + 1] == adv_type:
            result.append(payload[i + 2 : i + payload[i] + 1])
        i += 1 + payload[i]
    return result


def decode_name(payload):
    """Decodes the device name from the advertising payload, where:
            payload (bytearray): Advertising payload to be decoded which is represents the information
                                    about a Bluetooth device.
        Where it returns the decoded device name.

    """
    n = decode_field(payload, _ADV_TYPE_NAME)
    return str(n[0], "utf-8") if n else ""


def decode_services(payload):
    """Decodes the list of services from the advertising payload, where:
            payload (bytearray): Advertising payload to be decoded which is represents the information
                                    about a Bluetooth device.
        And it returns a list of Bluetooth UUIDs representing advertised services.
    """
    services = []
    for u in decode_field(payload, _ADV_TYPE_UUID16_COMPLETE):
        services.append(bluetooth.UUID(struct.unpack("<h", u)[0]))
    for u in decode_field(payload, _ADV_TYPE_UUID32_COMPLETE):
        services.append(bluetooth.UUID(struct.unpack("<d", u)[0]))
    for u in decode_field(payload, _ADV_TYPE_UUID128_COMPLETE):
        services.append(bluetooth.UUID(u))
    return services


def demo():
    """Demo function to showcase the usage of the advertising payload functions."""
    payload = advertising_payload(
        name="micropython",
        services=[bluetooth.UUID(0x181A), bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")],
    )
    print(payload)
    print(decode_name(payload))
    print(decode_services(payload))


if __name__ == "__main__":
    demo()
