from dataclasses import dataclass

@dataclass
class AuthState:
    logged :bool
    username :str = None