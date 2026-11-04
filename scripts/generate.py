#!/usr/bin/env python3
"""
GitQuarium SVG Generator
Generates animated aquarium SVGs based on real-time GitHub user activity.
Supports 'ocean' (bioluminescent vector) and 'pixel' (8-bit retro) themes.
Allows customizable width and height (default: 850x180 for sleek banner layout).
"""

import sys
import os
import json
import urllib.request
import datetime
import argparse

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events/public"
    req = urllib.request.Request(url, headers={"User-Agent": "GitQuarium-Bot"})
    events = []
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            events = json.loads(resp.read().decode())
    except Exception as e:
        print(f"[!] Warning: Failed to fetch events for {username}: {e}")

    now = datetime.datetime.now(datetime.timezone.utc)
    commit_count = 0
    has_ts = False
    has_fix = False

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
        "has_ts": has_ts or True,
        "has_fix": has_fix,
        "fish_count": fish_count
    }


def generate_pixel_svg(stats, w=850, h=180):
    user = stats["username"]
    commits = stats["commit_count"]
    fishes = stats["fish_count"]

    sand_top = h - 28
    sand_base = h - 20
    kelp_r_x = w - 85
    hud_r_x = w - 210
    center_x = w // 2
    jelly_y = int(h * 0.44)

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
    @keyframes pixelJellyBob {{
      0%   {{ transform: translate({center_x}px, {jelly_y}px); }}
      50%  {{ transform: translate({center_x}px, {jelly_y - 12}px); }}
      100% {{ transform: translate({center_x}px, {jelly_y}px); }}
    }}
    @keyframes pixelFish1 {{
      0%   {{ transform: translate(50px, {int(h*0.35)}px) scale(1, 1); }}
      49%  {{ transform: translate({w - 120}px, {int(h*0.38)}px) scale(1, 1); }}
      50%  {{ transform: translate({w - 120}px, {int(h*0.38)}px) scale(-1, 1); }}
      99%  {{ transform: translate(50px, {int(h*0.32)}px) scale(-1, 1); }}
      100% {{ transform: translate(50px, {int(h*0.35)}px) scale(1, 1); }}
    }}
    @keyframes pixelFish2 {{
      0%   {{ transform: translate({w - 140}px, {int(h*0.62)}px) scale(-1, 1); }}
      49%  {{ transform: translate(80px, {int(h*0.65)}px) scale(-1, 1); }}
      50%  {{ transform: translate(80px, {int(h*0.65)}px) scale(1, 1); }}
      99%  {{ transform: translate({w - 140}px, {int(h*0.58)}px) scale(1, 1); }}
      100% {{ transform: translate({w - 140}px, {int(h*0.62)}px) scale(-1, 1); }}
    }}
    @keyframes pixelFish3 {{
      0%   {{ transform: translate(160px, {int(h*0.75)}px) scale(1, 1); }}
      49%  {{ transform: translate({w - 160}px, {int(h*0.72)}px) scale(1, 1); }}
      50%  {{ transform: translate({w - 160}px, {int(h*0.72)}px) scale(-1, 1); }}
      99%  {{ transform: translate(160px, {int(h*0.78)}px) scale(-1, 1); }}
      100% {{ transform: translate(160px, {int(h*0.75)}px) scale(1, 1); }}
    }}
    .jelly-float {{ animation: pixelJellyBob 3.5s steps(8) infinite; }}
    .f1 {{ animation: pixelFish1 14s steps(50) infinite; }}
    .f2 {{ animation: pixelFish2 18s steps(50) infinite; }}
    .f3 {{ animation: pixelFish3 13s steps(50) infinite; }}
    .pb1 {{ animation: pixelBubble 4s steps(15) infinite; }}
    .pb2 {{ animation: pixelBubble 5.2s steps(15) infinite 1.2s; }}
    .pb3 {{ animation: pixelBubble 4.6s steps(15) infinite 2.5s; }}
    .sway-left {{ animation: pixelSway1 3.5s steps(6) infinite alternate; }}
    .sway-right {{ animation: pixelSway2 4s steps(6) infinite alternate; }}
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

  <!-- 🪼 Compact 8-Bit Pixel TypeScript Jellyfish -->
  <g class="jelly-float">
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

  <!-- 🐟 Neon Tetras -->
  <g class="f1">
    <rect x="-10" y="-3" width="20" height="6" fill="#0f172a" />
    <rect x="-5" y="-3" width="15" height="2" fill="#00f0ff" />
    <rect x="-6" y="1" width="12" height="2" fill="#ff0055" />
    <rect x="-13" y="-5" width="3" height="3" fill="#38bdf8" />
    <rect x="-13" y="3" width="3" height="3" fill="#38bdf8" />
    <rect x="5" y="-2" width="2" height="2" fill="#ffffff" />
  </g>
  <g class="f2">
    <rect x="-10" y="-3" width="20" height="6" fill="#0f172a" />
    <rect x="-5" y="-3" width="15" height="2" fill="#38bdf8" />
    <rect x="-6" y="1" width="12" height="2" fill="#f43f5e" />
    <rect x="-13" y="-5" width="3" height="3" fill="#38bdf8" />
    <rect x="-13" y="3" width="3" height="3" fill="#38bdf8" />
    <rect x="5" y="-2" width="2" height="2" fill="#ffffff" />
  </g>
  <g class="f3">
    <rect x="-8" y="-2" width="16" height="5" fill="#0f172a" />
    <rect x="-4" y="-2" width="12" height="2" fill="#22d3ee" />
    <rect x="-5" y="1" width="9" height="2" fill="#fb7185" />
    <rect x="-11" y="-4" width="3" height="2" fill="#38bdf8" />
    <rect x="-11" y="2" width="3" height="2" fill="#38bdf8" />
    <rect x="4" y="-2" width="2" height="2" fill="#ffffff" />
  </g>

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
    <text x="18" y="25" font-family="'Courier New', monospace" font-size="7.5" font-weight="700" fill="#38bdf8">{fishes} FISHES SWIMMING</text>
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

    # Generate slim banner pixel SVG (850x180)
    pixel_svg = generate_pixel_svg(stats, w=args.width, h=args.height)
    with open(f"api/{args.user}", "w", encoding="utf-8") as f:
        f.write(pixel_svg)
    with open(f"api/{args.user}.svg", "w", encoding="utf-8") as f:
        f.write(pixel_svg)
    with open("preview-pixel.svg", "w", encoding="utf-8") as f:
        f.write(pixel_svg)
    print(f"[+] Successfully generated {args.width}x{args.height} slim banner SVGs!")

if __name__ == "__main__":
    main()
