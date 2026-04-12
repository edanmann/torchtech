# RULES_ASSUMPTIONS

## Source conflicts reconciled
1. **Board square category totals conflict**: listed categories sum to 54, but board must be 52.
   - Implemented a 52-square board and kept all named special/company/property squares.
   - Reduced unnamed Free Land count to 7 (instead of 9) to satisfy 52 total.

2. **Round engine ambiguity**:
   - Implemented synchronized global rounds: each player must pass Start once before round-end payouts fire.
   - `round_passed_start` tracks players who passed Start in current round.

3. **Airport ownership/synergy ambiguity**:
   - Airports are currently non-ownable travel hubs.
   - SpaceX B2G airport synergy omitted by default (easy to add later through config/ownership extension).

4. **Presidency retention threshold ambiguity**:
   - A president must maintain at least 100 reputation and is forcibly removed below -500 reputation.

5. **Court and Intelligence values were variable `x`**:
   - Court uses half of target's most valuable asset value (minimum 60).
   - Intelligence uses fixed MVP values: target loses 80 money + 12 reputation; actor gains those values.

6. **Storyline branching in MVP**:
   - Story cards are data-driven and effectful now; explicit multi-choice branching hooks are prepared for future expansion.

7. **Investment wording ambiguity**:
   - Investment is a one-round delayed bet with configurable success probability, returning 2x on success.

## Other implementation notes
- B2C HQ/store conflict rule implemented with explicit choice endpoint for buyout vs revenue sharing.
- Rent/income formula for property and stores is strictly L1=x/2, L2=x, L3=1.5x.
- Upgrade cost per level is exactly base asset price (x).
