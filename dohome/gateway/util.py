"""Gateway utility functions"""

def apply_mask(local_address: str, mask: str) -> str:
    """Applies the netmask to the /24 address"""
    segments = local_address.split(".")
    mask_segments = mask.split(".")
    result_address = ""
    index = 0
    for segment in mask_segments:
        if len(result_address) > 0:
            result_address += "."
        if segment == "255":
            result_address += f"{segments[index]}"
        elif segment == "0":
            result_address += "255"
        index += 1
    return result_address

def parse_pong(message: str) -> dict:
    """Parses DoHome pong response"""
    records = list(map(lambda x: x.split('='), message.split('&')))
    descr = {
        record[0]: record[1].strip() for record in records
    }
    name = descr["device_name"]
    descr["sid"] = name[len(name) - 4:]
    return descr
