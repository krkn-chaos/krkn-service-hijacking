from typing import Any, Optional


def validate_step(step: dict[Any]) -> Optional[str]:
    errors = list[str]()
    if "duration" not in step:
        errors.append("duration")
    if "status" not in step:
        errors.append("status")
    if "mime_type" not in step:
        errors.append("mime_type")

    if len(errors) > 0:
        return ", ".join(errors)
    return None
