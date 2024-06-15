from networking.common import *
from networking.server.login_manager import LoginManager
from networking.server.models import User, SavedGame
from . import Room
import chess
import asyncio

@dataclass
class Game:
    hostname :str
    guestname :str
    board :chess.Board
    msgs :list[str]

    host :ServerConnection
    guest :ServerConnection
    spectators :list[ServerConnection]
    host_user :User
    guest_user :User

    def to_msg(self, to_host :bool | None) -> GameState:
        can_move = False
        if self.board.turn == chess.WHITE and to_host == True:
            can_move = True
        elif self.board.turn == chess.BLACK and to_host == False:
            can_move = True
        return GameState(
            self.hostname,
            self.guestname,
            can_move,
            to_host == None,
            self.msgs,
            [str(move) for move in self.board.move_stack],
            self.board,
        )

class GameManager:
    _games :list[Game] 

    def __init__(self):
        self._games = []
        self.scan_task = asyncio.create_task(self.scan_dead_connections())

    def start_game(self, room :Room):
        game = Game(
            hostname=room.host_username,
            guestname=room.guest_username,
            board=chess.Board(),
            msgs=[],
            host=room.host,
            guest=room.guest,
            spectators=room.spectators,
            host_user=LoginManager.instance.get_user(room.host),
            guest_user=LoginManager.instance.get_user(room.guest)
        )
        room.host.send(GameStarted(game.to_msg(True)))
        room.guest.send(GameStarted(game.to_msg(False)))
        for conn in room.spectators:
            conn.send(GameStarted(game.to_msg(None)))
        self._games.append(game)

    def process_message(self, msg :Message):
        processors = {
            MSG_GAME_MOVE_REQUEST: self._process_move_request,
            MSG_GAME_SEND_MSG_REQUEST: self._process_msg_request,
            MSG_GAME_SURRENDER_REUQEST: self._process_surrender_request,
            MSG_GAME_HISTORY_REQUEST: self._process_game_history,
            MSG_LEAVE_SPECTATE_REQUEST: self._process_leave_spectate,
        }
        if msg.msg_type in processors:
            processors[msg.msg_type](msg)

    async def scan_dead_connections(self):
        while True:
            for game in self._games:
                if not game.host.is_alive():
                    self.timeout_host(game)
                elif not game.guest.is_alive():
                    self.timeout_guest()
                spectators_copy = [s for s in game.spectators]
                for s in spectators_copy:
                    if not s.is_alive():
                        game.spectators.remove(s)
            await asyncio.sleep(1)

    def _process_move_request(self, msg :GameMoveRequest):
        game = self._find_game(msg.owner)
        if not game:
            msg.owner.send(Response(msg.id, False, 'You are not in a game'))
        elif not msg.move in list(game.board.legal_moves):
            msg.owner.send(Response(msg.id, False, 'Illegar move'))
        elif msg.owner == game.host and game.board.turn != chess.WHITE:
            msg.owner.send(Response(msg.id, False, 'Not your turn'))
        elif msg.owner == game.guest and game.board.turn != chess.BLACK:
            msg.owner.send(Response(msg.id, False, 'Not your turn'))
        else:
            game.board.push(msg.move)
            game.guest.send(GameUpdated(game.to_msg(False)))
            game.host.send(GameUpdated(game.to_msg(True)))
            for conn in game.spectators:
                conn.send(GameUpdated(game.to_msg(None)))

            msg.owner.send(Response(msg.id, True))

    def _process_msg_request(self, msg :GameSendMsgRequest):
        game = self._find_game(msg.owner)
        if not game:
            msg.owner.send(Response(msg.id, False, 'You are not in a game'))
        else:
            name = game.hostname if msg.owner == game.host else game.guestname
            game.msgs.append(f'{name}: {msg.msg}')
            game.guest.send(GameUpdated(game.to_msg(False)))
            game.host.send(GameUpdated(game.to_msg(True)))
            for conn in game.spectators:
                conn.send(GameUpdated(game.to_msg(None)))

            msg.owner.send(Response(msg.id, True))

    def _process_surrender_request(self, msg :GameSurrenderRequest):
        game = self._find_game(msg.owner)
        if not game:
            msg.owner.send(Response(msg.id, False, 'You are not in a game'))
        else:
            white_won = msg.owner == game.guest
            self._send_everyone(game, GameEnded(white_won, 'Surrender'))

            msg.owner.send(Response(msg.id, True))
            self.save_game(game, white_won)
            self._games.remove(game)

    def _process_game_history(self, msg :GameHistoryRequest):
        user = LoginManager.instance.get_user(msg.owner)
        games :list[SavedGame] = SavedGame.select().where(SavedGame.host == user)
        games += SavedGame.select().where(SavedGame.guest == user)

        records = []
        for game in games:
            records.append(GameRecord(
                moves=[chess.Move.from_uci(move) for move in game.moves.split()],
                hostname=game.host.username,
                guestname=game.guest.username,
                win=game.win,
                date_played=game.date_played
            ))
        msg.owner.send(GameHistoryResponse(records, msg.id))

    def _process_leave_spectate(self, msg :LeaveSpectateRequest):
        game = self._find_game(msg.owner)
        print('processing elave request')
        if not game:
            msg.owner.send(Response(msg.id, False, 'You are not spectating anything'))
        elif not msg.owner in game.spectators:
            msg.owner.send(Response(msg.id, False, 'You are not a spectator'))
        else:
            game.spectators.remove(msg.owner)
            msg.owner.send(Response(msg.id, True))

    def _find_game(self, conn :ClientConnection) -> Game | None:
        for game in self._games:
            if game.guest == conn:
                return game
            if game.host == conn:
                return game
            if conn in game.spectators:
                return game
        return None

    def _send_everyone(self, game :Game, msg :Message):
        game.host.send(msg)
        game.guest.send(msg)
        for spectator in game.spectators:
            spectator.send(msg)

    def timeout_host(self, game :Game):
        self._send_everyone(game, (GameEnded(False, 'White left the room')))
        self.save_game(game, False)
        self._games.remove(game)

    def timeout_guest(self, game :Game):
        self._send_everyone(game, (GameEnded(True, 'Black left the room')))
        self.save_game(game, True)
        self._games.remove(game)

    def save_game(self, game :Game, win :chess.Color | None):
        host = game.host_user
        guest = game.guest_user
        moves = ' '.join([move.uci() for move in game.board.move_stack])

        SavedGame.create(
            host = host,
            guest = guest,
            win = win,
            moves = moves,
        )