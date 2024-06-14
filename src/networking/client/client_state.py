from enum import Enum, auto
from dataclasses import dataclass

class ConnectionState(Enum):
    CONNECTED = auto()
    CONNECTING = auto()
    DISCONNECTED = auto()
    DISCONNECTING = auto()

@dataclass
class ClientState:
    state :ConnectionState
    error_msg :str = None