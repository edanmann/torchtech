let gameId = null;
let game = null;

const $ = (id) => document.getElementById(id);
async function api(path, method = "GET", body) {
  const res = await fetch(path, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "API error");
  return data;
}

function render() {
  if (!game) return;
  $("gameId").textContent = `Game ID: ${game.id}`;
  const current = game.players[game.current_player_index];
  $("playersView").textContent = game.players
    .map(
      (p) => `${p.name} | $${p.money} | REP ${p.reputation} | POWER ${p.money + p.reputation} | pos ${p.position}${p.id === current.id ? " <- current" : ""}`
    )
    .join("\n");

  $("metaView").textContent = `Turn: ${game.turn_number}\nRound: ${game.round_number}\nPresident: ${game.president_player_id || "none"}\nCurrent: ${current.name}`;
  $("logView").textContent = game.action_log.slice(-20).join("\n");

  $("board").innerHTML = game.board
    .map((s) => `<div class="square ${s.index === current.position ? "current" : ""}"><strong>${s.index}</strong><br/>${s.name}</div>`)
    .join("");
}

async function refresh() {
  if (!gameId) return;
  game = await api(`/games/${gameId}`);
  render();
}

$("createGame").onclick = async () => {
  const players = $("players").value.split(",").map((s) => s.trim()).filter(Boolean);
  game = await api("/games", "POST", { player_names: players, max_rounds: 12 });
  gameId = game.id;
  game = await api(`/games/${gameId}/start`, "POST", {});
  render();
};

$("drawMain").onclick = async () => { await api(`/games/${gameId}/draw-main-card`, "POST"); await refresh(); };
$("move").onclick = async () => { await api(`/games/${gameId}/move`, "POST", { steps: Number($("steps").value), pass_start_choice: $("startChoice").value }); await refresh(); };
$("resolve").onclick = async () => { await api(`/games/${gameId}/resolve-square`, "POST"); await refresh(); };
$("nextTurn").onclick = async () => { await api(`/games/${gameId}/next-turn`, "POST"); await refresh(); };
$("buyAsset").onclick = async () => { await api(`/games/${gameId}/buy-property`, "POST", { asset_id: $("assetId").value.trim() }); await refresh(); };
$("upgradeAsset").onclick = async () => { await api(`/games/${gameId}/upgrade-asset`, "POST", { asset_id: $("assetId").value.trim() }); await refresh(); };
$("runPresident").onclick = async () => { await api(`/games/${gameId}/run-for-president`, "POST"); await refresh(); };
$("policy").onclick = async () => { await api(`/games/${gameId}/presidential-policy`, "POST"); await refresh(); };
$("lobbySmall").onclick = async () => { await api(`/games/${gameId}/lobby`, "POST", { tier: "small" }); await refresh(); };
$("lobbyLarge").onclick = async () => { await api(`/games/${gameId}/lobby`, "POST", { tier: "large" }); await refresh(); };
