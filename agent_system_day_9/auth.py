USER_ROLE = "accountant"

PERMISSIONS = {
    "accountant": ["create_invoice"],
    "manager": ["create_invoice", "approve_invoice"]
}


def authorize(action: str):
    allowed = PERMISSIONS.get(USER_ROLE, [])

    if action not in allowed:
        raise PermissionError(f"User not allowed to perform {action}")