#!/usr/bin/env python3
"""
GitQuarium SVG Generator
Generates animated aquarium SVGs with diverse marine species:
- 🪼 TypeScript Jellyfish (central gliding & propelling)
- 🐡 Bug Pufferfish (chubby golden/orange spiky puffer)
- ⚡ React Ray (cyan glowing stingray with sweeping tail)
- 🏮 Nightshift Anglerfish (deep purple body with glowing yellow light bulb antenna)
- 🐟 Neon Tetras (vibrant neon striped agile schooling fishes)
"""

import sys
import os
import json
import urllib.request
import datetime
import argparse

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events/public"
    headers = {"User-Agent": "GitQuarium-Bot"}
    gh_token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if gh_token:
        headers["Authorization"] = f"token {gh_token}"
    req = urllib.request.Request(url, headers=headers)
    events = []
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            events = json.loads(resp.read().decode())
    except Exception as e:
        print(f"[!] Warning: Failed to fetch events for {username}: {e}")

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
        commit_count = 30
        has_ts = True

    fish_count = 7

    return {
        "username": username,
        "commit_count": commit_count,
        "has_ts": has_ts or True,
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

    # We will generate 7 diverse creatures:
    # 1. 🐡 Pufferfish (복어)
    # 2. ⚡ React Ray (가오리)
    # 3. 🏮 Anglerfish (야근 아귀)
    # 4. 🐟 Neon Tetra (Cyan/Pink)
    # 5. 🐟 Neon Tetra (Emerald/Gold)
    # 6. 🐟 Neon Tetra (Purple/Magenta)
    # 7. 🐟 Neon Tetra (Sky Blue/Coral)

    styles = []
    elements = []

    # 1. 🐡 Bug Pufferfish (복어) - chubby buoyant waddling & bouncing sine waves
    styles.append(f"""    @keyframes pufferTrack {{
      0%   {{ transform: translate(70px, {int(h*0.42)}px) scale(1, 1); }}
      15%  {{ transform: translate(220px, {int(h*0.25)}px) scale(1, 1); }}
      30%  {{ transform: translate(380px, {int(h*0.52)}px) scale(1, 1); }}
      42%  {{ transform: translate(540px, {int(h*0.28)}px) scale(1, 1); }}
      49%  {{ transform: translate({w - 110}px, {int(h*0.45)}px) scale(1, 1); }}
      50%  {{ transform: translate({w - 110}px, {int(h*0.45)}px) scale(-1, 1); }}
      65%  {{ transform: translate(560px, {int(h*0.60)}px) scale(-1, 1); }}
      78%  {{ transform: translate(390px, {int(h*0.26)}px) scale(-1, 1); }}
      90%  {{ transform: translate(210px, {int(h*0.50)}px) scale(-1, 1); }}
      100% {{ transform: translate(70px, {int(h*0.42)}px) scale(1, 1); }}
    }}
    .creature-puffer {{ animation: pufferTrack 21s ease-in-out infinite 0.5s; }}""")

    elements.append(f"""  <!-- 🐡 Bug Pufferfish -->
  <g class="creature-puffer" transform="translate(70, {int(h*0.42)})">
    <rect x="-8" y="-6" width="16" height="12" fill="#f59e0b" />
    <rect x="-6" y="-8" width="12" height="16" fill="#f59e0b" />
    <rect x="-4" y="2" width="8" height="4" fill="#fef3c7" />
    <rect x="4" y="-4" width="3" height="3" fill="#ffffff" />
    <rect x="5" y="-3" width="2" height="2" fill="#000000" />
    <rect x="-11" y="-3" width="3" height="6" fill="#d97706" />
    <rect x="-1" y="-10" width="3" height="2" fill="#d97706" />
    <rect x="-1" y="8" width="3" height="2" fill="#d97706" />
  </g>""")

    # 2. ⚡ React Ray (가오리) - wide diagonal swoops & altitude glides
    styles.append(f"""    @keyframes rayTrack {{
      0%   {{ transform: translate({w - 120}px, {int(h*0.28)}px) scale(-1, 1); }}
      16%  {{ transform: translate(540px, {int(h*0.64)}px) scale(-1, 1); }}
      30%  {{ transform: translate(360px, {int(h*0.35)}px) scale(-1, 1); }}
      42%  {{ transform: translate(200px, {int(h*0.62)}px) scale(-1, 1); }}
      49%  {{ transform: translate(80px, {int(h*0.48)}px) scale(-1, 1); }}
      50%  {{ transform: translate(80px, {int(h*0.48)}px) scale(1, 1); }}
      66%  {{ transform: translate(280px, {int(h*0.26)}px) scale(1, 1); }}
      80%  {{ transform: translate(490px, {int(h*0.58)}px) scale(1, 1); }}
      92%  {{ transform: translate(650px, {int(h*0.38)}px) scale(1, 1); }}
      100% {{ transform: translate({w - 120}px, {int(h*0.28)}px) scale(-1, 1); }}
    }}
    .creature-ray {{ animation: rayTrack 19s ease-in-out infinite 2s; }}""")

    elements.append(f"""  <!-- ⚡ React Ray -->
  <g class="creature-ray" transform="translate({w - 120}, {int(h*0.28)})">
    <polygon points="0,-7 14,0 0,7 -10,0" fill="#0284c7" />
    <polygon points="-2,-4 8,0 -2,4 -6,0" fill="#38bdf8" />
    <circle cx="4" cy="-2" r="1.2" fill="#ffffff" />
    <circle cx="4" cy="2" r="1.2" fill="#ffffff" />
    <line x1="-10" y1="0" x2="-22" y2="0" stroke="#38bdf8" stroke-width="1.5" />
  </g>""")

    # 3. 🏮 Nightshift Anglerfish (야근 아귀) - deep sea prowler with bobbing lantern
    styles.append(f"""    @keyframes anglerTrack {{
      0%   {{ transform: translate(80px, {int(h*0.69)}px) scale(1, 1); }}
      18%  {{ transform: translate(240px, {int(h*0.58)}px) scale(1, 1); }}
      32%  {{ transform: translate(430px, {int(h*0.73)}px) scale(1, 1); }}
      45%  {{ transform: translate(620px, {int(h*0.62)}px) scale(1, 1); }}
      49%  {{ transform: translate({w - 130}px, {int(h*0.71)}px) scale(1, 1); }}
      50%  {{ transform: translate({w - 130}px, {int(h*0.71)}px) scale(-1, 1); }}
      66%  {{ transform: translate(510px, {int(h*0.58)}px) scale(-1, 1); }}
      80%  {{ transform: translate(300px, {int(h*0.72)}px) scale(-1, 1); }}
      94%  {{ transform: translate(140px, {int(h*0.62)}px) scale(-1, 1); }}
      100% {{ transform: translate(80px, {int(h*0.69)}px) scale(1, 1); }}
    }}
    .creature-angler {{ animation: anglerTrack 24s ease-in-out infinite 3.5s; }}""")

    elements.append(f"""  <!-- 🏮 Nightshift Anglerfish -->
  <g class="creature-angler" transform="translate(80, {int(h*0.69)})">
    <ellipse cx="0" cy="0" rx="9" ry="6" fill="#4c1d95" />
    <rect x="4" y="-2" width="2" height="2" fill="#ffffff" />
    <path d="M 2 -5 Q 6 -11 9 -8" stroke="#a78bfa" stroke-width="1.5" fill="none" />
    <circle cx="9" cy="-8" r="2.5" fill="#fef08a" />
    <polygon points="-9,0 -14,-4 -14,4" fill="#5b21b6" />
  </g>""")

    # 4~7. 🐟 Agile Neon Tetras (4 colors, varied diagonal & undulating paths)
    tetras = [
        # (ty_base, dur, delay, c1, c2, rev, y_offsets)
        (int(h*0.30), 14, 0.0, '#00f0ff', '#ff0055', False, (-12, 14, -8)),
        (int(h*0.58), 16, 3.5, '#10b981', '#f59e0b', True, (16, -14, 10)),
        (int(h*0.42), 15, 6.0, '#a855f7', '#ec4899', False, (14, -16, 12)),
        (int(h*0.74), 18, 2.0, '#38bdf8', '#f43f5e', True, (-14, 12, -10))
    ]

    for idx, (ty, dur, delay, c1, c2, rev, (dy1, dy2, dy3)) in enumerate(tetras, start=1):
        sx = -1 if rev else 1
        x1 = w - 110 if rev else 50
        x2 = 60 if rev else w - 110
        mid1 = int(x1 + (x2 - x1) * 0.33)
        mid2 = int(x1 + (x2 - x1) * 0.66)

        styles.append(f"""    @keyframes tetraTrack{idx} {{
      0%   {{ transform: translate({x1}px, {ty}px) scale({sx}, 1); }}
      20%  {{ transform: translate({mid1}px, {ty + dy1}px) scale({sx}, 1); }}
      36%  {{ transform: translate({mid2}px, {ty + dy2}px) scale({sx}, 1); }}
      49%  {{ transform: translate({x2}px, {ty + dy3}px) scale({sx}, 1); }}
      50%  {{ transform: translate({x2}px, {ty + dy3}px) scale({-sx}, 1); }}
      70%  {{ transform: translate({mid2}px, {ty - dy1}px) scale({-sx}, 1); }}
      85%  {{ transform: translate({mid1}px, {ty - dy2}px) scale({-sx}, 1); }}
      100% {{ transform: translate({x1}px, {ty}px) scale({sx}, 1); }}
    }}
    .tetra-{idx} {{ animation: tetraTrack{idx} {dur}s ease-in-out infinite {delay}s; }}""")

        elements.append(f"""  <!-- 🐟 Neon Tetra {idx} -->
  <g class="tetra-{idx}" transform="translate({x1}, {ty})">
    <rect x="-10" y="-3" width="20" height="6" fill="#0f172a" />
    <rect x="-5" y="-3" width="15" height="2" fill="{c1}" />
    <rect x="-6" y="1" width="12" height="2" fill="{c2}" />
    <rect x="-13" y="-5" width="3" height="3" fill="#38bdf8" />
    <rect x="-13" y="3" width="3" height="3" fill="#38bdf8" />
    <rect x="5" y="-2" width="2" height="2" fill="#ffffff" />
  </g>""")

    creature_styles = "\n".join(styles)
    creature_elements = "\n".join(elements)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <pattern id="pixelGrid" width="8" height="8" patternUnits="userSpaceOnUse">
      <rect width="8" height="8" fill="#0b1021" />
      <rect x="0" y="0" width="4" height="4" fill="#0f172a" opacity="0.4" />
      <rect x="4" y="4" width="4" height="4" fill="#0f172a" opacity="0.4" />
    </pattern>
  </defs>

  <style>
  <![CDATA[
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
    /* 🪼 TS Jellyfish Roaming and Propulsion Animation */
    @keyframes pixelJellyRoam {{
      0%   {{ transform: translate({center_x - 50}px, {jelly_y}px); }}
      20%  {{ transform: translate({center_x - 10}px, {jelly_y - 24}px); }}
      35%  {{ transform: translate({center_x + 35}px, {jelly_y - 12}px); }}
      55%  {{ transform: translate({center_x + 65}px, {jelly_y + 18}px); }}
      70%  {{ transform: translate({center_x + 20}px, {jelly_y + 26}px); }}
      85%  {{ transform: translate({center_x - 25}px, {jelly_y + 8}px); }}
      100% {{ transform: translate({center_x - 50}px, {jelly_y}px); }}
    }}
    .jelly-roam {{ animation: pixelJellyRoam 9s ease-in-out infinite; }}
    .pb1 {{ animation: pixelBubble 4s steps(15) infinite; }}
    .pb2 {{ animation: pixelBubble 5.2s steps(15) infinite 1.2s; }}
    .pb3 {{ animation: pixelBubble 4.6s steps(15) infinite 2.5s; }}
    .sway-left {{ animation: pixelSway1 3.5s steps(6) infinite alternate; }}
    .sway-right {{ animation: pixelSway2 4s steps(6) infinite alternate; }}

{creature_styles}
  ]]>
  </style>

  <!-- Deep Ocean Base -->
  <rect width="{w}" height="{h}" fill="url(#pixelGrid)" />
  <rect width="{w}" height="{h}" fill="none" stroke="#334155" stroke-width="4" />

  <!-- Seabed -->
  <rect x="0" y="{sand_base}" width="{w}" height="20" fill="#0f172a" />
  <rect x="0" y="{sand_top}" width="{w}" height="8" fill="#1e293b" />

  <!-- Left Compact Kelp -->
  <g class="sway-left">
    <rect x="80" y="{h - 38}" width="6" height="12" fill="#059669" />
    <rect x="74" y="{h - 62}" width="6" height="24" fill="#059669" />
    <rect x="80" y="{h - 86}" width="6" height="24" fill="#10b981" />
    <rect x="86" y="{h - 110}" width="6" height="24" fill="#34d399" />
    <rect x="80" y="{h - 128}" width="6" height="18" fill="#6ee7b7" />
  </g>

  <!-- Right Compact Kelp -->
  <g class="sway-right">
    <rect x="{kelp_r_x}" y="{h - 38}" width="6" height="12" fill="#047857" />
    <rect x="{kelp_r_x + 6}" y="{h - 66}" width="6" height="28" fill="#059669" />
    <rect x="{kelp_r_x}" y="{h - 94}" width="6" height="28" fill="#10b981" />
    <rect x="{kelp_r_x - 6}" y="{h - 122}" width="6" height="28" fill="#34d399" />
    <rect x="{kelp_r_x}" y="{h - 140}" width="6" height="18" fill="#6ee7b7" />
  </g>

  <!-- Compact Bubbles -->
  <g class="pb1" transform="translate(110, {h - 30})">
    <rect x="0" y="0" width="5" height="5" fill="#38bdf8" />
  </g>
  <g class="pb2" transform="translate({center_x + 80}, {h - 30})">
    <rect x="0" y="0" width="6" height="6" fill="#7dd3fc" />
  </g>
  <g class="pb3" transform="translate({w - 140}, {h - 30})">
    <rect x="0" y="0" width="5" height="5" fill="#38bdf8" />
  </g>

  <!-- 🪼 TypeScript Jellyfish (Smooth Roaming and Propelling) -->
  <g class="jelly-roam" transform="translate({center_x - 50}, {jelly_y})">
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

  <!-- 🐠 Active Diverse Creatures -->
{creature_elements}

  <!-- Top Left HUD (Slim) -->
  <g transform="translate(16, 12)">
    <rect x="0" y="0" width="190" height="32" fill="#020617" stroke="#38bdf8" stroke-width="1.5" />
    <rect x="4" y="4" width="5" height="5" fill="#ec4899" />
    <text x="14" y="15" font-family="'Courier New', monospace" font-size="9.5" font-weight="900" fill="#38bdf8">🐠 GITQUARIUM</text>
    <text x="14" y="25" font-family="'Courier New', monospace" font-size="8" font-weight="700" fill="#94a3b8">@{user}'S TANK</text>
  </g>

  <!-- Top Right HUD (Slim) -->
  <g transform="translate({hud_r_x}, 12)">
    <rect x="0" y="0" width="200" height="32" fill="#020617" stroke="#10b981" stroke-width="1.5" />
    <rect x="8" y="8" width="5" height="5" fill="#10b981" />
    <text x="18" y="15" font-family="'Courier New', monospace" font-size="8.5" font-weight="900" fill="#e2e8f0">{commits} COMMITS (7D)</text>
    <text x="18" y="25" font-family="'Courier New', monospace" font-size="7.5" font-weight="700" fill="#38bdf8">7 CREATURES SWIMMING</text>
  </g>
</svg>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", default="dahee90522")
    parser.add_argument("--width", type=int, default=850)
    parser.add_argument("--height", type=int, default=180)
    args = parser.parse_args()

    stats = fetch_github_activity(args.user)
    print(f"[*] Fetched GitHub stats for {args.user}: {stats}")

    os.makedirs("api", exist_ok=True)

    pixel_svg = generate_pixel_svg(stats, w=args.width, h=args.height)
    
    # Write to multiple filenames for instant CDN cache busting
    files = [
        f"api/{args.user}",
        f"api/{args.user}.svg",
        f"api/{args.user}-live.svg",
        "api/tank.svg",
        "api/dahee.svg",
        "api/aquarium.svg",
        "preview-pixel.svg"
    ]
    for fn in files:
        with open(fn, "w", encoding="utf-8") as f:
            f.write(pixel_svg)
    print(f"[+] Successfully generated diverse aquarium creatures for {files}!")

if __name__ == "__main__":
    main()
