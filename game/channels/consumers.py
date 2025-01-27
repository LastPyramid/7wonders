from channels.generic.websocket import AsyncWebsocketConsumer
import json
from ..redis.async_redis_utils import add_player_to_game, remove_player_from_game, update_last_seen, add_player_websocket_group, get_player_channel_names, get_players, lock_game, insert_game_into_redis, pick_wonder, check_if_everyone_has_picked_a_wonder
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

        if data.get("type") == "state": # should send game-state back, like what?
            pass                        # cards, age? wonder, well see...

        if data.get("type") == "heartbeat":
            self.game_id = self.scope['url_route']['kwargs']['game_id'] # do we really need self.game_id? dont think so because its set in connet
            self.player_name = self.scope['url_route']['kwargs']['player_name']
            await update_last_seen(self.game_id, self.player_name)
            print(f"Received heartbeat from {self.channel_name}")

        if data.get("type") == "start":
            print("starting game...")
            game_id = self.scope['url_route']['kwargs']['game_id']
            result = await lock_game(game_id)
            if result == "failed":
                print("failed")
                await self.channel_layer.send(
                    self.channel_name,
                    {
                        "type": "chat_message",
                        "message": "could not start the game, someone else probably initiated the process before you."
                    }
                )
            elif result == "ok":
                print("ok1")
                channel_names = await get_player_channel_names(game_id)
                players = await get_players(game_id)
                if len(channel_names) != len(players):
                    print("amount of websockets connections should be equal to number of players") # add proper handeling later
                game = setup_game(players)
                await insert_game_into_redis(game_id, game)
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
                            "type":"send_wonder",
                            "message":[wonder[0].name, wonder[1].name]
                        }
                    )
        if data.get("type") == "pick_wonder":
            wonder = data.get("wonder")
            await pick_wonder(self.game_id, self.player_name, wonder)
            people_have_picked = await check_if_everyone_has_picked_a_wonder(self.game_id)
            if people_have_picked:
                game = people_have_picked
                channel_names = await get_player_channel_names(self.game_id)
                for player_name, channel_name in channel_names.items():
                    cards = []
                    for player in game.players:
                        if player.name == player_name:
                            for card in player.cards_to_pick_from:
                                cards.append(card.to_dict())
                    await self.channel_layer.send(
                    channel_name,
                        {
                            "type":"age_I_cards",
                            "message":cards
                        }
                    )
                # need to send shit to the front end
                print("everyone has picked now")
            else:
                print("apperently not everyone has picked")
            print("I'm speaking from the pick_wonder section")

        if data.get("type") == "setup":
            pass

        # Broadcast message to group
        if data.get("type") == "message":
            await self.channel_layer.group_send(# när man kör group_send, så kör man en funktion för alla
            self.group_name,                    # som prenumererar till gruppen
            {
                "type": "chat_message",
                "message": data['message'],
                "user": data['user']
            }
        )

        if data.get("start_game"):
            pass

    async def send_wonder(self, event):
        setup = event['message']
        await self.send(text_data=json.dumps({"setup":setup}))

    async def age_I_cards(self, event):
        cards = event['message']
        await self.send(text_data=json.dumps({"age_I_cards":cards}))


    async def chat_message(self, event):
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

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    async def new_game(self, event):
        await self.send(text_data=json.dumps({
            "game_data": event['game_data']
        }))
