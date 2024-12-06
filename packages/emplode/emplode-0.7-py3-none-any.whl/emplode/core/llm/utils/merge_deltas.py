def merge_deltas(original, delta):

    for key, value in dict(delta).items():
        if value != None:
            if isinstance(value, str):
                if key in original:
                    original[key] = (original[key] or "") + (value or "")
                else:
                    original[key] = value
            else:
                value = dict(value)
                if key not in original:
                    original[key] = value
                else:
                    merge_deltas(original[key], value)

    return original
