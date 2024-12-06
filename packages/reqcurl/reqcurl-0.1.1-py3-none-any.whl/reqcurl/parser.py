import shlex

def parse_curl(curl_command):
    """
    Parses a cURL command string into a dictionary for use with requests.
    """
    tokens = shlex.split(curl_command)
    
    if tokens[0] != "curl":
        raise ValueError("The input command is not a valid cURL command.")

    request_details = {
        "method": "GET",  # Default method
        "url": None,
        "headers": {},
        "data": None,
        "auth": None,
    }

    i = 1
    while i < len(tokens):
        token = tokens[i]

        if token == "-X":  # HTTP method
            i += 1
            request_details["method"] = tokens[i]

        elif token.startswith("http"):  # URL
            request_details["url"] = token

        elif token == "-H":  # Headers
            i += 1
            header = tokens[i].split(": ", 1)
            if len(header) == 2:
                key, value = header
                request_details["headers"][key] = value
            else:
                raise ValueError(f"Invalid header format: {tokens[i]}")

        elif token in ("-d", "--data"):  # Data payload
            i += 1
            # Check if the data contains key-value pairs (e.g., "key=value")
            data_str = tokens[i]
            data_dict = {}
            for pair in data_str.split("&"):
                key_value = pair.split("=", 1)
                if len(key_value) == 2:
                    data_dict[key_value[0]] = key_value[1]
                else:
                    raise ValueError(f"Invalid data format: {pair}")
            request_details["data"] = data_dict

        elif token == "--user":  # Authentication
            i += 1
            user_info = tokens[i].split(":", 1)
            if len(user_info) == 2:
                request_details["auth"] = (user_info[0], user_info[1])
            else:
                raise ValueError(f"Invalid authentication format: {tokens[i]}")

        i += 1

    if not request_details["url"]:
        raise ValueError("URL is missing in the cURL command.")

    return request_details
