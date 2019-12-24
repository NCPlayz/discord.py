from typing import Any, Iterable, Tuple

class BaseFlags:
    value: int

    def __init__(self, **kwargs: Any) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
    def __iter__(self) -> Iterator[Tuple[str, bool]]: ...

class SystemChannelFlags(BaseFlags):
    join_notifications: bool
    premium_subscriptions: bool

class MessageFlags(BaseFlags):
    crossposted: bool
    is_crossposted: bool
    suppress_embeds: bool
    source_message_deleted: bool
    urgent: bool
