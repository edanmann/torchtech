from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    AirportTravelRequest,
    BasicActionResponse,
    BuyAssetRequest,
    CourtRequest,
    CreateGameRequest,
    HQStoreChoiceRequest,
    IntelligenceRequest,
    InvestmentRequest,
    LobbyRequest,
    MoveRequest,
    StartGameRequest,
    UpgradeAssetRequest,
    WhiteHouseOptionRequest,
)
from app.services.game_service import service

router = APIRouter(prefix="/games", tags=["games"])


def _handle(action):
    try:
        return action()
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not found")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("")
def create_game(req: CreateGameRequest):
    return _handle(lambda: service.create_game(req))


@router.get("/{game_id}")
def get_game(game_id: str):
    return _handle(lambda: service.get_game(game_id))


@router.post("/{game_id}/start")
def start_game(game_id: str, req: StartGameRequest):
    return _handle(lambda: service.start_game(game_id, req.shuffle_seed))


@router.post("/{game_id}/next-turn")
def next_turn(game_id: str):
    game = _handle(lambda: service.next_turn(game_id))
    return BasicActionResponse(message="Turn advanced", game=game)


@router.post("/{game_id}/move")
def move(game_id: str, req: MoveRequest):
    game = _handle(lambda: service.move(game_id, req))
    return BasicActionResponse(message="Player moved", game=game)


@router.post("/{game_id}/resolve-square")
def resolve_square(game_id: str):
    game = _handle(lambda: service.resolve_square(game_id))
    return BasicActionResponse(message="Square resolved", game=game)


@router.post("/{game_id}/buy-property")
def buy_property(game_id: str, req: BuyAssetRequest):
    game = _handle(lambda: service.buy_asset(game_id, req))
    return BasicActionResponse(message="Asset purchased", game=game)


@router.post("/{game_id}/buy-hq")
def buy_hq(game_id: str, req: BuyAssetRequest):
    game = _handle(lambda: service.buy_asset(game_id, req))
    return BasicActionResponse(message="HQ purchased", game=game)


@router.post("/{game_id}/upgrade-asset")
def upgrade_asset(game_id: str, req: UpgradeAssetRequest):
    game = _handle(lambda: service.upgrade_asset(game_id, req))
    return BasicActionResponse(message="Asset upgraded", game=game)


@router.post("/{game_id}/draw-main-card")
def draw_main_card(game_id: str):
    card = _handle(lambda: service.draw_card(game_id, "main"))
    return {"message": "Main card drawn", "card": card, "game": service.get_game(game_id)}


@router.post("/{game_id}/draw-media-card")
def draw_media_card(game_id: str):
    card = _handle(lambda: service.draw_card(game_id, "media"))
    return {"message": "Media card drawn", "card": card, "game": service.get_game(game_id)}


@router.post("/{game_id}/draw-story-card")
def draw_story_card(game_id: str):
    card = _handle(lambda: service.draw_card(game_id, "story"))
    return {"message": "Story card drawn", "card": card, "game": service.get_game(game_id)}


@router.post("/{game_id}/run-for-president")
def run_for_president(game_id: str):
    game = _handle(lambda: service.run_for_president(game_id))
    return BasicActionResponse(message="Presidential candidacy submitted", game=game)


@router.post("/{game_id}/presidential-policy")
def presidential_policy(game_id: str):
    game = _handle(lambda: service.presidential_policy(game_id))
    return BasicActionResponse(message="Policy executed", game=game)


@router.post("/{game_id}/choose-white-house-option")
def choose_white_house_option(game_id: str, req: WhiteHouseOptionRequest):
    game = _handle(lambda: service.white_house_option(game_id, req))
    return BasicActionResponse(message="White House option resolved", game=game)


@router.post("/{game_id}/lobby")
def lobby(game_id: str, req: LobbyRequest):
    game = _handle(lambda: service.lobby(game_id, req))
    return BasicActionResponse(message="Lobby action resolved", game=game)


@router.post("/{game_id}/airport-travel")
def airport_travel(game_id: str, req: AirportTravelRequest):
    game = _handle(lambda: service.airport_travel(game_id, req))
    return BasicActionResponse(message="Airport travel resolved", game=game)


@router.post("/{game_id}/investment")
def investment(game_id: str, req: InvestmentRequest):
    game = _handle(lambda: service.invest(game_id, req))
    return BasicActionResponse(message="Investment placed", game=game)


@router.post("/{game_id}/resolve-hq-store-choice")
def resolve_hq_store_choice(game_id: str, req: HQStoreChoiceRequest):
    game = _handle(lambda: service.resolve_hq_store_choice(game_id, req))
    return BasicActionResponse(message="HQ/store choice resolved", game=game)


@router.post("/{game_id}/court")
def court(game_id: str, req: CourtRequest):
    game = _handle(lambda: service.court_action(game_id, req))
    return BasicActionResponse(message="Court action resolved", game=game)


@router.post("/{game_id}/intelligence")
def intelligence(game_id: str, req: IntelligenceRequest):
    game = _handle(lambda: service.intel_action(game_id, req))
    return BasicActionResponse(message="Intelligence action resolved", game=game)
