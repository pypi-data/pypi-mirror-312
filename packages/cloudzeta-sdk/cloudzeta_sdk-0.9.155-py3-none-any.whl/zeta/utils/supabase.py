import base64
import re
import uuid


def is_valid_uuid(uuid_str: str) -> bool:
    """Check if string is a valid UUID"""
    uuid_pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
    return bool(uuid_pattern.match(uuid_str))


def is_valid_user_uid(uid: str) -> bool:
    """
    Validates if a string is a valid Firebase UID.
    User UIDs are either 28 characters (migrated from Firebase) or 22 characters (newly generated).

    Args:
        uid: Firebase-style UID to validate
    Returns:
        bool: True if valid Firebase UID format, False otherwise
    """
    if not isinstance(uid, str):
        return False

    # Firebase UIDs are 28 characters
    if len(uid) != 28 and len(uid) != 22:
        return False

    # Check if it only contains valid base64url characters
    return bool(re.match(r'^[A-Za-z0-9_-]+$', uid))


def user_uid_to_uuid(uid: str) -> str:
    """
    Converts a Firebase-style UID back to a UUID.
    This is the inverse operation of uuid_to_user_uid.

    Args:
        uid: Firebase-style UID (28 characters)
    Returns:
        Standard UUID (e.g., "123e4567-e89b-12d3-a456-426614174000")
    """
    # Validate Firebase UID format
    if not is_valid_user_uid(uid):
        raise ValueError("Invalid Firebase UID format")

    # Restore base64 padding if needed
    padded_uid = uid[:22].replace("-", "+").replace("_", "/")
    padding_length = (4 - (len(padded_uid) % 4)) % 4
    padded_uid += "=" * padding_length

    # Decode base64 back to bytes
    try:
        buffer = base64.b64decode(padded_uid)
    except Exception as e:
        raise ValueError(f"Invalid base64 encoding in UID: {e}")

    # Convert bytes to hex string
    hex_str = buffer.hex()

    # Insert hyphens to create UUID format
    uuid_str = f"{hex_str[:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:]}"

    # Validate the resulting UUID
    try:
        uuid.UUID(uuid_str)
    except ValueError as e:
        raise ValueError(f"Resulting UUID is invalid: {e}")

    return uuid_str


def uuid_to_user_uid(uuid: str) -> str:
    """
    Converts a UUID to a Firebase-style UID.
    This is a deterministic conversion - the same UUID will always produce the same Firebase UID.

    Args:
        uuid: Standard UUID (e.g., "123e4567-e89b-12d3-a456-426614174000")
    Returns:
        Firebase-style UID (28 characters)
    """
    # Validate UUID format
    if not is_valid_uuid(uuid):
        raise ValueError("Invalid UUID format")

    # Remove hyphens from UUID
    clean_uuid = uuid.replace("-", "")

    # Convert hex string to bytes and then to Base64URL
    buffer = bytes.fromhex(clean_uuid)
    base64_str = base64.b64encode(buffer).decode("ascii") \
        .replace("+", "-") \
        .replace("/", "_") \
        .replace("=", "")

    return base64_str


def get_supabase_user_uid(user) -> str:
    if user.user_metadata.get("fbuser"):
        return user.user_metadata.get("fbuser").get("uid")
    else:
        return uuid_to_user_uid(user.id)