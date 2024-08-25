from typing import Callable, Optional
from enum import Enum

class EventType(Enum):
    SINGLE = "single"
    DOUBLE = "double"
    HOLD = "hold"
    RELEASE = "release"

class Button:
    def __init__(self,
                 on_single: Optional[Callable] = None,
                 on_double: Optional[Callable] = None,
                 on_hold: Optional[Callable] = None,
                 on_release: Optional[Callable] = None):
        self.handle_single = on_single
        self.handle_double = on_double
        self.handle_hold = on_hold
        self.handle_release = on_release

    async def handle_event(self, event):
        try:
            event_type = EventType(event["action"])
        except ValueError:
            print(f"Unknown event type: {event['action']}")
            return

        match event_type:
            case EventType.SINGLE:
                if self.handle_single:
                    await self.handle_single(event)
            case EventType.DOUBLE:
                if self.handle_double:
                    await self.handle_double(event)
            case EventType.HOLD:
                if self.handle_hold:
                    await self.handle_hold(event)
            case EventType.RELEASE:
                if self.handle_release:
                    await self.handle_release(event)

