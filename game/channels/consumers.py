from channels.generic.websocket import AsyncWebsocketConsumer
import json
from ..redis.async_redis_utils import add_player_to_game, remove_player_from_game, update_last_seen, add_player_websocket_group, get_player_channel_names, get_players, lock_game, insert_game_into_redis
from ..game.game_logic import setup_game

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.player_name = self.scope['url_route']['kwargs']['player_name']
        self.group_name = f"lobby_{self.game_id}"
        result = await add_player_to_game(self.player_name, self.game_id)
        print("IN CONNECT FUNCTION, result: ", result)
        if result == "success":
            res = await add_player_websocket_group(self.game_id, self.player_name, self.group_name, self.channel_name)
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await update_last_seen(self.game_id, self.player_name) # incase heartbeat is not sent
            await self.accept()
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "message": f"{self.player_name} joined the game",
                    "user": f"{self.player_name}"
                }
            )
        else:
            print("connect failed, hey yeah you yeah")

    async def disconnect(self, closing_code):
        # Leave group
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.player_name = self.scope['url_route']['kwargs']['player_name']
        print("disconnect function, player_name is: ", self.player_name)
        result = await remove_player_from_game(self.player_name, self.game_id)
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data): # tar emot meddelanden från 1 websocket, frontend
        data = json.loads(text_data)

        if data.get("type") == "heartbeat":
            self.game_id = self.scope['url_route']['kwargs']['game_id'] # do we really need self.game_id?
            self.player_name = self.scope['url_route']['kwargs']['player_name']
            await update_last_seen(self.game_id, self.player_name)
            print(f"Received heartbeat from {self.channel_name}")

        if data.get("type") == "setup":
            game_id = self.scope['url_route']['kwargs']['game_id']
            result = lock_game(game_id)
            if result == "failed":
                await self.channel_layer.send(
                    self.channel_name,
                    {
                        "type": "chat_message",
                        "message": "could not start the game, someone else probably initiated the process before you."
                    }
                )
            else:
                channel_names = get_player_channel_names(game_id)
                players = get_players(game_id)
                if len(channel_names) != len(players):
                    print("amount of websockets connections should be equal to number of players") # add proper handeling later
                game = setup_game(players)
                insert_game_into_redis(game_id, game)
                for player_name, channel_name in channel_names.items():
                    wonder = None
                    for game_player in game.players:
                        if game_player.name == player_name:
                            wonder = game_player.wonder
                    if wonder == None:
                        raise Exception("players in the game object, websocket:{players} and game{game_id} should be the same.")
                    await self.channel_layer.send( # front-end should send back the choice
                    channel_name,
                        {
                            "type":"setup",
                            "wonder_choice":[wonder[0], wonder[1]]
                        }
                    )
                


        # Broadcast message to group
        if data.get("type") == "message":
            await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": data['message'],
                "user": data['user']
            }
        )

        if data.get("start_game"):
            pass

    async def chat_message(self, event): # tar emot meddelanden från websocket-gruppen, backend, group_send, med "type" "chat_message"
        print(event)
        message = event["message"]
        user = event["user"]
        print("username is: ", user)
        await self.send(text_data=json.dumps({"message": message, "user":user}))

class LandingPageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "games_broadcast"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        # here contact redis and broadcast all games that are available

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    async def new_game(self, event):
        await self.send(text_data=json.dumps({
            "game_data": event['game_data']
        }))
