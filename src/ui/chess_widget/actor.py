from enum import Enum, auto

class ActorType(Enum):
    ONLINE = auto()
    LOCAL = auto()
    BOT = auto()

class Actor:
    def __init__(self, actor_type :ActorType, player_id :str = None, rating :int = None) -> None:
        rating_set = rating is not None
        player_id_set = player_id is not None
        if actor_type == ActorType.BOT:
            if player_id_set or not rating_set:
                raise ValueError('Bot cant have player id and needs to have rating')
        elif actor_type == ActorType.LOCAL:
            if player_id_set or rating_set:
                raise ValueError('Local player cant have player id or rating')
        elif actor_type == ActorType.ONLINE:
            if not player_id_set or rating_set:
                raise ValueError('Online player cant have rating and needs playerid')

        self.actory_type = actor_type
        self.player_id = player_id
        self.rating = rating