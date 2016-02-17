
def normalize(id):
    id = str(id)
    if id is None or len(id) == 0:
        return None
    new_id = id.translate(None,' +.()-').strip()
    if not new_id or not new_id.isdigit():
        return None
    return new_id


def normalize_list(ids):
    result = []
    for id in ids:
        normalized_id = normalize(id)
        if normalized_id is None:
            continue
        result.append(normalized_id)
    return result


def normalize_list_field(dictionary, field):
    result = []
    for value in dictionary:
        id = value.get (field)
        if id is None:
            continue
        normalized_id = normalize(id)
        if normalized_id is None:
            continue
        value[field] = normalized_id
        result.append(value)
    return result
