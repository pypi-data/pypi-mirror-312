from datetime import datetime, timezone
from typing import TypeVar, Any, List

from pydantic import BaseModel
from pymongo import ASCENDING, DESCENDING

T = TypeVar("T", bound=BaseModel)


def set_timestamps(record: T, is_new: bool = False):
    """Sets the created_at, updated_at fields for a record.

    Args:
        record (T): The record to update timestamps for.
        is_new (bool, optional): Whether the record is new. Defaults to False.
    """

    # Check if the record has a created_at attribute and set it if needed
    current_time = datetime.now(timezone.utc)

    if is_new and hasattr(record, "created_at"):
        if getattr(record, "created_at") is None:
            setattr(record, "created_at", current_time)

    # Always update the updated_at field, either on creation, update, or delete
    if hasattr(record, "updated_at"):
        setattr(record, "updated_at", current_time)


# Define operator_map outside the function for reuse and better performance
OPERATOR_MAP = {
    ">=": lambda f, v: f >= v,
    "<=": lambda f, v: f <= v,
    ">": lambda f, v: f > v,
    "<": lambda f, v: f < v,
    "!=": lambda f, v: f != v,
    "in": lambda f, values: f.in_(values),
    "not in": lambda f, values: f.notin_(values),
    "like": lambda f, v: f.like(v),
    "not set": lambda f, v: None if v is None else f == v
}


def apply_operator(field, operator: str, value: Any):
    """Applies an operator to a field based on the provided operator string."""

    operator = operator.lower()

    # Handle the `in` and `not in` operators separately to ensure we pass a list or set
    if operator in ["in", "not in"]:
        if not isinstance(value, (list, set, tuple)):
            raise ValueError(f"`{operator}` operator expects a list, set, or tuple, got {type(value).__name__}")

    apply_op = OPERATOR_MAP.get(operator)

    if apply_op is None:
        raise ValueError(f"Unsupported operator: {operator}")

    # Apply the operator and return the condition
    return apply_op(field, value)


def mongo_build_sort(order_by: str | List[str]) -> List[tuple[str, int]]:
    """Build MongoDB sort parameters."""
    if isinstance(order_by, str):
        order_by = [order_by]

    sort_fields = []
    for field in order_by:
        if field.startswith("-"):
            sort_fields.append((field[1:], DESCENDING))
        else:
            sort_fields.append((field, ASCENDING))

    return sort_fields
