import React, { useState, useMemo } from "react";

/**
 * U — Feed‑First Split‑Narrative News (v0.9, JS build)
 * Bugfix: remove TypeScript-only syntax to stop parser errors.
 *  - Removed all generics and type annotations.
 *  - Kept self-tests and added a couple more.
 *  - Conclusion centered in News with bold H1 and Credibility badge (0–100).
 */

export default function UNewsDemo() {
  const DEMO_KEYS = Object.keys(demoData);
  const DEFAULT_KEY = "amsterdam-incident";

  // Feed is default
  const [tab, setTab] = useState("feed");
  const [eventKey, setEventKey] = useState(DEFAULT_KEY);
  const [theme, setTheme] = useState("dark");
  const [aiDockOpen, setAiDockOpen] = useState(false);
  const [aiThread, setAiThread] = useState([]);
  const [headlineCount, setHeadlineCount] = useState(12);
  const [commentSort, setCommentSort] = useState("top");
  const [settingsOpen, setSettingsOpen] = useState(false);

  const USER_HANDLE = "@edan";

  const data = useMemo(() => safeGetData(eventKey, DEFAULT_KEY), [eventKey, DEFAULT_KEY]);
  const leftCred = avgCred(data?.narratives?.left?.sources);
  const rightCred = avgCred(data?.narratives?.right?.sources);
  const centerCred = avgCred(data?.facts?.sources);

  const isLight = theme === "light";

  const askAI = q => {
    const left = joinBulleted((data?.narratives?.left?.claims || []).slice(0, 2));
    const right = joinBulleted((data?.narratives?.right?.claims || []).slice(0, 2));
    const ans = `Likely Truth: ${data?.facts?.verdict || "Insufficient evidence"}` +
      ((left || right) ? ` | A: ${left || "—"} | B: ${right || "—"}` : "");
    setAiThread(t => [...t, { role: "user", content: q }, { role: "assistant", content: ans }]);
  };

  const openNews = id => {
    setEventKey(id);
    setTab("news");
    if (typeof window !== "undefined") window.scrollTo?.({ top: 0, behavior: "smooth" });
  };

  return (
    <div className={`min-h-screen w-full ${isLight ? "bg-white text-neutral-900" : "bg-neutral-950 text-neutral-100"}`}>
      <header className={`sticky top-0 z-30 backdrop-blur ${isLight ? "border-b border-neutral-200 bg-white/80" : "border-b border-neutral-800 bg-neutral-950/80"}`}>
        <div className="mx-auto flex max-w-7xl items-center gap-3 px-4 py-3">
          <Logo compact={tab !== "news"} labelOverride={tab === "feed" ? "U" : undefined} />
          <button onClick={() => setSettingsOpen(v => !v)} aria-label="Settings" className={`ml-1 grid h-7 w-7 place-items-center rounded ${isLight ? "bg-neutral-100" : "bg-neutral-900"}`}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zm8.94-3.5c0-.6-.05-1.18-.15-1.75l2.1-1.64-2-3.46-2.52.63a8.8 8.8 0 0 0-1.52-.88l-.38-2.55H9.04l-.38 2.55a8.8 8.8 0 0 0-1.52.88l-2.52-.63-2 3.46 2.1 1.64c-.1.57-.15 1.15-.15 1.75s.05 1.18.15 1.75l-2.1 1.64 2 3.46 2.52-.63c.47.35.98.64 1.52.88l.38 2.55h5.96l.38-2.55c.54-.24 1.05-.53 1.52-.88l2.52.63 2-3.46-2.1-1.64c.1-.57.15-1.15.15-1.75z"/></svg>
          </button>
          <nav className="ml-2 hidden items-center gap-1 md:flex">
            {["feed", "news", "uai"].map(k => (
              <button key={k} onClick={() => setTab(k)}
                className={`rounded-full px-3 py-1 text-sm transition ${tab === k ? "bg-emerald-500 text-black" : isLight ? "bg-neutral-100 text-neutral-800 hover:bg-neutral-200" : "bg-neutral-800 text-neutral-200 hover:bg-neutral-700"}`}>
                {k === "feed" ? "Feed" : k === "news" ? "News" : "U AI"}
              </button>
            ))}
          </nav>
          {tab === "news" && (
            <div className="hidden items-center gap-2 md:flex">
              {DEMO_KEYS.slice(0, 6).map(k => (
                <button key={k} onClick={() => setEventKey(k)}
                  className={`rounded-full px-3 py-1 text-sm transition ${k === eventKey ? "bg-emerald-500 text-black" : isLight ? "bg-neutral-100 text-neutral-800 hover:bg-neutral-200" : "bg-neutral-800 text-neutral-200 hover:bg-neutral-700"}`}>
                  {demoData[k]?.title || k}
                </button>
              ))}
            </div>
          )}
          <div className="ml-auto flex items-center gap-2">
            {tab !== "uai" && (
              <button onClick={() => setAiDockOpen(v => !v)} className={`rounded-full px-3 py-1 text-xs ${isLight ? "bg-neutral-100 border border-neutral-200" : "bg-neutral-900 border border-neutral-800"}`}>{aiDockOpen ? "Close U AI" : "Open U AI"}</button>
            )}
            <button onClick={() => setTheme(isLight ? "dark" : "light")} className={`rounded border px-2 py-1 text-xs ${isLight ? "border-neutral-300" : "border-neutral-700"}`}>
              {isLight ? "Dark Mode" : "White Mode"}
            </button>
          </div>
        </div>
        {settingsOpen && (
          <div className="mx-auto max-w-7xl px-4 pb-3">
            <div className={`mt-2 w-full rounded-2xl border p-3 ${isLight ? "border-neutral-200 bg-white" : "border-neutral-800 bg-neutral-900"}`}>
              <div className="flex flex-wrap items-center gap-3 text-sm">
                <div className="font-semibold">Settings</div>
                <div className="ml-auto" />
                <button onClick={() => setTheme("dark")} className={`rounded border px-2 py-1 text-xs ${!isLight ? "border-emerald-600" : "border-neutral-300"}`}>Black mode</button>
                <button onClick={() => setTheme("light")} className={`rounded border px-2 py-1 text-xs ${isLight ? "border-emerald-600" : "border-neutral-300"}`}>White mode</button>
                <button className={`rounded border px-2 py-1 text-xs ${isLight ? "border-neutral-300" : "border-neutral-700"}`}>Profile</button>
              </div>
            </div>
          </div>
        )}
      </header>

      {tab === "feed" && <FeedArea isLight={isLight} current={data} onOpenNews={openNews} aiThread={aiThread} onAskAI={askAI} />}
      {tab === "uai" && <AIChatFull isLight={isLight} userHandle={USER_HANDLE} onAsk={q => askAI(q)} />}
      {tab === "news" && (
        <>
          <section className="mx-auto max-w-4xl px-4 py-6 text-center">
            <h1 className="text-4xl font-extrabold tracking-tight">{data?.facts?.verdict || "Truth pending"}</h1>
            <div className="mt-2 flex items-center justify-center gap-3 text-sm">
              <span className={`rounded-full px-2 py-1 text-xs ${isLight ? "bg-neutral-100 text-neutral-700" : "bg-neutral-900 text-neutral-300"}`}>{data?.window || "—"} · {data?.location || "—"}</span>
              <CredBadge value={centerCred || Math.round(((leftCred || 0) + (rightCred || 0)) / 2)} />
            </div>
          </section>
          <section className="mx-auto grid max-w-7xl grid-cols-1 gap-4 px-4 md:grid-cols-3">
            <NarrativePanel isLight={isLight} side="A" data={data?.narratives?.left} cred={leftCred} withMiniComposer />
            <FactsPanel isLight={isLight} data={data?.facts} centerCred={centerCred} leftCred={leftCred} rightCred={rightCred} withMiniComposer />
            <NarrativePanel isLight={isLight} side="B" data={data?.narratives?.right} cred={rightCred} withMiniComposer />
          </section>
          <CommentsThread isLight={isLight} sort={commentSort} onSortChange={setCommentSort} embedCard={<NewsEmbed card={data} />} />
          <HeadlinesHub isLight={isLight} items={HEADLINES.slice(0, headlineCount)} onMore={() => setHeadlineCount(c => Math.min(c + 8, HEADLINES.length))} onOpen={id => openNews(id)} />
        </>
      )}

      {aiDockOpen && tab !== "uai" && (
        <AIDock isLight={isLight} userHandle={USER_HANDLE} onClose={() => setAiDockOpen(false)} onAsk={q => askAI(q)} />
      )}
    </div>
  );
}

function NarrativePanel({ isLight, side, data, cred, withMiniComposer }) {
  return (
    <div className={`rounded-2xl border p-4 ${isLight ? "border-neutral-200 bg-white" : "border-neutral-800 bg-neutral-900"}`}>
      <div className="mb-1 text-xs uppercase tracking-wide text-neutral-400">Narrative {side}</div>
      <div className="mb-2 text-sm font-semibold">{data?.title || "—"}</div>
      <div className={`mb-2 text-xs ${isLight ? "text-neutral-600" : "text-neutral-400"}`}>Objective lead: {data?.lead || "Key claims summarised below."}</div>
      <ul className="mb-3 list-disc pl-4 text-sm">{(data?.claims || []).map((c, i) => (<li key={i}>{c}</li>))}</ul>
      <CredMeter isLight={isLight} label="Credibility" value={cred} tone={side === "A" ? "red" : "blue"} />
      <CredLabel val={cred} />
      {withMiniComposer && <MiniCommentComposer isLight={isLight} placeholder={`Comment on Narrative ${side}`} />}
    </div>
  );
}

function FactsPanel({ isLight, data, centerCred, leftCred, rightCred, withMiniComposer }) {
  const [faLikes, setFaLikes] = useState(412);
  const [faDislikes, setFaDislikes] = useState(23);

  const extra = [
    { title: "Police response", text: "City later said both racist provocation and retaliatory assaults were unacceptable (demo)." },
  ];
  const happened = data?.whatHappened || "Video shows racist chants and flag tearing by a subset of Maccabi fans before the match; retaliatory street violence followed after the match (demo).";
  const timeline = data?.timeline || [
    { t: "Nov 6 eve", e: "Ultras filmed pulling flags; taxi vandalism; street fights" },
    { t: "Nov 7 20:59", e: "Minute of silence disrupted by whistles from a group; anti-Arab chants reported" },
    { t: "Post-match", e: "Ambushes and counter-violence downtown; arrests" },
  ];
  const keyFactsList = ([]).concat(data?.keyFacts || [], extra);

  return (
    <div className={`rounded-2xl border p-4 ${isLight ? "border-neutral-200 bg-white" : "border-neutral-800 bg-neutral-900"}`}>
      <div className="mb-2 flex items-center justify-between text-sm">
        <div className="font-semibold">Facts & Analysis</div>
        <div className="flex items-center gap-3 text-xs text-neutral-500">
          <button onClick={() => setFaLikes(faLikes + 1)} className="inline-flex items-center gap-1 hover:underline"><InlineIcon variant="like"/> {faLikes}</button>
          <button onClick={() => setFaDislikes(faDislikes + 1)} className="inline-flex items-center gap-1 hover:underline"><InlineIcon variant="dislike"/> {faDislikes}</button>
        </div>
      </div>
      <p className={`mb-3 text-sm ${isLight ? "text-neutral-800" : "text-neutral-200"}`}><span className="font-semibold">Conclusion:</span> {data?.verdict || "Truth pending"}.</p>
      <div className={`mb-3 rounded-lg border p-3 text-sm ${isLight ? "border-neutral-200" : "border-neutral-800"}`}>
        <div className="font-medium">What happened</div>
        <div className="mt-1 text-[13px] opacity-90">{happened}</div>
      </div>
      <div className="mb-2 text-sm font-medium">Key stats</div>
      {keyFactsList.map((f, i) => (<div key={i} className="mb-2 text-sm"><span className="font-medium">{f.title}:</span> {f.text}</div>))}
      <div className="mt-3 text-sm font-medium">Timeline</div>
      <ul className="mb-2 mt-1 list-disc pl-5 text-[13px] opacity-90">{timeline.map((it, idx) => (<li key={idx}><span className="font-mono text-xs">{it.t}</span> — {it.e}</li>))}</ul>
      <NarrativeStrengthScale left={leftCred} right={rightCred} />
      <CredMeter isLight={isLight} label="Overall Evidence" value={centerCred} tone="emerald" />
      <CredLabel val={centerCred} />
      <ConsensusGauge left={leftCred} right={rightCred} center={centerCred} />
      <div className="mt-3 text-sm"><a href="#" onClick={e => e.preventDefault()} className="underline">Methodology & Evidence</a></div>
      {withMiniComposer && <div className="mt-3"><MiniCommentComposer isLight={isLight} placeholder="Comment on Facts & Analysis" /></div>}
    </div>
  );
}

function HeadlinesHub({ isLight, items, onMore, onOpen }) {
  return (
    <section className="mx-auto max-w-5xl px-4 py-8">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-semibold">Trending Headlines</h2>
        <button onClick={onMore} className="text-xs underline">Show more</button>
      </div>
      <div className="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-3">
        {items.map(h => (
          <button key={h.id} onClick={() => onOpen(h.id)} className={`group overflow-hidden rounded-2xl border text-left transition ${isLight ? "border-neutral-200 bg-white hover:shadow" : "border-neutral-800 bg-neutral-900 hover:shadow"}`}>
            {h.thumb ? <img src={h.thumb} alt="" className="h-36 w-full object-cover" /> : <div className={`${isLight ? "bg-neutral-100" : "bg-neutral-800"} h-36 w-full`} />}
            <div className="p-3">
              <div className="flex items-center gap-2 text-[11px] text-neutral-500">
                <span className={`rounded px-1 py-0.5 ${categoryTone(h.cat)}`}>{h.cat}</span>
                <span>{h.time}</span>
              </div>
              <div className="mt-1 line-clamp-2 text-sm font-semibold leading-snug">{h.title}</div>
            </div>
          </button>
        ))}
      </div>
    </section>
  );
}

function CommentsThread({ isLight, sort, onSortChange, embedCard }) {
  const [posts, setPosts] = useState(THREAD_SAMPLE);
  const sorted = [...posts].sort((a, b) => sort === "top" ? (b.likes - b.dislikes) - (a.likes - a.dislikes) : (b.ts - a.ts));
  const like = (id, dir) => setPosts(ps => ps.map(p => p.id === id ? { ...p, likes: p.likes + (dir === "up" ? 1 : 0), dislikes: p.dislikes + (dir === "down" ? 1 : 0) } : p));

  return (
    <section className="mx-auto max-w-3xl px-4 pb-8">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-lg font-semibold">Comments</h3>
        <select value={sort} onChange={e => onSortChange(e.target.value)} className={`text-xs ${isLight ? "bg-neutral-100" : "bg-neutral-900"} rounded border px-2 py-1`}>
          <option value="top">Top</option>
          <option value="latest">Latest</option>
        </select>
      </div>
      <div className={`mb-4 flex items-start gap-2 rounded-2xl border p-3 ${isLight ? "border-neutral-200 bg-white" : "border-neutral-800 bg-neutral-900"}`}>
        <div className="h-8 w-8 rounded-full bg-neutral-400/30" />
        <input placeholder="Post your reply" className={`flex-1 rounded-full px-3 py-2 text-sm ${isLight ? "bg-neutral-100" : "bg-neutral-800"}`} />
      </div>
      <div>
        {sorted.map(p => (
          <div key={p.id} className={`border-b ${isLight ? "border-neutral-200" : "border-neutral-800"} py-3`}>
            <div className="flex items-start gap-3">
              <div className="h-9 w-9 rounded-full bg-neutral-400/30" />
              <div className="flex-1">
                <div className="text-sm"><span className="font-semibold">{p.name}</span> <span className="text-neutral-500">{p.handle} · {timeAgo(p.ts)}</span></div>
                <div className="mt-1 text-sm">{p.text}</div>
                {p.embed && (<div className="mt-2">{embedCard}</div>)}
                <div className="mt-2 flex gap-5 text-xs">
                  <IconButton label={`${p.likes}`} variant="like" onClick={() => like(p.id, "up")} />
                  <IconButton label={`${p.dislikes}`} variant="dislike" onClick={() => like(p.id, "down")} />
                  <IconButton label="Reply" variant="comment" />
                  <IconButton label="Repost" variant="repost" />
                  <IconButton label="Share" variant="share" />
                </div>
                {(p.replies || []).map(r => (
                  <div key={r.id} className="mt-3 ml-10 flex items-start gap-2">
                    <div className="h-7 w-7 rounded-full bg-neutral-400/30" />
                    <div className="flex-1">
                      <div className="text-xs"><span className="font-semibold">{r.name}</span> <span className="text-neutral-500">{r.handle} · {timeAgo(r.ts)}</span></div>
                      <div className="text-sm">{r.text}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function FeedArea({ isLight, current, onOpenNews, aiThread, onAskAI }) {
  const sampleAI = (aiThread[aiThread.length - 1] && aiThread[aiThread.length - 1].content) || current?.facts?.verdict || "U AI answer will appear here.";
  const base = [
    pNews(1, current, onOpenNews),
    pAI(2, sampleAI),
    pPhoto(3, "@sara", "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=1200&auto=format&fit=crop"),
    pText(4, "@analyst", "Counter‑point on Narrative A:"),
    pText(5, "@community", "Synthesis TL;DR: " + (current?.facts?.verdict || "n/a")),
  ];
  const filler = Array.from({ length: 16 }).map((_, i) => i % 3 === 0 ? pText(100 + i, "@user" + (i % 7), `Random thought #${i}`) : i % 3 === 1 ? pPhoto(100 + i, "@photo" + (i % 5), `https://picsum.photos/seed/${i}/1200/800`) : pLink(100 + i, "@curator", HEADLINES[(i % HEADLINES.length)], onOpenNews));
  const posts = [...base, ...filler];

  return (
    <div className="mx-auto grid max-w-7xl grid-cols-1 gap-6 px-4 py-6 md:grid-cols-3">
      <div className="md:col-span-2 space-y-4">
        {posts.map(p => (
          <FeedPost key={p.id} isLight={isLight} user={p.user} text={p.text} embed={p.embed} img={p.img} likes={p.likes} dislikes={p.dislikes} />
        ))}
      </div>
      <aside className="space-y-4">
        <HeadlinesMiniPanel isLight={isLight} items={HEADLINES.slice(0, 10)} onOpenNews={onOpenNews} />
        <AskUStrip isLight={isLight} onAsk={q => onAskAI(q)} />
      </aside>
    </div>
  );
}

function FeedPost({ isLight, user, text, embed, img, likes, dislikes }) {
  return (
    <div className={`rounded-2xl border p-0 ${isLight ? "border-neutral-200 bg-white" : "border-neutral-800 bg-neutral-900"}`}>
      <div className="flex items-start gap-3 p-4">
        <div className="h-9 w-9 shrink-0 overflow-hidden rounded-full bg-neutral-500/30">
          {user?.avatar && <img src={user.avatar} alt="" className="h-full w-full object-cover" />}
        </div>
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2 text-sm"><span className="font-semibold truncate">{user?.handle || "@user"}</span><span className="text-[11px] text-neutral-500">· {Math.floor(Math.random() * 5) + 1}h</span></div>
          <div className="mt-1 text-sm">{text}</div>
        </div>
      </div>
      {img && <img src={img} alt="" className="max-h-[420px] w-full object-cover" />}
      {embed && <div className="p-4">{embed}</div>}
      <div className="px-4 pb-3 pt-1 text-xs text-neutral-500">{likes} likes · {dislikes} dislikes</div>
      <div className="px-4 pb-4"><EngagementBar isLight={isLight} /></div>
    </div>
  );
}

function HeadlinesMiniPanel({ isLight, items, onOpenNews }) {
  return (
    <div className={`rounded-2xl border p-0 ${isLight ? "border-neutral-200 bg-white" : "border-neutral-800 bg-neutral-900"}`}>
      <div className="flex items-center justify-between rounded-t-2xl bg-emerald-600/10 px-3 py-2">
        <div className="text-sm font-semibold">Now trending</div>
        <div className="text-[11px] text-neutral-500">Live</div>
      </div>
      <ul className="divide-y divide-neutral-800">
        {items.map(h => (
          <li key={h.id}>
            <button onClick={() => onOpenNews(h.id)} className="flex w-full items-center gap-3 p-2 text-left hover:bg-neutral-800/30">
              {h.thumb ? <img src={h.thumb} alt="" className="h-12 w-16 rounded object-cover" /> : <div className="h-12 w-16 rounded bg-neutral-700" />}
              <div className="min-w-0 flex-1">
                <div className="truncate text-[13px] font-medium">{h.title}</div>
                <div className="mt-0.5 flex items-center gap-2 text-[11px] text-neutral-500">
                  <span className={`rounded px-1 py-0.5 ${categoryTone(h.cat)}`}>{h.cat}</span>
                  <span>{h.time}</span>
                </div>
              </div>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

function AskUStrip({ isLight, onAsk }) {
  const [q, setQ] = useState("");
  return (
    <div className={`rounded-2xl border p-3 ${isLight ? "border-neutral-200 bg-white" : "border-neutral-800 bg-neutral-900"}`}>
      <div className="text-sm font-semibold">Ask U how the world works</div>
      <form className="mt-2 flex gap-2" onSubmit={e => { e.preventDefault(); if (!q.trim()) return; onAsk(q); setQ(""); }}>
        <input value={q} onChange={e => setQ(e.target.value)} placeholder="Type a question…" className={`flex-1 rounded px-3 py-2 text-sm ${isLight ? "bg-neutral-100" : "bg-neutral-800"}`} />
        <button className="rounded bg-emerald-500 px-3 text-xs text-black">Ask</button>
      </form>
      <div className={`mt-1 text-[11px] ${isLight ? "text-neutral-500" : "text-neutral-400"}`}>Answers may be embedded as posts.</div>
    </div>
  );
}

function NewsEmbed({ card, onOpen }) {
  return (
    <div className="overflow-hidden rounded-xl border border-neutral-800">
      <button onClick={() => onOpen && onOpen(card?.id || "oil-price-spike")} className="w-full text-left">
        <div className="bg-neutral-900 p-3 text-sm font-semibold">{card?.title}</div>
        <div className="bg-neutral-950 p-3 text-xs text-neutral-300">{card?.facts?.verdict}</div>
      </button>
    </div>
  );
}

function AIDock({ isLight, userHandle, onClose, onAsk }) {
  const [q, setQ] = useState("");
  return (
    <div className={`fixed bottom-0 right-0 z-40 w-full max-w-md rounded-t-2xl border-t p-3 md:top-0 md:h-full md:rounded-none md:border-l ${isLight ? "bg-white border-neutral-200" : "bg-neutral-900 border-neutral-800"}`}>
      <div className="flex items-center justify-between">
        <div className="text-sm font-semibold">Hello, Welcome {userHandle} to U AI</div>
        <button onClick={onClose} className="text-xs underline">Close</button>
      </div>
      <form className="mt-3 flex gap-2" onSubmit={e => { e.preventDefault(); if (!q.trim()) return; onAsk(q); setQ(""); }}>
        <input value={q} onChange={e => setQ(e.target.value)} placeholder="Ask about any headline…" className={`flex-1 rounded px-3 py-2 text-sm ${isLight ? "bg-neutral-100" : "bg-neutral-800"}`} />
        <button className="rounded bg-emerald-500 px-3 text-xs text-black">Ask</button>
      </form>
      <div className={`mt-2 text-[11px] ${isLight ? "text-neutral-500" : "text-neutral-400"}`}>U AI answers will appear inline in feed posts or the News page.</div>
    </div>
  );
}

function AIChatFull({ isLight, userHandle, onAsk }) {
  const [q, setQ] = useState("");
  return (
    <div className="mx-auto max-w-3xl px-4 py-6">
      <div className={`rounded-2xl border p-4 ${isLight ? "border-neutral-200 bg-white" : "border-neutral-800 bg-neutral-900"}`}>
        <div className="text-sm font-semibold">Hello, Welcome {userHandle} to U AI</div>
        <form className="mt-3 flex gap-2" onSubmit={e => { e.preventDefault(); if (!q.trim()) return; onAsk(q); setQ(""); }}>
          <input value={q} onChange={e => setQ(e.target.value)} placeholder="Ask U AI anything about today’s news…" className={`flex-1 rounded px-3 py-2 text-sm ${isLight ? "bg-neutral-100" : "bg-neutral-800"}`} />
          <button className="rounded bg-emerald-500 px-3 text-xs text-black">Ask</button>
        </form>
        <div className={`mt-2 text-[11px] ${isLight ? "text-neutral-500" : "text-neutral-400"}`}>Responses are formatted with Narratives A/B and a Likely Truth and may be embedded into posts.</div>
      </div>
    </div>
  );
}

function CredBadge({ value }) {
  const v = Math.max(0, Math.min(100, Math.round(value || 0)));
  let tone = "bg-red-600/20 text-red-300";
  if (v >= 80) tone = "bg-emerald-600/20 text-emerald-300"; else if (v >= 60) tone = "bg-sky-600/20 text-sky-300"; else if (v >= 40) tone = "bg-yellow-600/20 text-yellow-300";
  return <span className={`rounded-full px-2 py-1 text-xs ${tone}`}>Credibility {v}/100</span>;
}

function EngagementBar({ isLight }) {
  return (
    <div className="mt-3 flex gap-4 text-sm">
      <IconButton label="Like" />
      <IconButton label="Dislike" variant="dislike" />
      <IconButton label="Repost" variant="repost" />
      <IconButton label="Comment" variant="comment" />
      <IconButton label="Share" variant="share" />
    </div>
  );
}

function CredMeter({ isLight, label, value, tone }) {
  const toneMap = { red: "bg-red-500", blue: "bg-sky-500", emerald: "bg-emerald-500" };
  const width = Math.max(0, Math.min(100, value || 0));
  return (
    <div className="mt-2">
      <div className="flex justify-between text-xs"><span>{label}</span><span>{Math.round(width)} / 100</span></div>
      <div className={`h-2 w-full rounded ${isLight ? "bg-neutral-200" : "bg-neutral-800"}`}>
        <div className={`h-2 rounded ${toneMap[tone]}`} style={{ width: `${width}%` }} />
      </div>
    </div>
  );
}

function CredLabel({ val }) {
  if (val >= 80) return <div className="mt-1 text-xs text-emerald-500">Highly credible</div>;
  if (val >= 60) return <div className="mt-1 text-xs text-sky-500">Mostly credible</div>;
  if (val >= 40) return <div className="mt-1 text-xs text-yellow-500">Mixed evidence</div>;
  return <div className="mt-1 text-xs text-red-500">Low credibility</div>;
}

function ConsensusGauge({ left, right, center }) {
  const total = (left || 0) + (right || 0) + (center || 0) || 1;
  return (
    <div className="mt-2 text-xs text-neutral-400">Consensus A:{Math.round((left || 0) / total * 100)}% · F:{Math.round((center || 0) / total * 100)}% · B:{Math.round((right || 0) / total * 100)}%</div>
  );
}

function NarrativeStrengthScale({ left = 0, right = 0 }) {
  const sum = Math.max(1, left + right);
  const aPct = Math.round((left / sum) * 100);
  const bPct = 100 - aPct;
  const favored = right > left ? "Narrative B favored" : right < left ? "Narrative A favored" : "Even";
  return (
    <div className="mt-3">
      <div className="mb-1 flex items-center justify-between text-xs text-neutral-500"><span>Narrative strength</span><span>{favored}</span></div>
      <div className="h-2 w-full overflow-hidden rounded bg-neutral-800">
        <div className="h-2 bg-red-500 inline-block" style={{ width: `${aPct}%` }} />
        <div className="h-2 bg-sky-500 inline-block" style={{ width: `${bPct}%` }} />
      </div>
      <div className="mt-1 flex justify-between text-[11px] text-neutral-500"><span>A {aPct}%</span><span>B {bPct}%</span></div>
    </div>
  );
}

function InlineIcon({ variant }) {
  const icons = {
    like: "👍",
    dislike: "👎",
  };
  return <span>{icons[variant] || "👍"}</span>;
}

function IconButton({ label, variant, onClick }) {
  return (
    <button onClick={onClick} className="inline-flex items-center gap-1 text-neutral-500 hover:underline">
      <InlineIcon variant={variant} />
      {label}
    </button>
  );
}

function MiniCommentComposer({ isLight, placeholder }) {
  return (
    <div className="mt-3 flex items-start gap-2">
      <div className="h-8 w-8 rounded-full bg-neutral-400/30" />
      <input placeholder={placeholder} className={`flex-1 rounded-full px-3 py-2 text-sm ${isLight ? "bg-neutral-100" : "bg-neutral-800"}`} />
    </div>
  );
}

// Helpers & Data
function safeGetData(key, fallbackKey) {
  if (key && demoData[key]) return demoData[key];
  if (fallbackKey && demoData[fallbackKey]) return demoData[fallbackKey];
  return { title: "No data", narratives: { left: {}, right: {} }, facts: {} };
}

function avgCred(s) {
  if (!Array.isArray(s) || s.length === 0) return 0;
  return s.reduce((a, b) => a + (b?.cred || 0), 0) / s.length;
}

function categoryTone(cat) {
  const map = { Politics: "bg-indigo-500/20 text-indigo-300", Economy: "bg-emerald-600/20 text-emerald-300", Conflict: "bg-red-600/20 text-red-300", Tech: "bg-sky-600/20 text-sky-300", Sports: "bg-yellow-600/20 text-yellow-300", Climate: "bg-lime-600/20 text-lime-300" };
  return map[cat] || "bg-neutral-700/20 text-neutral-300";
}

function timeAgo(ts) {
  const d = Math.max(1, Math.floor((Date.now() - ts) / 60000));
  if (d < 60) return `${d}m`;
  const h = Math.floor(d / 60);
  if (h < 24) return `${h}h`;
  const da = Math.floor(h / 24);
  return `${da}d`;
}

function joinBulleted(arr) { return arr.map(c => `• ${c}`).join(" • "); }

// self-tests
if (typeof window !== "undefined") {
  try {
    const j = joinBulleted(["a", "b"]);
    console.assert(j === "• a • • b" || j.includes(" • "), "joinBulleted should use literal bullet separator");
    const fb = safeGetData("no-such-key", "oil-price-spike");
    console.assert(fb && fb.title, "safeGetData should return fallback data");
    console.assert(avgCred([{ cred: 50 }, { cred: 70 }]) === 60, "avgCred should average cred values");
  } catch (e) {
    console.warn("Self-tests failed", e);
  }
}

// Builders
function pUser(handle) { return { handle, avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(handle)}` }; }

function pNews(id, current, onOpenNews) {
  return { id, user: pUser("@newsbot"), text: `Breaking: ${current?.title}`, embed: <NewsEmbed card={{ ...current, id: current?.id || "oil-price-spike" }} onOpen={nid => onOpenNews(nid)} />, img: null, likes: 248, dislikes: 7 };
}
function pAI(id, ans) { return { id, user: pUser("@omar"), text: "Asked U AI: Why did oil spike today? →", embed: <div className="rounded border border-emerald-700/40 p-3 text-sm">{ans}</div>, img: null, likes: 207, dislikes: 9 }; }
function pPhoto(id, handle, img) { return { id, user: pUser(handle), text: "Photo", embed: null, img, likes: Math.floor(Math.random() * 600) + 50, dislikes: Math.floor(Math.random() * 30) }; }
function pText(id, handle, text) { return { id, user: pUser(handle), text, embed: null, img: null, likes: Math.floor(Math.random() * 200) + 10, dislikes: Math.floor(Math.random() * 20) }; }
function pLink(id, handle, headline, onOpenNews) { return { id, user: pUser(handle), text: headline.title, embed: (<button onClick={() => onOpenNews(headline.id)} className="w-full text-left"><div className="rounded border border-neutral-800 p-3 text-sm">Open: {headline.title}</div></button>), img: null, likes: Math.floor(Math.random() * 150) + 5, dislikes: Math.floor(Math.random() * 20) }; }

// Demo data
const demoData = {
  "amsterdam-incident": {
    id: "amsterdam-incident",
    title: "Amsterdam UEFA Match Riots",
    window: "Nov 6–7, 2024",
    location: "Amsterdam, NL",
    narratives: {
      left: {
        title: "Antisemitic attacks on Israelis",
        lead: "Post-match assaults targeted Israelis; leaders condemned antisemitism.",
        claims: [
          "Israeli fans were hunted across the city; ≈7 hospitalized, 20–30 minor injuries",
          "Leaders condemned antisemitism; arrests followed",
          "Police organized escorts and transfers"
        ],
        sources: [
          { name: "Reuters arrests update", cred: 85 },
          { name: "AP follow-up", cred: 85 },
          { name: "Netherlands govt statements", cred: 80 }
        ]
      },
      right: {
        title: "Ultras’ racist provocation escalated clashes",
        lead: "Documented anti‑Arab chants, flag tearing, and harassment preceded attacks.",
        claims: [
          "Flags torn from homes; anti‑Arab chants like ‘death to Arabs’ recorded",
          "Taxi drivers and locals harassed before match",
          "Mayor/prosecutor/police memo cites ‘toxic combination’ incl. hooliganism"
        ],
        sources: [
          { name: "Guardian mayor report", cred: 90 },
          { name: "Washington Post video analysis", cred: 90 },
          { name: "Amsterdam memo coverage", cred: 85 }
        ]
      }
    },
    facts: {
      verdict: "Narrative B stronger; authorities must condemn both racist provocation and retaliatory assaults",
      whatHappened: "A subset of Maccabi fans engaged in racist slurs, harassment of taxi drivers, and removal of Palestinian flags before the match; after the match, Israeli fans were ambushed in multiple downtown spots, resulting in injuries and arrests.",
      keyFacts: [
        { title: "Injuries", text: "≈7 hospitalized; 20–30 minor injuries" },
        { title: "Videos", text: "Multiple clips corroborate both racist provocation and later assaults" },
        { title: "Official memo", text: "‘Toxic combination of antisemitism, hooliganism, and anger over Gaza’" }
      ],
      timeline: [
        { t: "Nov 6 evening", e: "Flag removals, racist chants, taxi harassment recorded" },
        { t: "Nov 7 pre‑match", e: "Police separate groups; chants continue" },
        { t: "Post‑match", e: "Ambushes, street fights; escorts organized; arrests" }
      ],
      sources: [
        { name: "Verified video compilations", cred: 98 },
        { name: "Mayor–prosecutor–police memo", cred: 98 },
        { name: "Major outlets’ corrections", cred: 96 }
      ]
    }
  },
  "oil-price-spike": {
    id: "oil-price-spike",
    title: "Oil Prices Soar After Gulf Tensions Escalate",
    window: "Last 6h",
    location: "Middle East",
    narratives: {
      left: { title: "OPEC policy drove spike", lead: "Producers signaled cuts as tensions rose.", claims: ["Production cuts announced", "Cartel exploiting crisis", "Consumers bear brunt"], sources: [{ name: "MarketWatch", cred: 75 }] },
      right: { title: "Security threats disrupted supply", lead: "A shipping incident constrained flows.", claims: ["Tanker incident in Strait", "Insurance rates up", "Supply chain jitters"], sources: [{ name: "Reuters", cred: 90 }] }
    },
    facts: { verdict: "Both policy and disruption contributed", keyFacts: [{ title: "Brent", text: "$108/bbl intraday high (demo)" }, { title: "Drivers", text: "Cuts + tanker risk cited by multiple outlets (demo)" }], sources: [{ name: "Reuters", cred: 92 }] }
  }
};

const HEADLINES = [
  { id: "oil-price-spike", title: "Oil Prices Soar After Gulf Tensions Escalate", cat: "Economy", time: "30m ago", thumb: "https://images.unsplash.com/photo-1542367597-8849eb47b6ea?q=80&w=1200&auto=format&fit=crop" },
  { id: "amsterdam-incident", title: "Amsterdam UEFA Match Riots", cat: "Conflict", time: "1h ago", thumb: "https://images.unsplash.com/photo-1504712598893-24159a89200e?q=80&w=1200&auto=format&fit=crop" }
];

const THREAD_SAMPLE = [
  { id: 1, name: "Fatima", handle: "@fatima", text: "The conclusion seems fair. Would like district‑level data.", ts: Date.now() - 7200000, likes: 312, dislikes: 7, embed: true, replies: [{ id: 11, name: "Omar", handle: "@omar", text: "City data is in local feeds.", ts: Date.now() - 3600000 }] },
  { id: 2, name: "Aisha", handle: "@aisha", text: "Left claim #2 needs", ts: Date.now() - 4000000, likes: 120, dislikes: 2 }
];
