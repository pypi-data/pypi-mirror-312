def transfer_str_to_dict(argument: str):
    # argument is a string in the format of key1=value1&key2=value2
    raw_pairs = [tuple(arg.split("=")) for arg in argument.split("&")]
    cleaned_pairs = [(key.strip(), value.strip()) for key, value in raw_pairs]
    return dict(cleaned_pairs)