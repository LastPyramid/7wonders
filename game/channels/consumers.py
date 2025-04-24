import json
from ..game.game_logic import setup_game
from ..redis.setups import setup_next_turn, setup_next_age
from channels.generic.websocket import AsyncWebsocketConsumer
from ..redis.async_redis_utils import (
    add_player_to_game, remove_player_from_game, update_last_seen,
    add_player_websocket_group, lock_game, insert_game_into_redis, pick_wonder, 
    pick_card, sell_card, build_wonder_stage, insert_player_choice_into_game, player_can_pick_card)
from ..redis.get import (
    get_player_cards, get_player_resources, get_players,
    get_player_state, get_player_ids,get_player_decisions, get_player_channel_names)
from ..redis.check import (
    check_if_everyone_has_picked_a_wonder, check_if_everyone_have_made_a_picking_decision,
    check_if_player_can_build_wonder_stage)

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
            pass

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

    async def setup_new_age(self, game_id):
        channel_names = await get_player_channel_names(self.game_id)
        game = await setup_next_age(game_id)
        await self.send_cards(channel_names, game)

    async def get_other_players_resources(self, game_id):
        channel_names = await get_player_channel_names(self.game_id)
        game = await setup_next_age(game_id)
        await self.send_cards(channel_names, game)

    async def setup_new_turn(self, game_id):
        channel_names = await get_player_channel_names(self.game_id)
        game = await setup_next_turn(game_id)
        print("in setup_new_turn")
        await self.send_cards(channel_names, game)

    async def send_cards(self, channel_names, game):
        age = game.age * "I"
        for player_name, channel_name in channel_names.items():
            cards = []
            for player in game.players:
                if player.name == player_name:
                    for card in player.cards_to_pick_from:
                        cards.append(card.to_dict())
            print(f"channel_name = {channel_name}, player_name = {player_name}, age = {age}")
            await self.channel_layer.send(
            channel_name,
                {
                    "type":f"age_{age}_cards",
                    "turn":f"{game.turn}",
                    "message":cards
                }
            )

    async def receive(self, text_data): # tar emot meddelanden från 1 websocket, frontend
        data = json.loads(text_data)

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
                print(game)
                channel_names = await get_player_channel_names(self.game_id)
                await self.send_cards(channel_names, game)
                print("everyone has picked now")
            else:
                print("apperently not everyone has picked")

        if data.get("type") == "get_cards":
            await self.send_player_cards()

        if data.get("type") == "get_player_state":
            player_id = data.get("player_id")
            await self.send_player_state(player_id)

        if data.get("type") == "get_player_ids":
            print("in consumers.py get_player_ids")
            await self.send_player_ids()


        if data.get("type") == "get_resources":
            print("getting resources!")
            resources = await get_player_resources(self.player_name, self.game_id)
            print(f"sending resources: {resources}")
            await self.send(text_data=json.dumps({"resources": resources}))

        if data.get("type") == "build_wonder":
            print("building wonder!")
            player_can_build_wonder_stage = await check_if_player_can_build_wonder_stage(self.player_name, self.game_id)
            if player_can_build_wonder_stage:
                stage = player_can_build_wonder_stage
                choice = {"build_wonder":stage}
                await insert_player_choice_into_game(self.player_name, self.game_id, choice)
                await self.send(text_data=json.dumps({"build_wonder": {"status":"success", "stage":stage}}))
            else:
                await self.send(text_data=json.dumps({"build_wonder": {"status":"fail"}}))
            await self.check_if_everyone_has_picked()

        if data.get("type") == "sell_card":
            card_name = data.get("name")
            choice = {"sell_card":card_name}
            await insert_player_choice_into_game(self.player_name, self.game_id, choice)
            await self.send(text_data=json.dumps({"sell_card": {"status":"success"}}))
            await self.check_if_everyone_has_picked()

        if data.get("type") == "pick_card":
            card_name = data.get("name")
            if await player_can_pick_card(self.player_name, self.game_id, card_name):
                choice = {"pick_card":card_name}
                await insert_player_choice_into_game(self.player_name, self.game_id, choice)
                await self.send(text_data=json.dumps({"pick_card": {"status":"success"}}))
            else:
                await self.send(text_data=json.dumps({"pick_card": {"status":"fail"}, "message": "Could not pick card"}))
            await self.check_if_everyone_has_picked()

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

    async def send_players_their_resources(self):
        channel_names = await get_player_channel_names(self.game_id)
        for player_name, channel_name in channel_names.items():
            resources = await get_player_resources(player_name, self.game_id)
            await self.channel_layer.send(
            channel_name,
                {
                    "type":"send_resources",
                    "resources":resources
                }
            )

    async def check_if_everyone_has_picked(self):
        everyone_has_picked = await check_if_everyone_have_made_a_picking_decision(self.game_id)
        if everyone_has_picked:
            print("Everyone has picked!")
            game = everyone_has_picked
            await self.resolve_decisions()
            await self.send_players_their_resources()
            if game.turn == 6:
                print("last turn")
                await self.setup_new_age(self.game_id)
            else:
                print("prepping next turn")
                await self.setup_new_turn(self.game_id)
        else:
            print("Waiting for everyone to pick a card")

    async def resolve_decisions(self):
        print("In resolve_decisions")
        player_decisions = await get_player_decisions(self.game_id)
        for player, choice in player_decisions.items():
            print(f"August Remove this: player: {player}")
            for event, item in choice.items():
                if event == "pick_card":
                    player_could_pick = await pick_card(self.game_id, item, player)
                    if player_could_pick:
                        await self.send_player_cards()
                    else:
                        raise Exception(f"Something went really wrong, could not pick card for {player}")
                elif event == "sell_card":
                    await sell_card(player, self.game_id, item)
                elif event == "build_wonder":
                    await build_wonder_stage(self.game_id, player, item)

    async def send_player_cards(self):
        cards = await get_player_cards(self.player_name, self.game_id)
        if cards == []:
            await self.send(text_data=json.dumps({"get_cards":{"status":"empty", "message": "you have no cards"}}))
        else:
            await self.send(text_data=json.dumps({"get_cards":{"status":"ok", "cards":cards}}))

    async def send_wonder(self, event):
        setup = event['message']
        await self.send(text_data=json.dumps({"setup":setup}))

    async def send_resources(self, event):
        resources = event["resources"]
        await self.send(text_data=json.dumps({"resources": resources}))

    async def send_player_state(self, player_id):
        resources, wonder, cards = await get_player_state(player_id, self.game_id)
        await self.send(text_data=json.dumps({"player_state":{"resources":resources, "wonder": wonder, "cards": cards}}))

    async def send_player_ids(self):
        player_ids, player_id, left_player_id, right_player_id = await get_player_ids(self.player_name, self.game_id)
        print("Sending Player Ids!")
        await self.send(text_data=json.dumps({"player_ids": player_ids,
                                              "player_id": player_id,
                                              "left_player_id":left_player_id,
                                              "right_player_id": right_player_id}))

    async def age_I_cards(self, event):
        cards = event['message']
        await self.send(text_data=json.dumps({"age_I_cards":cards}))

    async def chat_message(self, event):
        print(event)
        message = event["message"]
        user = event["user"]
        print("username is: ", user)
        await self.send(text_data=json.dumps({"message": message, "user":user}))

class LandingPageConsumer(AsyncWebsocketConsumer): # rename this
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