
def normalize(id):
    id = str(id)
    if id is None:
        return None
    new_id = id.translate(None,' +.()-').strip()
    if not new_id or not new_id.isdigit():
        return None
    return new_id