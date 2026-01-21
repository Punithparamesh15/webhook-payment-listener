from typing import Any, Dict, Tuple, List

class PayloadError(ValueError):
    pass

def extract_fields(data: Dict[str, Any]) -> Tuple[str, str, str]:
    try:
        event_type = data["event"]
        event_id = data["id"]
        payment_id = data["payload"]["payment"]["entity"]["id"]
    except (KeyError, TypeError):
        raise PayloadError("Missing required fields: event, id, payload.payment.entity.id")

    if not event_type or not event_id or not payment_id:
        raise PayloadError("Required fields cannot be empty.")

    return event_type, event_id, payment_id

def ensure_event_list(payload: Any) -> List[Dict[str, Any]]:
    """
    Company payload is a LIST of events.
    Webhook in real world is often a single event dict.
    This function supports BOTH.

    Returns a list of event dicts.
    """
    if isinstance(payload, dict):
        return [payload]
    if isinstance(payload, list) and all(isinstance(item, dict) for item in payload):
        return payload
    raise PayloadError("Payload must be an object or a list of objects.")

def normalize_event_type(event_type: str) -> str:
    # sample response shows underscore style
    return event_type.replace(".", "_").lower()