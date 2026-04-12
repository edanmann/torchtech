from __future__ import annotations

from typing import Dict, List
from app.models.schemas import AssetDefinition, Card, CardEffect, Square


PROPERTY_DATA = [
    ("prop_nyc_penthouse", "New York City Penthouse", 350),
    ("prop_zurich_apartment", "Zürich City Apartment Complex", 220),
    ("prop_geneva_mansion", "Geneva Mansion", 400),
    ("prop_mumbai_apartment", "Mumbai Apartment", 230),
    ("prop_barcelona_camp_nou", "Barcelona, Camp Nou", 260),
    ("prop_silicon_valley_apartment", "Silicon Valley, California Apartment", 140),
    ("prop_london_house", "London, House", 220),
    ("prop_delhi_slum_house", "Slum house in Delhi", 60),
    ("prop_marrakesh_house", "Marrakesch, Morocco House", 140),
    ("prop_cairo_apartment", "Cairo, Egypt Apartment", 100),
    ("prop_sydney_apartment", "Sydney, Australia, Apartment", 180),
    ("prop_cape_town_mansion", "Cape Town Mansion", 300),
    ("prop_burj_penthouse", "Burj Khalifa Penthouse", 300),
]

COMPANY_DATA = [
    ("hq_tesla", "Tesla HQ", "b2c_hq", 400, None),
    ("store_xcom", "X.com store", "b2c_store", 130, "hq_tesla"),
    ("store_melon_mask", "Melon Mask Super Fan Shop", "b2c_store", 110, "hq_tesla"),
    ("hq_apple", "Apple HQ", "b2c_hq", 420, None),
    ("store_apple_mall", "Apple Store Mall", "b2c_store", 140, "hq_apple"),
    ("store_apple_downtown", "Apple Store Downtown", "b2c_store", 130, "hq_apple"),
    ("hq_mcd", "McDonalds HQ", "b2c_hq", 350, None),
    ("store_mcd_city", "McDonalds Franchise City", "b2c_store", 110, "hq_mcd"),
    ("store_mcd_highway", "McDonalds Franchise Highway", "b2c_store", 100, "hq_mcd"),
    ("hq_aws", "AWS Cloud Infrastructure HQ", "b2b_hq", 550, None),
    ("hq_siemens", "Siemens Industrial Systems HQ", "b2b_hq", 530, None),
    ("hq_spacex_gov", "SpaceX Government Contracts HQ", "b2g_hq", 580, None),
    ("hq_palantir_gov", "Palantir Intelligence Systems HQ", "b2g_hq", 520, None),
]


def build_assets() -> Dict[str, AssetDefinition]:
    assets: Dict[str, AssetDefinition] = {}
    for asset_id, name, price in PROPERTY_DATA:
        assets[asset_id] = AssetDefinition(id=asset_id, name=name, category="property", base_cost=price)
    for asset_id, name, category, price, parent_hq_id in COMPANY_DATA:
        assets[asset_id] = AssetDefinition(
            id=asset_id,
            name=name,
            category=category,
            base_cost=price,
            parent_hq_id=parent_hq_id,
        )
    return assets


def build_board() -> List[Square]:
    # 52-square board with all named assets; count conflict in source resolved in assumptions file.
    names: List[Square] = [
        Square(index=0, name="Start", kind="start"),
        Square(index=1, name="New York City Penthouse", kind="property", asset_id="prop_nyc_penthouse"),
        Square(index=2, name="Airport North", kind="airport"),
        Square(index=3, name="Tesla HQ", kind="company_hq", asset_id="hq_tesla"),
        Square(index=4, name="X.com store", kind="company_store", asset_id="store_xcom"),
        Square(index=5, name="Free Land A", kind="free_land"),
        Square(index=6, name="Media Hub Alpha", kind="media_hub"),
        Square(index=7, name="Zürich City Apartment Complex", kind="property", asset_id="prop_zurich_apartment"),
        Square(index=8, name="Apple HQ", kind="company_hq", asset_id="hq_apple"),
        Square(index=9, name="Apple Store Mall", kind="company_store", asset_id="store_apple_mall"),
        Square(index=10, name="Go To Jail", kind="go_to_jail"),
        Square(index=11, name="Geneva Mansion", kind="property", asset_id="prop_geneva_mansion"),
        Square(index=12, name="Airport East", kind="airport"),
        Square(index=13, name="AWS Cloud Infrastructure HQ", kind="company_hq", asset_id="hq_aws"),
        Square(index=14, name="Investment Hub", kind="investment_hub"),
        Square(index=15, name="Free Land B", kind="free_land"),
        Square(index=16, name="Mumbai Apartment", kind="property", asset_id="prop_mumbai_apartment"),
        Square(index=17, name="McDonalds HQ", kind="company_hq", asset_id="hq_mcd"),
        Square(index=18, name="McDonalds Franchise City", kind="company_store", asset_id="store_mcd_city"),
        Square(index=19, name="Jail", kind="jail"),
        Square(index=20, name="Barcelona, Camp Nou", kind="property", asset_id="prop_barcelona_camp_nou"),
        Square(index=21, name="Airport South", kind="airport"),
        Square(index=22, name="Siemens Industrial Systems HQ", kind="company_hq", asset_id="hq_siemens"),
        Square(index=23, name="Innovation Hub", kind="innovation_hub"),
        Square(index=24, name="Free Land C", kind="free_land"),
        Square(index=25, name="Silicon Valley, California Apartment", kind="property", asset_id="prop_silicon_valley_apartment"),
        Square(index=26, name="Apple Store Downtown", kind="company_store", asset_id="store_apple_downtown"),
        Square(index=27, name="Media Hub Beta", kind="media_hub"),
        Square(index=28, name="London, House", kind="property", asset_id="prop_london_house"),
        Square(index=29, name="Airport West", kind="airport"),
        Square(index=30, name="SpaceX Government Contracts HQ", kind="company_hq", asset_id="hq_spacex_gov"),
        Square(index=31, name="White House", kind="white_house"),
        Square(index=32, name="Free Land D", kind="free_land"),
        Square(index=33, name="Slum house in Delhi", kind="property", asset_id="prop_delhi_slum_house"),
        Square(index=34, name="Melon Mask Super Fan Shop", kind="company_store", asset_id="store_melon_mask"),
        Square(index=35, name="Court", kind="court"),
        Square(index=36, name="Marrakesch, Morocco House", kind="property", asset_id="prop_marrakesh_house"),
        Square(index=37, name="Airport Prime", kind="airport"),
        Square(index=38, name="Palantir Intelligence Systems HQ", kind="company_hq", asset_id="hq_palantir_gov"),
        Square(index=39, name="Lobbying Office", kind="lobbying_office"),
        Square(index=40, name="Free Land E", kind="free_land"),
        Square(index=41, name="Cairo, Egypt Apartment", kind="property", asset_id="prop_cairo_apartment"),
        Square(index=42, name="McDonalds Franchise Highway", kind="company_store", asset_id="store_mcd_highway"),
        Square(index=43, name="Intelligence Agency", kind="intelligence_agency"),
        Square(index=44, name="Sydney, Australia, Apartment", kind="property", asset_id="prop_sydney_apartment"),
        Square(index=45, name="Airport Gateway", kind="airport"),
        Square(index=46, name="Black Market", kind="black_market"),
        Square(index=47, name="Gangster Hood", kind="gangster_hood"),
        Square(index=48, name="Free Land F", kind="free_land"),
        Square(index=49, name="Cape Town Mansion", kind="property", asset_id="prop_cape_town_mansion"),
        Square(index=50, name="Hospital", kind="hospital"),
        Square(index=51, name="Burj Khalifa Penthouse", kind="property", asset_id="prop_burj_penthouse"),
    ]
    return names


def _card(card_id: str, deck: str, name: str, description: str, **kwargs: int | bool) -> Card:
    return Card(id=card_id, deck=deck, name=name, description=description, effect=CardEffect(**kwargs))


def build_decks() -> Dict[str, List[Card]]:
    main_cards: List[Card] = [
        _card("m01", "main", "Bull Run", "Strong market momentum.", money=120),
        _card("m02", "main", "Brand Boost", "Public likes your product.", reputation=20),
        _card("m03", "main", "Compliance Audit", "Regulatory friction.", money=-100),
        _card("m04", "main", "Viral Launch", "You surge online.", money=80, reputation=15),
        _card("m05", "main", "Labor Strike", "Operations halted briefly.", money=-70),
        _card("m06", "main", "Founder Podcast", "Story resonates.", reputation=25),
        _card("m07", "main", "Fleet Expansion", "Move ahead.", move=2),
        _card("m08", "main", "Luxury Tax", "Unexpected tax bill.", money=-90),
        _card("m09", "main", "Strategic Partner", "Partnership bonus.", money=140),
        _card("m10", "main", "PR Gaffe", "Bad press cycle.", reputation=-20),
        _card("m11", "main", "Story Trigger", "Resolve a storyline.", trigger_story=True),
        _card("m12", "main", "Media Trigger", "Resolve media spotlight.", trigger_media=True),
        _card("m13", "main", "Night Shift", "Move quickly.", move=3),
        _card("m14", "main", "IP Lawsuit", "Pay legal settlement.", money=-120),
        _card("m15", "main", "Market Survey", "Minor boost.", reputation=10),
        _card("m16", "main", "Angel Investor", "Fresh capital.", money=160),
        _card("m17", "main", "Security Breach", "Trust drops.", reputation=-15, money=-60),
        _card("m18", "main", "Hackathon Win", "Innovation gains.", reputation=18),
        _card("m19", "main", "Travel Voucher", "Move by one.", move=1),
        _card("m20", "main", "Tax Credit", "Government incentive.", money=110),
        _card("m21", "main", "Consumer Backlash", "Short term pain.", reputation=-18),
        _card("m22", "main", "Mentor Session", "Leadership gains.", reputation=12),
        _card("m23", "main", "Procurement Win", "Contract delivered.", money=130),
        _card("m24", "main", "Supply Shock", "Costs increase.", money=-80),
        _card("m25", "main", "Expansion Permit", "Move forward.", move=4),
        _card("m26", "main", "Community Program", "Positive image.", reputation=14),
        _card("m27", "main", "Influencer Boost", "Money + image.", money=60, reputation=10),
        _card("m28", "main", "Aggressive Rival", "Competitive hit.", money=-50, reputation=-8),
        _card("m29", "main", "Patent Granted", "Defensible moat.", money=90, reputation=8),
        _card("m30", "main", "Courier Delay", "Lost delivery cycle.", money=-40),
        _card("m31", "main", "Story Trigger II", "Deep branching event.", trigger_story=True),
        _card("m32", "main", "Media Trigger II", "Public narrative shift.", trigger_media=True),
        _card("m33", "main", "Executive Retreat", "Reputation and cash.", money=70, reputation=9),
        _card("m34", "main", "Risk Mispricing", "Portfolio drawdown.", money=-95),
        _card("m35", "main", "Sector Rotation", "Move backward strategically.", move=5),
        _card("m36", "main", "Grassroots Rally", "Momentum in polls.", reputation=22),
        _card("m37", "main", "Vendor Rebate", "Operational savings.", money=75),
        _card("m38", "main", "Penalty Fee", "Late filing.", money=-65),
        _card("m39", "main", "Global Summit", "Credibility jump.", reputation=16),
        _card("m40", "main", "Lightning Pitch", "Seed extension.", money=100),
    ]

    story_cards = [
        _card("s01", "story", "Whistleblower", "Pay to settle or take rep hit.", money=-120, reputation=-10),
        _card("s02", "story", "Acquisition Offer", "Synergy reward.", money=180, reputation=5),
        _card("s03", "story", "Ethics Review", "Strong ethics pays later.", reputation=25),
        _card("s04", "story", "Political Rumor", "Media storm.", reputation=-30),
        _card("s05", "story", "Founder Choice", "High-risk expansion.", money=150, move=2),
        _card("s06", "story", "Layoff Fallout", "Cash up, image down.", money=140, reputation=-20),
        _card("s07", "story", "Open-source Bet", "Image up.", reputation=18),
        _card("s08", "story", "Emergency Recall", "Direct loss.", money=-140),
        _card("s09", "story", "Diplomatic Visit", "Reputation boost.", reputation=20),
        _card("s10", "story", "Underground Deal", "Money for credibility.", money=190, reputation=-22),
    ]

    media_cards = [
        _card("md01", "media", "Prime Time Interview", "Great public moment.", reputation=22),
        _card("md02", "media", "Minor Scandal", "News cycle turns.", reputation=-15),
        _card("md03", "media", "Viral Thread", "Audience growth.", reputation=18, money=40),
        _card("md04", "media", "Fact-check Expose", "Credibility shock.", reputation=-20, money=-40),
        _card("md05", "media", "Influencer Endorsement", "Social trust rises.", reputation=14),
        _card("md06", "media", "Philanthropy Feature", "Goodwill converts.", reputation=16),
        _card("md07", "media", "Press Ambush", "Bad day.", reputation=-12),
        _card("md08", "media", "Election Momentum", "Political momentum.", reputation=24),
    ]

    return {"main": main_cards, "story": story_cards, "media": media_cards}
