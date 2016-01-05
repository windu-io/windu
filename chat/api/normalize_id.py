
def normalize(id):
    if id is None:
        return None
    return id.translate(None,' +.()-').strip()