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
    .creature-puffer {{ animation: pufferTrack 21s ease-in-out infinite 0.5s; }}
    @keyframes pufferTailWag {{
      0%, 100% {{ transform: scaleX(1); }}
      50% {{ transform: scaleX(0.2); }}
    }}
    .puffer-tail {{
      transform-origin: -8px 0px;
      animation: pufferTailWag 0.35s ease-in-out infinite;
    }}
    @keyframes pufferPulse {{
      0%, 100% {{ transform: scale(1, 1); }}
      50% {{ transform: scale(1.08, 1.08); }}
    }}
    .puffer-body {{
      transform-origin: 0px 0px;
      animation: pufferPulse 2.5s ease-in-out infinite;
    }}""")

    elements.append(f"""  <!-- 🐡 Bug Pufferfish -->
  <g class="creature-puffer" transform="translate(70, {int(h*0.42)})">
    <g class="puffer-body">
      <rect x="-8" y="-6" width="16" height="12" fill="#f59e0b" />
      <rect x="-6" y="-8" width="12" height="16" fill="#f59e0b" />
      <rect x="-4" y="2" width="8" height="4" fill="#fef3c7" />
      <rect x="4" y="-4" width="3" height="3" fill="#ffffff" />
      <rect x="5" y="-3" width="2" height="2" fill="#000000" />
      <rect x="-1" y="-10" width="3" height="2" fill="#d97706" />
      <rect x="-1" y="8" width="3" height="2" fill="#d97706" />
    </g>
    <g class="puffer-tail">
      <rect x="-11" y="-3" width="3" height="6" fill="#d97706" />
    </g>
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
    .creature-ray {{ animation: rayTrack 19s ease-in-out infinite 2s; }}
    @keyframes rayWingFlap {{
      0%, 100% {{ transform: scaleY(1); }}
      50% {{ transform: scaleY(0.42); }}
    }}
    .ray-wings {{
      transform-origin: 0px 0px;
      animation: rayWingFlap 0.9s ease-in-out infinite;
    }}
    @keyframes rayTailWave {{
      0%, 100% {{ transform: rotate(-8deg); }}
      50% {{ transform: rotate(8deg); }}
    }}
    .ray-tail {{
      transform-origin: -10px 0px;
      animation: rayTailWave 0.9s ease-in-out infinite 0.2s;
    }}""")

    elements.append(f"""  <!-- ⚡ React Ray -->
  <g class="creature-ray" transform="translate({w - 120}, {int(h*0.28)})">
    <g class="ray-wings">
      <polygon points="0,-7 14,0 0,7 -10,0" fill="#0284c7" />
      <polygon points="-2,-4 8,0 -2,4 -6,0" fill="#38bdf8" />
      <circle cx="4" cy="-2" r="1.2" fill="#ffffff" />
      <circle cx="4" cy="2" r="1.2" fill="#ffffff" />
    </g>
    <g class="ray-tail">
      <line x1="-10" y1="0" x2="-22" y2="0" stroke="#38bdf8" stroke-width="1.5" />
    </g>
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
    .creature-angler {{ animation: anglerTrack 24s ease-in-out infinite 3.5s; }}
    @keyframes anglerTailWag {{
      0%, 100% {{ transform: scaleX(1); }}
      50% {{ transform: scaleX(0.25); }}
    }}
    .angler-tail {{
      transform-origin: -9px 0px;
      animation: anglerTailWag 0.55s ease-in-out infinite;
    }}
    @keyframes lanternBob {{
      0%, 100% {{ transform: translateY(0) rotate(0deg); opacity: 1; }}
      50% {{ transform: translateY(-3px) rotate(6deg); opacity: 0.8; }}
    }}
    .angler-lantern {{
      transform-origin: 2px -5px;
      animation: lanternBob 1.6s ease-in-out infinite;
    }}""")

    elements.append(f"""  <!-- 🏮 Nightshift Anglerfish -->
  <g class="creature-angler" transform="translate(80, {int(h*0.69)})">
    <ellipse cx="0" cy="0" rx="9" ry="6" fill="#4c1d95" />
    <rect x="4" y="-2" width="2" height="2" fill="#ffffff" />
    <g class="angler-tail">
      <polygon points="-9,0 -14,-4 -14,4" fill="#5b21b6" />
    </g>
    <g class="angler-lantern">
      <path d="M 2 -5 Q 6 -11 9 -8" stroke="#a78bfa" stroke-width="1.5" fill="none" />
      <circle cx="9" cy="-8" r="2.5" fill="#fef08a" />
    </g>
  </g>""")

    # 4~7. 🐟 Agile Neon Tetras (4 colors, varied diagonal & undulating paths)
    tetras = [
        # (ty_base, dur, delay, c1, c2, rev, y_offsets, tail_speed)
        (int(h*0.30), 14, 0.0, '#00f0ff', '#ff0055', False, (-12, 14, -8), 0.22),
        (int(h*0.58), 16, 3.5, '#10b981', '#f59e0b', True, (16, -14, 10), 0.28),
        (int(h*0.42), 15, 6.0, '#a855f7', '#ec4899', False, (14, -16, 12), 0.25),
        (int(h*0.74), 18, 2.0, '#38bdf8', '#f43f5e', True, (-14, 12, -10), 0.30)
    ]

    for idx, (ty, dur, delay, c1, c2, rev, (dy1, dy2, dy3), tail_speed) in enumerate(tetras, start=1):
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
    .tetra-{idx} {{ animation: tetraTrack{idx} {dur}s ease-in-out infinite {delay}s; }}
    @keyframes tetraTailWag{idx} {{
      0%, 100% {{ transform: scaleX(1); }}
      50% {{ transform: scaleX(0.18); }}
    }}
    .tetra-tail-{idx} {{
      transform-origin: -10px 0px;
      animation: tetraTailWag{idx} {tail_speed}s ease-in-out infinite;
    }}""")

        elements.append(f"""  <!-- 🐟 Neon Tetra {idx} -->
  <g class="tetra-{idx}" transform="translate({x1}, {ty})">
    <rect x="-10" y="-3" width="20" height="6" fill="#0f172a" />
    <rect x="-5" y="-3" width="15" height="2" fill="{c1}" />
    <rect x="-6" y="1" width="12" height="2" fill="{c2}" />
    <rect x="5" y="-2" width="2" height="2" fill="#ffffff" />
    <g class="tetra-tail-{idx}">
      <rect x="-13" y="-5" width="3" height="3" fill="#38bdf8" />
      <rect x="-13" y="3" width="3" height="3" fill="#38bdf8" />
    </g>
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
    @keyframes jellyBellPulse {{
      0%, 100% {{ transform: scale(1, 1); }}
      35% {{ transform: scale(0.92, 1.14); }}
      65% {{ transform: scale(1.08, 0.88); }}
    }}
    .jelly-bell {{
      transform-origin: 0px 0px;
      animation: jellyBellPulse 1.8s ease-in-out infinite;
    }}
    @keyframes jellyLegsWaveL {{
      0%, 100% {{ transform: rotate(0deg) skewX(0deg) scaleY(1); }}
      40% {{ transform: rotate(-14deg) skewX(-10deg) scaleY(0.8); }}
      75% {{ transform: rotate(8deg) skewX(8deg) scaleY(1.05); }}
    }}
    .jelly-legs-outer-l {{
      transform-origin: -14px 9px;
      animation: jellyLegsWaveL 1.8s ease-in-out infinite;
    }}
    @keyframes jellyLegsWaveMid {{
      0%, 100% {{ transform: scaleY(1) skewX(0deg); }}
      40% {{ transform: scaleY(0.72) skewX(6deg); }}
      75% {{ transform: scaleY(1.12) skewX(-6deg); }}
    }}
    .jelly-legs-mid {{
      transform-origin: 0px 9px;
      animation: jellyLegsWaveMid 1.8s ease-in-out infinite 0.2s;
    }}
    @keyframes jellyLegsWaveR {{
      0%, 100% {{ transform: rotate(0deg) skewX(0deg) scaleY(1); }}
      40% {{ transform: rotate(14deg) skewX(10deg) scaleY(0.8); }}
      75% {{ transform: rotate(-8deg) skewX(-8deg) scaleY(1.05); }}
    }}
    .jelly-legs-outer-r {{
      transform-origin: 11px 9px;
      animation: jellyLegsWaveR 1.8s ease-in-out infinite 0.4s;
    }}
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

  <!-- 🪨 Seabed Rocks (Reef Stones) -->
  <polygon points="120,{sand_top} 128,{sand_top - 12} 144,{sand_top - 12} 152,{sand_top}" fill="#1e293b" />
  <polygon points="128,{sand_top - 12} 134,{sand_top - 12} 130,{sand_top - 6} 124,{sand_top - 6}" fill="#334155" />
  <ellipse cx="114" cy="{sand_top - 2}" rx="6" ry="4" fill="#334155" />

  <ellipse cx="325" cy="{sand_top - 3}" rx="14" ry="7" fill="#1e293b" />
  <ellipse cx="323" cy="{sand_top - 5}" rx="9" ry="4" fill="#334155" />
  <ellipse cx="343" cy="{sand_top - 1}" rx="5" ry="3" fill="#475569" />

  <polygon points="{w - 200},{sand_top} {w - 192},{sand_top - 10} {w - 176},{sand_top - 10} {w - 168},{sand_top}" fill="#1e293b" />
  <polygon points="{w - 192},{sand_top - 10} {w - 186},{sand_top - 10} {w - 182},{sand_top - 6} {w - 189},{sand_top - 6}" fill="#475569" />
  <circle cx="{w - 163}" cy="{sand_top - 2}" r="3" fill="#334155" />

  <!-- 🪸 Vibrant Coral Reefs -->
  <!-- 1. Left Branching Pink Coral -->
  <g transform="translate(185, {sand_top})">
    <rect x="-3" y="-16" width="6" height="16" fill="#f43f5e" />
    <rect x="-11" y="-20" width="8" height="5" fill="#f43f5e" />
    <rect x="-15" y="-26" width="5" height="8" fill="#fb7185" />
    <rect x="-16" y="-30" width="7" height="4" fill="#fecdd3" />
    <rect x="3" y="-22" width="8" height="5" fill="#f43f5e" />
    <rect x="9" y="-28" width="5" height="8" fill="#fb7185" />
    <rect x="8" y="-32" width="7" height="4" fill="#fecdd3" />
    <rect x="-4" y="-28" width="8" height="12" fill="#fb7185" />
    <rect x="-3" y="-34" width="6" height="6" fill="#fecdd3" />
  </g>

  <!-- 2. Center-Right Bioluminescent Purple Mushroom Coral -->
  <g transform="translate(485, {sand_top})">
    <path d="M -14 0 Q -14 -14 0 -14 Q 14 -14 14 0 Z" fill="#7c3aed" />
    <path d="M -9 -2 Q -9 -8 0 -8 Q 9 -8 9 -2" stroke="#38bdf8" stroke-width="1.5" fill="none" />
    <circle cx="0" cy="-11" r="2" fill="#38bdf8" />
  </g>

  <!-- 3. Right Sunset Orange Tube Coral -->
  <g transform="translate({w - 235}, {sand_top})">
    <rect x="-10" y="-6" width="20" height="6" fill="#c2410c" />
    <rect x="-8" y="-22" width="5" height="16" fill="#ea580c" />
    <ellipse cx="-5.5" cy="-22" rx="3.5" ry="2" fill="#fef08a" />
    <rect x="-2" y="-18" width="6" height="12" fill="#f97316" />
    <ellipse cx="1" cy="-18" rx="4" ry="2" fill="#fef08a" />
    <rect x="5" y="-14" width="5" height="8" fill="#fb923c" />
    <ellipse cx="7.5" cy="-14" rx="3.5" ry="2" fill="#fef08a" />
  </g>

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
    <g class="jelly-bell">
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
    </g>
    <g class="jelly-legs-outer-l">
      <rect x="-14" y="9" width="3" height="9" fill="#38bdf8" />
      <rect x="-11" y="18" width="3" height="7" fill="#38bdf8" />
    </g>
    <g class="jelly-legs-mid">
      <rect x="-4" y="9" width="3" height="14" fill="#bae6fd" />
      <rect x="2" y="9" width="3" height="14" fill="#bae6fd" />
    </g>
    <g class="jelly-legs-outer-r">
      <rect x="11" y="9" width="3" height="9" fill="#38bdf8" />
      <rect x="8" y="18" width="3" height="7" fill="#38bdf8" />
    </g>
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
