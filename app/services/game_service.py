from __future__ import annotations

import random
import uuid
from typing import Dict, Optional

from app.core.seed_data import build_assets, build_board, build_decks
from app.models.schemas import (
    AirportTravelRequest,
    AssetDefinition,
    BasicActionResponse,
    BuyAssetRequest,
    Card,
    CourtRequest,
    CreateGameRequest,
    GameState,
    HQStoreChoiceRequest,
    IntelligenceRequest,
    InvestmentPosition,
    InvestmentRequest,
    LobbyRequest,
    MoveRequest,
    OwnedAsset,
    Player,
    UpgradeAssetRequest,
    WhiteHouseOptionRequest,
)


class GameService:
    def __init__(self) -> None:
        self.games: Dict[str, GameState] = {}
        self.assets: Dict[str, AssetDefinition] = build_assets()

    def create_game(self, req: CreateGameRequest) -> GameState:
        players = [Player(id=str(i + 1), name=name.strip()) for i, name in enumerate(req.player_names)]
        decks = build_decks()
        game = GameState(
            id=str(uuid.uuid4()),
            players=players,
            board=build_board(),
            decks={k: list(v) for k, v in decks.items()},
            discards={"main": [], "story": [], "media": []},
            max_rounds=req.max_rounds,
        )
        self.games[game.id] = game
        return game

    def get_game(self, game_id: str) -> GameState:
        return self.games[game_id]

    def start_game(self, game_id: str, seed: Optional[int] = None) -> GameState:
        game = self.get_game(game_id)
        if seed is not None:
            random.seed(seed)
        for deck_name in game.decks:
            random.shuffle(game.decks[deck_name])
        game.started = True
        self._log(game, "Game started.")
        return game

    def next_turn(self, game_id: str) -> GameState:
        game = self.get_game(game_id)
        game.turn_number += 1
        self._advance_current_player(game)
        player = self.current_player(game)
        if player.jail_turns_remaining > 0:
            player.jail_turns_remaining -= 1
            self._log(game, f"{player.name} is in jail and skips this turn.")
            self._advance_current_player(game)
        elif player.hospital_turns_remaining > 0:
            player.hospital_turns_remaining -= 1
            self._log(game, f"{player.name} is recovering in hospital and skips this turn.")
            self._advance_current_player(game)
        return game

    def move(self, game_id: str, req: MoveRequest) -> GameState:
        game = self.get_game(game_id)
        player = self.current_player(game)
        old_pos = player.position
        new_pos = (player.position + req.steps) % len(game.board)
        crossed_start = player.position + req.steps >= len(game.board)
        player.position = new_pos
        if crossed_start:
            self._apply_start_pass(game, player, req.pass_start_choice)
        self._log(game, f"{player.name} moved from {old_pos} to {new_pos}.")
        return game

    def resolve_square(self, game_id: str) -> GameState:
        game = self.get_game(game_id)
        player = self.current_player(game)
        square = game.board[player.position]

        if square.kind in {"property", "company_hq", "company_store"} and square.asset_id:
            self._resolve_asset_landing(game, player.id, square.asset_id)
        elif square.kind == "go_to_jail":
            self._send_to_jail(game, player)
        elif square.kind == "gangster_hood":
            self._send_to_hospital(game, player)
        elif square.kind == "black_market":
            player.money += game.config.black_market_money_gain
            player.reputation -= game.config.black_market_reputation_loss
            self._log(game, f"{player.name} used Black Market.")
        elif square.kind == "media_hub":
            self.draw_card(game_id, "media")
        self._update_presidency(game)
        return game

    def buy_asset(self, game_id: str, req: BuyAssetRequest) -> GameState:
        game = self.get_game(game_id)
        player = self.current_player(game)
        asset = self.assets[req.asset_id]
        if req.asset_id in game.ownership:
            raise ValueError("Asset already owned.")
        if asset.category == "b2g_hq" and player.reputation < game.config.b2g_unlock_reputation:
            raise ValueError("Need 100 reputation for B2G purchase.")
        if player.money < asset.base_cost:
            raise ValueError("Not enough money.")
        player.money -= asset.base_cost
        game.ownership[asset.id] = OwnedAsset(asset_id=asset.id, owner_id=player.id, level=1)
        self._log(game, f"{player.name} bought {asset.name}.")
        if asset.category == "b2c_hq":
            self._register_hq_conflicts(game, player.id, asset.id)
        return game

    def upgrade_asset(self, game_id: str, req: UpgradeAssetRequest) -> GameState:
        game = self.get_game(game_id)
        player = self.current_player(game)
        owned = game.ownership.get(req.asset_id)
        if not owned or owned.owner_id != player.id:
            raise ValueError("Asset not owned by current player.")
        if owned.level >= 3:
            raise ValueError("Asset already max level.")
        cost = self.assets[req.asset_id].base_cost
        if player.money < cost:
            raise ValueError("Not enough money to upgrade.")
        player.money -= cost
        owned.level += 1
        self._log(game, f"{player.name} upgraded {self.assets[req.asset_id].name} to L{owned.level}.")
        return game

    def draw_card(self, game_id: str, deck_name: str) -> Card:
        game = self.get_game(game_id)
        if not game.decks[deck_name]:
            game.decks[deck_name] = game.discards[deck_name]
            game.discards[deck_name] = []
            random.shuffle(game.decks[deck_name])
        card = game.decks[deck_name].pop(0)
        game.discards[deck_name].append(card)
        self._apply_card_effect(game, self.current_player(game), card)
        self._log(game, f"{self.current_player(game).name} drew {deck_name} card: {card.name}.")
        return card

    def white_house_option(self, game_id: str, req: WhiteHouseOptionRequest) -> GameState:
        game = self.get_game(game_id)
        player = self.current_player(game)
        if req.option == "improve_b2g":
            player.reputation += 10
            self._log(game, f"{player.name} improved B2G standing.")
        elif req.option == "run_for_president":
            self.run_for_president(game_id)
        elif req.option == "draw_media":
            self.draw_card(game_id, "media")
            player.reputation += 5
        self._update_presidency(game)
        return game

    def run_for_president(self, game_id: str) -> GameState:
        game = self.get_game(game_id)
        player = self.current_player(game)
        if player.reputation < game.config.president_min_reputation:
            raise ValueError("Need 100 reputation to run for President.")
        player.is_presidential_candidate = True
        candidates = [p for p in game.players if p.is_presidential_candidate and p.reputation >= game.config.president_min_reputation]
        if candidates:
            winner = sorted(candidates, key=lambda p: p.reputation, reverse=True)[0]
            game.president_player_id = winner.id
            self._log(game, f"{winner.name} became President.")
        return game

    def presidential_policy(self, game_id: str) -> GameState:
        game = self.get_game(game_id)
        if not game.president_player_id:
            raise ValueError("No active president")
        president = self._player_by_id(game, game.president_player_id)
        if president.policy_used_round == game.round_number:
            raise ValueError("Policy already used this round")
        for p in game.players:
            if p.id != president.id:
                p.money = max(0, p.money - game.config.president_policy_tax)
        president.money += game.config.president_policy_gain
        president.policy_used_round = game.round_number
        self._log(game, f"{president.name} executed a presidential policy.")
        return game

    def airport_travel(self, game_id: str, req: AirportTravelRequest) -> GameState:
        game = self.get_game(game_id)
        player = self.current_player(game)
        if req.use_fee:
            if player.money < game.config.airport_any_square_fee:
                raise ValueError("Not enough money for airport fee")
            player.money -= game.config.airport_any_square_fee
        else:
            if game.board[req.destination_square].kind != "airport":
                raise ValueError("Free airport travel only allows airport destinations")
        player.position = req.destination_square
        self._log(game, f"{player.name} traveled to square {req.destination_square} by airport.")
        return game

    def invest(self, game_id: str, req: InvestmentRequest) -> GameState:
        game = self.get_game(game_id)
        player = self.current_player(game)
        if player.money < req.amount:
            raise ValueError("Not enough money")
        player.money -= req.amount
        player.pending_investments.append(InvestmentPosition(amount=req.amount))
        self.draw_card(game_id, "media")
        self._log(game, f"{player.name} invested {req.amount}.")
        return game

    def lobby(self, game_id: str, req: LobbyRequest) -> GameState:
        game = self.get_game(game_id)
        player = self.current_player(game)
        if req.tier == "small":
            if player.money < game.config.lobbying_small_money:
                raise ValueError("Not enough money")
            player.money -= game.config.lobbying_small_money
            player.reputation += game.config.lobbying_small_rep
        else:
            if player.money < game.config.lobbying_large_money:
                raise ValueError("Not enough money")
            player.money -= game.config.lobbying_large_money
            player.reputation += game.config.lobbying_large_rep
        self._log(game, f"{player.name} used lobbying office ({req.tier}).")
        return game

    def court_action(self, game_id: str, req: CourtRequest) -> GameState:
        game = self.get_game(game_id)
        actor = self.current_player(game)
        target = self._player_by_id(game, req.target_player_id)
        value = self._most_valuable_asset_value(game, target.id)
        payout = max(60, value // 2)
        target.money = max(0, target.money - payout)
        actor.money += payout
        self._log(game, f"{actor.name} sued {target.name} for {payout}.")
        return game

    def intel_action(self, game_id: str, req: IntelligenceRequest) -> GameState:
        game = self.get_game(game_id)
        actor = self.current_player(game)
        target = self._player_by_id(game, req.target_player_id)
        money_delta = 80
        rep_delta = 12
        target.money = max(0, target.money - money_delta)
        target.reputation -= rep_delta
        actor.money += money_delta
        actor.reputation += rep_delta
        self._log(game, f"{actor.name} used intelligence action against {target.name}.")
        self._update_presidency(game)
        return game

    def resolve_hq_store_choice(self, game_id: str, req: HQStoreChoiceRequest) -> GameState:
        game = self.get_game(game_id)
        hq_owner = self.current_player(game)
        store_owned = game.ownership.get(req.store_asset_id)
        if not store_owned:
            raise ValueError("Store is not currently owned")
        store_asset = self.assets[req.store_asset_id]
        if req.choice == "buyout":
            valuation = int(store_asset.base_cost * store_owned.level)
            buy_price = int(valuation * game.config.hq_store_buyout_multiplier)
            if hq_owner.money < buy_price:
                raise ValueError("Not enough money for buyout")
            seller = self._player_by_id(game, store_owned.owner_id)
            hq_owner.money -= buy_price
            seller.money += buy_price
            store_owned.owner_id = hq_owner.id
            game.hq_store_revenue_share.pop(req.store_asset_id, None)
            self._log(game, f"{hq_owner.name} bought out {store_asset.name} for {buy_price}.")
        else:
            game.hq_store_revenue_share[req.store_asset_id] = hq_owner.id
            self._log(game, f"{hq_owner.name} set revenue share on {store_asset.name}.")
        return game

    def _register_hq_conflicts(self, game: GameState, hq_owner_id: str, hq_id: str) -> None:
        for asset in self.assets.values():
            if asset.parent_hq_id == hq_id and asset.id in game.ownership:
                if game.ownership[asset.id].owner_id != hq_owner_id:
                    self._log(
                        game,
                        f"HQ conflict: choose buyout or revenue-share for {asset.name} via resolve-hq-store-choice endpoint.",
                    )

    def _resolve_asset_landing(self, game: GameState, player_id: str, asset_id: str) -> None:
        owned = game.ownership.get(asset_id)
        if not owned or owned.owner_id == player_id:
            return
        tenant = self._player_by_id(game, player_id)
        owner = self._player_by_id(game, owned.owner_id)
        rent = self._asset_income(asset_id, owned.level)
        paid = min(tenant.money, rent)
        tenant.money -= paid
        owner.money += paid
        hq_share_owner_id = game.hq_store_revenue_share.get(asset_id)
        if hq_share_owner_id and hq_share_owner_id != owner.id:
            share_owner = self._player_by_id(game, hq_share_owner_id)
            share = int(rent * game.config.hq_store_round_share)
            owner.money -= share
            share_owner.money += share
        self._log(game, f"{tenant.name} paid {paid} to {owner.name} for {self.assets[asset_id].name}.")

    def _apply_start_pass(self, game: GameState, player: Player, choice: str) -> None:
        if choice == "money":
            player.money += game.config.pass_start_money
        else:
            player.reputation += game.config.pass_start_reputation
        player.loops_completed += 1
        if player.id not in game.round_passed_start:
            game.round_passed_start.append(player.id)
        self._log(game, f"{player.name} passed Start and chose {choice}.")
        if len(game.round_passed_start) == len(game.players):
            self._process_round_end(game)

    def _process_round_end(self, game: GameState) -> None:
        self._log(game, f"Round {game.round_number} completed. Processing payouts.")
        self._resolve_investments(game)
        self._apply_b2b_payouts(game)
        self._apply_b2g_payouts(game)
        game.round_number += 1
        game.round_passed_start = []
        if game.round_number > game.max_rounds:
            game.ended = True

    def _resolve_investments(self, game: GameState) -> None:
        for player in game.players:
            retained = []
            for inv in player.pending_investments:
                inv.rounds_remaining -= 1
                if inv.rounds_remaining <= 0:
                    if random.random() <= game.config.investment_success_probability:
                        player.money += inv.amount * 2
                        self._log(game, f"{player.name} investment returned 2x.")
                    else:
                        self._log(game, f"{player.name} investment failed.")
                else:
                    retained.append(inv)
            player.pending_investments = retained

    def _apply_b2b_payouts(self, game: GameState) -> None:
        # AWS
        aws = game.ownership.get("hq_aws")
        if aws:
            aws_owner = self._player_by_id(game, aws.owner_id)
            b2c_hq_owned = sum(1 for a in game.ownership.values() if self.assets[a.asset_id].category == "b2c_hq")
            b2c_store_owned = sum(1 for a in game.ownership.values() if self.assets[a.asset_id].category == "b2c_store")
            aws_owner.money += b2c_hq_owned * game.config.b2b_aws_per_b2c_hq + b2c_store_owned * game.config.b2b_aws_per_b2c_store

        siemens = game.ownership.get("hq_siemens")
        if siemens:
            siemens_owner = self._player_by_id(game, siemens.owner_id)
            payout = 0
            for owned in game.ownership.values():
                if self.assets[owned.asset_id].category == "property":
                    payout += {1: game.config.b2b_siemens_l1, 2: game.config.b2b_siemens_l2, 3: game.config.b2b_siemens_l3}[owned.level]
            siemens_owner.money += payout

    def _apply_b2g_payouts(self, game: GameState) -> None:
        for aid, base in (("hq_spacex_gov", game.config.b2g_spacex_base), ("hq_palantir_gov", game.config.b2g_palantir_base)):
            owned = game.ownership.get(aid)
            if not owned:
                continue
            owner = self._player_by_id(game, owned.owner_id)
            payout = int(base * (1 + (owned.level - 1) * game.config.b2g_level_multiplier))
            if aid == "hq_palantir_gov":
                payout += (len(game.players) - 1) * game.config.b2g_palantir_per_opponent
            if game.president_player_id == owner.id:
                payout = int(payout * game.config.president_b2g_multiplier)
            owner.money += payout

    def _apply_card_effect(self, game: GameState, player: Player, card: Card) -> None:
        eff = card.effect
        player.money += eff.money
        player.reputation += eff.reputation
        if eff.move > 0:
            self.move(game.id, MoveRequest(steps=eff.move, pass_start_choice="money"))
        if eff.goto_square is not None:
            player.position = eff.goto_square
        if eff.go_to_jail:
            self._send_to_jail(game, player)
        if eff.send_hospital:
            self._send_to_hospital(game, player)
        if eff.trigger_story:
            self.draw_card(game.id, "story")
        if eff.trigger_media:
            self.draw_card(game.id, "media")
        self._update_presidency(game)

    def _send_to_jail(self, game: GameState, player: Player) -> None:
        player.position = next(s.index for s in game.board if s.kind == "jail")
        player.jail_turns_remaining = game.config.jail_default_turns
        self._log(game, f"{player.name} was sent to Jail.")

    def _send_to_hospital(self, game: GameState, player: Player) -> None:
        player.position = next(s.index for s in game.board if s.kind == "hospital")
        player.hospital_turns_remaining = game.config.hospital_injury_turns
        self._log(game, f"{player.name} was sent to Hospital.")

    def _update_presidency(self, game: GameState) -> None:
        if not game.president_player_id:
            return
        president = self._player_by_id(game, game.president_player_id)
        if president.reputation < game.config.president_kick_threshold or president.reputation < game.config.president_min_reputation:
            self._log(game, f"{president.name} lost presidency due to low reputation.")
            game.president_player_id = None

    def _most_valuable_asset_value(self, game: GameState, player_id: str) -> int:
        values = [self.assets[a.asset_id].base_cost * a.level for a in game.ownership.values() if a.owner_id == player_id]
        return max(values) if values else 120

    def _asset_income(self, asset_id: str, level: int) -> int:
        x = self.assets[asset_id].base_cost
        return {1: x // 2, 2: x, 3: int(x * 1.5)}[level]

    def _advance_current_player(self, game: GameState) -> None:
        game.current_player_index = (game.current_player_index + 1) % len(game.players)

    def _player_by_id(self, game: GameState, player_id: str) -> Player:
        return next(p for p in game.players if p.id == player_id)

    def current_player(self, game: GameState) -> Player:
        return game.players[game.current_player_index]

    def _log(self, game: GameState, message: str) -> None:
        game.action_log.append(message)


service = GameService()
