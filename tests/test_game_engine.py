from app.models.schemas import BuyAssetRequest, CreateGameRequest, HQStoreChoiceRequest, MoveRequest, UpgradeAssetRequest
from app.services.game_service import GameService


def fresh_game() -> tuple[GameService, str]:
    svc = GameService()
    game = svc.create_game(CreateGameRequest(player_names=["A", "B"], max_rounds=5))
    svc.start_game(game.id, seed=1)
    return svc, game.id


def test_passing_start_reward_money():
    svc, gid = fresh_game()
    game = svc.get_game(gid)
    p = game.players[0]
    p.position = 50
    base = p.money
    svc.move(gid, MoveRequest(steps=3, pass_start_choice="money"))
    assert p.money == base + 200


def test_property_upgrade_cost_and_level():
    svc, gid = fresh_game()
    game = svc.get_game(gid)
    p = game.players[0]
    svc.buy_asset(gid, BuyAssetRequest(asset_id="prop_delhi_slum_house"))
    before = p.money
    svc.upgrade_asset(gid, UpgradeAssetRequest(asset_id="prop_delhi_slum_house"))
    assert game.ownership["prop_delhi_slum_house"].level == 2
    assert p.money == before - 60


def test_hq_store_buyout_flow():
    svc, gid = fresh_game()
    game = svc.get_game(gid)
    p1, p2 = game.players
    svc.buy_asset(gid, BuyAssetRequest(asset_id="store_xcom"))
    svc.next_turn(gid)
    svc.buy_asset(gid, BuyAssetRequest(asset_id="hq_tesla"))
    val = 130
    buy_price = int(val * 1.5)
    before_p1, before_p2 = p1.money, p2.money
    svc.resolve_hq_store_choice(gid, HQStoreChoiceRequest(store_asset_id="store_xcom", choice="buyout"))
    assert game.ownership["store_xcom"].owner_id == p2.id
    assert p2.money == before_p2 - buy_price
    assert p1.money == before_p1 + buy_price


def test_presidency_logic():
    svc, gid = fresh_game()
    game = svc.get_game(gid)
    p = game.players[0]
    p.reputation = 120
    svc.run_for_president(gid)
    assert game.president_player_id == p.id
    p.reputation = 80
    svc.resolve_square(gid)
    assert game.president_player_id is None


def test_jail_hospital_logic():
    svc, gid = fresh_game()
    game = svc.get_game(gid)
    p = game.players[0]
    p.position = 10
    svc.resolve_square(gid)
    assert p.jail_turns_remaining >= 1
    p.position = 47
    svc.resolve_square(gid)
    assert p.hospital_turns_remaining == 2


def test_round_end_b2b_payouts():
    svc, gid = fresh_game()
    game = svc.get_game(gid)
    p1, p2 = game.players
    svc.buy_asset(gid, BuyAssetRequest(asset_id="hq_aws"))
    svc.next_turn(gid)
    svc.buy_asset(gid, BuyAssetRequest(asset_id="hq_tesla"))
    p1.position = 51
    p2.position = 51
    before = p1.money
    svc.move(gid, MoveRequest(steps=2, pass_start_choice="money"))
    svc.next_turn(gid)
    svc.move(gid, MoveRequest(steps=2, pass_start_choice="money"))
    assert game.round_number == 2
    assert p1.money > before


def test_main_card_resolution_changes_stats():
    svc, gid = fresh_game()
    game = svc.get_game(gid)
    p = game.players[0]
    m, r = p.money, p.reputation
    svc.draw_card(gid, "main")
    assert p.money != m or p.reputation != r
