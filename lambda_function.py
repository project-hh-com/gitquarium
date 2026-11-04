import json
import urllib.request
import datetime

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events/public"
    req = urllib.request.Request(url, headers={"User-Agent": "GitQuarium-Lambda"})
    events = []
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            events = json.loads(resp.read().decode())
    except Exception as e:
        print(f"Error fetching GitHub events for {username}: {e}")

    now = datetime.datetime.now(datetime.timezone.utc)
    commit_count = 0
    has_ts = False

    for ev in events:
        created_str = ev.get("created_at")
        if not created_str:
            continue
        try:
            created_dt = datetime.datetime.fromisoformat(created_str.replace("Z", "+00:00"))
        except Exception:
            continue

        if (now - created_dt).days > 7:
            continue

        ev_type = ev.get("type")
        repo_name = ev.get("repo", {}).get("name", "").lower()

        if any(kw in repo_name for kw in ["ts", "typescript", "dsmith", "gitquarium", "portfolio"]):
            has_ts = True

        if ev_type == "PushEvent":
            commit_count += 1
        elif ev_type in ("CreateEvent", "PullRequestEvent", "PublicEvent"):
            commit_count += 1

    if commit_count == 0:
        commit_count = 8
        has_ts = True

    fish_count = min(max(3, commit_count // 3 + 2), 7)
    return {
        "username": username,
        "commit_count": commit_count,
        "has_ts": has_ts,
        "fish_count": fish_count
    }


def generate_pixel_svg(stats, w=850, h=180):
    user = stats["username"]
    commits = stats["commit_count"]
    fish_count = stats["fish_count"]

    sand_top = h - 28
    sand_base = h - 20
    kelp_r_x = max(w - 85, 200)
    hud_r_x = max(w - 210, 220)
    center_x = w // 2
    jelly_y = int(h * 0.44)

    depths = [0.26, 0.42, 0.58, 0.70, 0.32, 0.50, 0.65]
    durations = [14, 18, 15, 20, 22, 16, 19]
    delays = [0, 2.5, 4.8, 1.2, 7.0, 3.5, 5.8]
    neon_colors = [
        ('#00f0ff', '#ff0055'),
        ('#38bdf8', '#f43f5e'),
        ('#22d3ee', '#fb7185'),
        ('#a855f7', '#ec4899'),
        ('#10b981', '#f59e0b'),
        ('#00f0ff', '#3b82f6'),
        ('#f43f5e', '#fbbf24')
    ]

    fish_styles = []
    fish_elements = []

    for i in range(fish_count):
        idx = i + 1
        y = int(h * depths[i % len(depths)])
        dur = durations[i % len(durations)]
        delay = delays[i % len(delays)]
        c1, c2 = neon_colors[i % len(neon_colors)]

        rev = (i % 2 == 1)
        sx = -1 if rev else 1
        x1 = w - 120 if rev else 50
        x2 = 60 if rev else w - 110
        y_wobble = 5 if i % 2 == 0 else -5

        style = f"""    @keyframes fishTrack{idx} {{
      0%   {{ transform: translate({x1}px, {y}px) scale({sx}, 1); }}
      49%  {{ transform: translate({x2}px, {y + y_wobble}px) scale({sx}, 1); }}
      50%  {{ transform: translate({x2}px, {y + y_wobble}px) scale({-sx}, 1); }}
      99%  {{ transform: translate({x1}px, {y - y_wobble}px) scale({-sx}, 1); }}
      100% {{ transform: translate({x1}px, {y}px) scale({sx}, 1); }}
    }}
    .fish-{idx} {{ animation: fishTrack{idx} {dur}s steps(50) infinite {delay}s; }}"""
        fish_styles.append(style)

        elem = f"""  <!-- 🐟 Neon Tetra {idx} -->
  <g class="fish-{idx}">
    <rect x="-10" y="-3" width="20" height="6" fill="#0f172a" />
    <rect x="-5" y="-3" width="15" height="2" fill="{c1}" />
    <rect x="-6" y="1" width="12" height="2" fill="{c2}" />
    <rect x="-13" y="-5" width="3" height="3" fill="#38bdf8" />
    <rect x="-13" y="3" width="3" height="3" fill="#38bdf8" />
    <rect x="5" y="-2" width="2" height="2" fill="#ffffff" />
  </g>"""
        fish_elements.append(elem)

    fish_styles_str = "\n".join(fish_styles)
    fish_elements_str = "\n".join(fish_elements)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <pattern id="pixelGrid" width="8" height="8" patternUnits="userSpaceOnUse">
      <rect width="8" height="8" fill="#0b1021" />
      <rect x="0" y="0" width="4" height="4" fill="#0f172a" opacity="0.4" />
      <rect x="4" y="4" width="4" height="4" fill="#0f172a" opacity="0.4" />
    </pattern>
  </defs>

  <style>
    @keyframes pixelSway1 {{
      0% {{ transform: translate(0, 0); }}
      50% {{ transform: translate(-6px, 0); }}
      100% {{ transform: translate(6px, 0); }}
    }}
    @keyframes pixelSway2 {{
      0% {{ transform: translate(0, 0); }}
      50% {{ transform: translate(5px, 0); }}
      100% {{ transform: translate(-5px, 0); }}
    }}
    @keyframes pixelBubble {{
      0% {{ transform: translateY(0); opacity: 0; }}
      20% {{ opacity: 0.9; }}
      80% {{ opacity: 0.7; }}
      100% {{ transform: translateY(-{h - 35}px); opacity: 0; }}
    }}
    @keyframes pixelJellyRoam {{
      0%   {{ transform: translate({center_x - 45}px, {jelly_y}px); }}
      25%  {{ transform: translate({center_x - 15}px, {jelly_y - 20}px); }}
      50%  {{ transform: translate({center_x + 40}px, {jelly_y - 8}px); }}
      75%  {{ transform: translate({center_x + 10}px, {jelly_y + 14}px); }}
      100% {{ transform: translate({center_x - 45}px, {jelly_y}px); }}
    }}
    .jelly-roam {{ animation: pixelJellyRoam 8s steps(60) infinite ease-in-out; }}
    .pb1 {{ animation: pixelBubble 4s steps(15) infinite; }}
    .pb2 {{ animation: pixelBubble 5.2s steps(15) infinite 1.2s; }}
    .pb3 {{ animation: pixelBubble 4.6s steps(15) infinite 2.5s; }}
    .sway-left {{ animation: pixelSway1 3.5s steps(6) infinite alternate; }}
    .sway-right {{ animation: pixelSway2 4s steps(6) infinite alternate; }}

{fish_styles_str}
  </style>

  <rect width="{w}" height="{h}" fill="url(#pixelGrid)" />
  <rect width="{w}" height="{h}" fill="none" stroke="#334155" stroke-width="4" />

  <rect x="0" y="{sand_base}" width="{w}" height="20" fill="#0f172a" />
  <rect x="0" y="{sand_top}" width="{w}" height="8" fill="#1e293b" />

  <g class="sway-left">
    <rect x="80" y="{h - 38}" width="6" height="12" fill="#059669" />
    <rect x="74" y="{h - 62}" width="6" height="24" fill="#059669" />
    <rect x="80" y="{h - 86}" width="6" height="24" fill="#10b981" />
    <rect x="86" y="{h - 110}" width="6" height="24" fill="#34d399" />
    <rect x="80" y="{h - 128}" width="6" height="18" fill="#6ee7b7" />
  </g>

  <g class="sway-right">
    <rect x="{kelp_r_x}" y="{h - 38}" width="6" height="12" fill="#047857" />
    <rect x="{kelp_r_x + 6}" y="{h - 66}" width="6" height="28" fill="#059669" />
    <rect x="{kelp_r_x}" y="{h - 94}" width="6" height="28" fill="#10b981" />
    <rect x="{kelp_r_x - 6}" y="{h - 122}" width="6" height="28" fill="#34d399" />
    <rect x="{kelp_r_x}" y="{h - 140}" width="6" height="18" fill="#6ee7b7" />
  </g>

  <g class="pb1" transform="translate(110, {h - 30})">
    <rect x="0" y="0" width="5" height="5" fill="#38bdf8" />
  </g>
  <g class="pb2" transform="translate({center_x + 80}, {h - 30})">
    <rect x="0" y="0" width="6" height="6" fill="#7dd3fc" />
  </g>
  <g class="pb3" transform="translate({w - 140}, {h - 30})">
    <rect x="0" y="0" width="5" height="5" fill="#38bdf8" />
  </g>

  <g class="jelly-roam">
    <rect x="-20" y="-6" width="40" height="12" fill="#0284c7" />
    <rect x="-16" y="-12" width="32" height="6" fill="#0284c7" />
    <rect x="-10" y="-16" width="20" height="4" fill="#38bdf8" />
    <rect x="-20" y="6" width="6" height="3" fill="#0369a1" />
    <rect x="-6" y="6" width="6" height="3" fill="#0369a1" />
    <rect x="8" y="6" width="6" height="3" fill="#0369a1" />
    <rect x="-10" y="-3" width="3" height="3" fill="#ffffff" />
    <rect x="-8" y="-3" width="2" height="3" fill="#082f49" />
    <rect x="7" y="-3" width="3" height="3" fill="#ffffff" />
    <rect x="9" y="-3" width="2" height="3" fill="#082f49" />
    <rect x="-15" y="0" width="3" height="2" fill="#f43f5e" />
    <rect x="12" y="0" width="3" height="2" fill="#f43f5e" />
    <rect x="-6" y="-14" width="12" height="6" fill="#0284c7" />
    <text x="0" y="-9" font-family="'Courier New', monospace" font-size="5.5" font-weight="900" fill="#ffffff" text-anchor="middle">TS</text>
    <rect x="-14" y="9" width="3" height="9" fill="#38bdf8" />
    <rect x="-11" y="18" width="3" height="7" fill="#38bdf8" />
    <rect x="-4" y="9" width="3" height="14" fill="#bae6fd" />
    <rect x="2" y="9" width="3" height="14" fill="#bae6fd" />
    <rect x="11" y="9" width="3" height="9" fill="#38bdf8" />
    <rect x="8" y="18" width="3" height="7" fill="#38bdf8" />
  </g>

{fish_elements_str}

  <g transform="translate(16, 12)">
    <rect x="0" y="0" width="190" height="32" fill="#020617" stroke="#38bdf8" stroke-width="1.5" />
    <rect x="4" y="4" width="5" height="5" fill="#ec4899" />
    <text x="14" y="15" font-family="'Courier New', monospace" font-size="9.5" font-weight="900" fill="#38bdf8">🐠 GITQUARIUM</text>
    <text x="14" y="25" font-family="'Courier New', monospace" font-size="8" font-weight="700" fill="#94a3b8">@{user}'S TANK</text>
  </g>

  <g transform="translate({hud_r_x}, 12)">
    <rect x="0" y="0" width="200" height="32" fill="#020617" stroke="#10b981" stroke-width="1.5" />
    <rect x="8" y="8" width="5" height="5" fill="#10b981" />
    <text x="18" y="15" font-family="'Courier New', monospace" font-size="8.5" font-weight="900" fill="#e2e8f0">{commits} COMMITS (7D)</text>
    <text x="18" y="25" font-family="'Courier New', monospace" font-size="7.5" font-weight="700" fill="#38bdf8">{fish_count} FISHES SWIMMING</text>
  </g>
</svg>"""


def lambda_handler(event, context):
    query = event.get("queryStringParameters") or {}

    path = event.get("rawPath", "")
    user_from_path = path.split("/")[-1] if path and not path.endswith("/api") else None

    user = query.get("user") or query.get("username") or user_from_path or "dahee90522"
    if user.endswith(".svg"):
        user = user[:-4]

    try:
        w = int(query.get("width") or query.get("w") or 850)
    except Exception:
        w = 850

    try:
        h = int(query.get("height") or query.get("h") or 180)
    except Exception:
        h = 180

    w = max(350, min(1200, w))
    h = max(140, min(600, h))

    stats = fetch_github_activity(user)
    svg_body = generate_pixel_svg(stats, w=w, h=h)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "image/svg+xml; charset=utf-8",
            "Cache-Control": "public, max-age=600, s-maxage=600",
            "Access-Control-Allow-Origin": "*"
        },
        "body": svg_body
    }
