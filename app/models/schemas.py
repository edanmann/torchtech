from __future__ import annotations

from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field


SquareKind = Literal[
    "start",
    "property",
    "free_land",
    "airport",
    "media_hub",
    "investment_hub",
    "innovation_hub",
    "black_market",
    "court",
    "go_to_jail",
    "jail",
    "white_house",
    "gangster_hood",
    "intelligence_agency",
    "lobbying_office",
    "hospital",
    "company_hq",
    "company_store",
]

DeckType = Literal["main", "story", "media"]


class CardEffect(BaseModel):
    money: int = 0
    reputation: int = 0
    move: int = 0
    goto_square: Optional[int] = None
    go_to_jail: bool = False
    send_hospital: bool = False
    trigger_story: bool = False
    trigger_media: bool = False


class Card(BaseModel):
    id: str
    deck: DeckType
    name: str
    description: str
    effect: CardEffect


class Square(BaseModel):
    index: int
    name: str
    kind: SquareKind
    asset_id: Optional[str] = None


class AssetDefinition(BaseModel):
    id: str
    name: str
    category: Literal["property", "b2c_hq", "b2c_store", "b2b_hq", "b2g_hq"]
    base_cost: int
    parent_hq_id: Optional[str] = None


class OwnedAsset(BaseModel):
    asset_id: str
    owner_id: str
    level: int = 1


class InvestmentPosition(BaseModel):
    amount: int
    rounds_remaining: int = 1


class Player(BaseModel):
    id: str
    name: str
    money: int = 1500
    reputation: int = 0
    position: int = 0
    loops_completed: int = 0
    jail_turns_remaining: int = 0
    hospital_turns_remaining: int = 0
    is_presidential_candidate: bool = False
    policy_used_round: int = 0
    pending_investments: List[InvestmentPosition] = Field(default_factory=list)

    @property
    def power_score(self) -> int:
        return self.money + self.reputation


class GameConfig(BaseModel):
    pass_start_money: int = 200
    pass_start_reputation: int = 50
    airport_any_square_fee: int = 120
    jail_default_turns: int = 1
    hospital_injury_turns: int = 2
    black_market_money_gain: int = 180
    black_market_reputation_loss: int = 25
    lobbying_small_money: int = 100
    lobbying_small_rep: int = 10
    lobbying_large_money: int = 500
    lobbying_large_rep: int = 60
    investment_success_probability: float = 0.6
    b2b_aws_per_b2c_hq: int = 20
    b2b_aws_per_b2c_store: int = 10
    b2b_siemens_l1: int = 5
    b2b_siemens_l2: int = 10
    b2b_siemens_l3: int = 15
    b2g_unlock_reputation: int = 100
    b2g_spacex_base: int = 120
    b2g_palantir_base: int = 100
    b2g_palantir_per_opponent: int = 20
    b2g_level_multiplier: float = 0.5
    president_min_reputation: int = 100
    president_kick_threshold: int = -500
    president_b2g_multiplier: float = 1.2
    president_policy_gain: int = 50
    president_policy_tax: int = 25
    hq_store_buyout_multiplier: float = 1.5
    hq_store_round_share: float = 0.25


class GameState(BaseModel):
    id: str
    started: bool = False
    ended: bool = False
    max_rounds: int = 12
    board: List[Square]
    players: List[Player]
    current_player_index: int = 0
    turn_number: int = 1
    round_number: int = 1
    round_passed_start: List[str] = Field(default_factory=list)
    president_player_id: Optional[str] = None
    ownership: Dict[str, OwnedAsset] = Field(default_factory=dict)
    hq_store_revenue_share: Dict[str, str] = Field(default_factory=dict)
    decks: Dict[str, List[Card]] = Field(default_factory=dict)
    discards: Dict[str, List[Card]] = Field(default_factory=dict)
    action_log: List[str] = Field(default_factory=list)
    config: GameConfig = Field(default_factory=GameConfig)


class CreateGameRequest(BaseModel):
    player_names: List[str] = Field(min_length=2, max_length=4)
    max_rounds: int = 12


class StartGameRequest(BaseModel):
    shuffle_seed: Optional[int] = None


class MoveRequest(BaseModel):
    steps: int = Field(ge=1, le=12)
    pass_start_choice: Literal["money", "reputation"] = "money"


class BuyAssetRequest(BaseModel):
    asset_id: str


class UpgradeAssetRequest(BaseModel):
    asset_id: str


class WhiteHouseOptionRequest(BaseModel):
    option: Literal["improve_b2g", "run_for_president", "draw_media"]


class AirportTravelRequest(BaseModel):
    destination_square: int = Field(ge=0, le=51)
    use_fee: bool = False


class InvestmentRequest(BaseModel):
    amount: int = Field(gt=0)


class LobbyRequest(BaseModel):
    tier: Literal["small", "large"]


class CourtRequest(BaseModel):
    target_player_id: str


class IntelligenceRequest(BaseModel):
    target_player_id: str


class HQStoreChoiceRequest(BaseModel):
    store_asset_id: str
    choice: Literal["buyout", "revenue_share"]


class BasicActionResponse(BaseModel):
    message: str
    game: GameState
