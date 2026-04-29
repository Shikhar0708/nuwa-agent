def classify_intent(user):
    u = user.lower()

    if "edit" in u or "modify" in u:
        return "edit"
    if "debug" in u or "fix" in u:
        return "debug"
    if "explain" in u:
        return "explain"

    return "generate"