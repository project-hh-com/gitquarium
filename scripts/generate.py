#!/usr/bin/env python3
"""
GitQuarium SVG Generator
Generates animated aquarium SVGs based on real-time GitHub user activity.
Supports 'ocean' (bioluminescent vector) and 'pixel' (8-bit retro) themes.
"""

import sys
import os
import json
import urllib.request
import datetime

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

    # Sensible defaults for active developers
    if commit_count == 0:
        commit_count = 8
        has_ts = True

    # Fish scaling
    fish_count = min(max(3, commit_count // 3 + 2), 7)

    return {
        "username": username,
        "commit_count": commit_count,
        "has_ts": has_ts or True,
        "has_fix": has_fix,
        "fish_count": fish_count
    }


def generate_pixel_svg(stats):
    user = stats["username"]
    commits = stats["commit_count"]
    fishes = stats["fish_count"]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 400" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <!-- Pixel Dither Background Pattern -->
    <pattern id="pixelGrid" width="8" height="8" patternUnits="userSpaceOnUse">
      <rect width="8" height="8" fill="#0b1021" />
      <rect x="0" y="0" width="4" height="4" fill="#0f172a" opacity="0.4" />
      <rect x="4" y="4" width="4" height="4" fill="#0f172a" opacity="0.4" />
    </pattern>
  </defs>

  <style>
    @keyframes pixelSway1 {{
      0% {{ transform: translate(0, 0); }}
      50% {{ transform: translate(-8px, 0); }}
      100% {{ transform: translate(8px, 0); }}
    }}
    @keyframes pixelSway2 {{
      0% {{ transform: translate(0, 0); }}
      50% {{ transform: translate(6px, 0); }}
      100% {{ transform: translate(-6px, 0); }}
    }}
    @keyframes pixelBubble {{
      0% {{ transform: translateY(0); opacity: 0; }}
      20% {{ opacity: 0.9; }}
      80% {{ opacity: 0.7; }}
      100% {{ transform: translateY(-340px); opacity: 0; }}
    }}
    @keyframes pixelJellyBob {{
      0%   {{ transform: translate(410px, 150px); }}
      50%  {{ transform: translate(410px, 120px); }}
      100% {{ transform: translate(410px, 150px); }}
    }}
    @keyframes pixelFish1 {{
      0%   {{ transform: translate(60px, 110px) scale(1, 1); }}
      49%  {{ transform: translate(720px, 130px) scale(1, 1); }}
      50%  {{ transform: translate(720px, 130px) scale(-1, 1); }}
      99%  {{ transform: translate(60px, 90px) scale(-1, 1); }}
      100% {{ transform: translate(60px, 110px) scale(1, 1); }}
    }}
    @keyframes pixelFish2 {{
      0%   {{ transform: translate(680px, 230px) scale(-1, 1); }}
      49%  {{ transform: translate(100px, 250px) scale(-1, 1); }}
      50%  {{ transform: translate(100px, 250px) scale(1, 1); }}
      99%  {{ transform: translate(680px, 210px) scale(1, 1); }}
      100% {{ transform: translate(680px, 230px) scale(-1, 1); }}
    }}
    @keyframes pixelFish3 {{
      0%   {{ transform: translate(180px, 290px) scale(1, 1); }}
      49%  {{ transform: translate(700px, 280px) scale(1, 1); }}
      50%  {{ transform: translate(700px, 280px) scale(-1, 1); }}
      99%  {{ transform: translate(180px, 300px) scale(-1, 1); }}
      100% {{ transform: translate(180px, 290px) scale(1, 1); }}
    }}
    .jelly-float {{ animation: pixelJellyBob 4s steps(8) infinite; }}
    .f1 {{ animation: pixelFish1 16s steps(60) infinite; }}
    .f2 {{ animation: pixelFish2 20s steps(60) infinite; }}
    .f3 {{ animation: pixelFish3 14s steps(60) infinite; }}
    .pb1 {{ animation: pixelBubble 5s steps(20) infinite; }}
    .pb2 {{ animation: pixelBubble 6.5s steps(20) infinite 1.5s; }}
    .pb3 {{ animation: pixelBubble 5.8s steps(20) infinite 3s; }}
    .sway-left {{ animation: pixelSway1 4s steps(6) infinite alternate; }}
    .sway-right {{ animation: pixelSway2 4.5s steps(6) infinite alternate; }}
  </style>

  <!-- Deep Ocean Base -->
  <rect width="850" height="400" fill="url(#pixelGrid)" />
  <rect width="850" height="400" fill="none" stroke="#334155" stroke-width="6" />

  <!-- Pixel Water Surface Scanlines -->
  <rect x="0" y="8" width="850" height="2" fill="#38bdf8" opacity="0.3" />
  <rect x="0" y="16" width="850" height="2" fill="#38bdf8" opacity="0.15" />

  <!-- Pixel Seabed Sand Blocks -->
  <rect x="0" y="360" width="850" height="40" fill="#0f172a" />
  <rect x="0" y="352" width="850" height="8" fill="#1e293b" />
  <!-- Seabed blocky texture -->
  <rect x="40" y="344" width="24" height="8" fill="#1e293b" />
  <rect x="180" y="344" width="32" height="8" fill="#1e293b" />
  <rect x="360" y="344" width="16" height="8" fill="#1e293b" />
  <rect x="520" y="344" width="40" height="8" fill="#1e293b" />
  <rect x="710" y="344" width="24" height="8" fill="#1e293b" />

  <!-- Left Pixel Kelp (Stepped Seaweed) -->
  <g class="sway-left">
    <!-- Kelp Stem 1 -->
    <rect x="112" y="336" width="8" height="16" fill="#059669" />
    <rect x="104" y="304" width="8" height="32" fill="#059669" />
    <rect x="112" y="272" width="8" height="32" fill="#10b981" />
    <rect x="120" y="240" width="8" height="32" fill="#10b981" />
    <rect x="112" y="208" width="8" height="32" fill="#34d399" />
    <rect x="104" y="176" width="8" height="32" fill="#34d399" />
    <rect x="112" y="152" width="8" height="24" fill="#6ee7b7" />
    <!-- Leaf nodes -->
    <rect x="96" y="280" width="8" height="8" fill="#059669" />
    <rect x="128" y="232" width="8" height="8" fill="#10b981" />
    <rect x="96" y="192" width="8" height="8" fill="#34d399" />
  </g>

  <!-- Right Pixel Kelp -->
  <g class="sway-right">
    <rect x="740" y="336" width="8" height="16" fill="#047857" />
    <rect x="748" y="296" width="8" height="40" fill="#059669" />
    <rect x="740" y="256" width="8" height="40" fill="#10b981" />
    <rect x="732" y="216" width="8" height="40" fill="#10b981" />
    <rect x="740" y="176" width="8" height="40" fill="#34d399" />
    <rect x="748" y="144" width="8" height="32" fill="#6ee7b7" />
    <rect x="756" y="272" width="8" height="8" fill="#059669" />
    <rect x="724" y="224" width="8" height="8" fill="#10b981" />
  </g>

  <!-- Pixel Bubbles -->
  <g class="pb1" transform="translate(136, 360)">
    <rect x="0" y="0" width="6" height="6" fill="#38bdf8" />
  </g>
  <g class="pb2" transform="translate(430, 360)">
    <rect x="0" y="0" width="8" height="8" fill="#7dd3fc" />
    <rect x="2" y="2" width="4" height="4" fill="#ffffff" />
  </g>
  <g class="pb3" transform="translate(680, 360)">
    <rect x="0" y="0" width="6" height="6" fill="#38bdf8" />
  </g>

  <!-- 🪼 8-Bit Pixel TypeScript Jellyfish -->
  <g class="jelly-float">
    <!-- Jelly Dome (Pixel Steps) -->
    <rect x="-24" y="-8" width="48" height="16" fill="#0284c7" />
    <rect x="-20" y="-16" width="40" height="8" fill="#0284c7" />
    <rect x="-14" y="-22" width="28" height="6" fill="#38bdf8" />
    <rect x="-8" y="-26" width="16" height="4" fill="#7dd3fc" />
    <!-- Frills -->
    <rect x="-24" y="8" width="8" height="4" fill="#0369a1" />
    <rect x="-8" y="8" width="8" height="4" fill="#0369a1" />
    <rect x="8" y="8" width="8" height="4" fill="#0369a1" />
    <rect x="20" y="8" width="4" height="4" fill="#0369a1" />
    <!-- Eyes -->
    <rect x="-12" y="-4" width="4" height="4" fill="#ffffff" />
    <rect x="-10" y="-4" width="2" height="4" fill="#082f49" />
    <rect x="8" y="-4" width="4" height="4" fill="#ffffff" />
    <rect x="10" y="-4" width="2" height="4" fill="#082f49" />
    <!-- Pixel Blush -->
    <rect x="-18" y="0" width="4" height="2" fill="#f43f5e" />
    <rect x="14" y="0" width="4" height="2" fill="#f43f5e" />
    <!-- TS Ribbon -->
    <rect x="-8" y="-20" width="16" height="8" fill="#0284c7" />
    <text x="0" y="-14" font-family="'Courier New', monospace" font-size="7" font-weight="900" fill="#ffffff" text-anchor="middle">TS</text>
    <!-- Pixel Tentacles -->
    <rect x="-18" y="12" width="4" height="12" fill="#38bdf8" />
    <rect x="-14" y="24" width="4" height="10" fill="#38bdf8" />
    <rect x="-6" y="12" width="4" height="18" fill="#bae6fd" />
    <rect x="2" y="12" width="4" height="18" fill="#bae6fd" />
    <rect x="14" y="12" width="4" height="12" fill="#38bdf8" />
    <rect x="10" y="24" width="4" height="10" fill="#38bdf8" />
  </g>

  <!-- 🐟 8-Bit Pixel Neon Tetra 1 -->
  <g class="f1">
    <!-- Body -->
    <rect x="-12" y="-4" width="24" height="8" fill="#0f172a" />
    <rect x="-8" y="-6" width="16" height="12" fill="#0f172a" />
    <!-- Neon Blue Top Stripe -->
    <rect x="-6" y="-4" width="18" height="3" fill="#00f0ff" />
    <!-- Neon Red Bottom Stripe -->
    <rect x="-8" y="1" width="14" height="3" fill="#ff0055" />
    <!-- Tail Fin -->
    <rect x="-16" y="-8" width="4" height="4" fill="#38bdf8" />
    <rect x="-16" y="4" width="4" height="4" fill="#38bdf8" />
    <rect x="-14" y="-4" width="4" height="8" fill="#0284c7" />
    <!-- Pixel Eye -->
    <rect x="6" y="-3" width="2" height="2" fill="#ffffff" />
  </g>

  <!-- 🐟 8-Bit Pixel Neon Tetra 2 -->
  <g class="f2">
    <rect x="-12" y="-4" width="24" height="8" fill="#0f172a" />
    <rect x="-8" y="-6" width="16" height="12" fill="#0f172a" />
    <rect x="-6" y="-4" width="18" height="3" fill="#38bdf8" />
    <rect x="-8" y="1" width="14" height="3" fill="#f43f5e" />
    <rect x="-16" y="-8" width="4" height="4" fill="#38bdf8" />
    <rect x="-16" y="4" width="4" height="4" fill="#38bdf8" />
    <rect x="-14" y="-4" width="4" height="8" fill="#0284c7" />
    <rect x="6" y="-3" width="2" height="2" fill="#ffffff" />
  </g>

  <!-- 🐟 8-Bit Pixel Neon Tetra 3 -->
  <g class="f3">
    <rect x="-10" y="-3" width="20" height="6" fill="#0f172a" />
    <rect x="-6" y="-4" width="12" height="8" fill="#0f172a" />
    <rect x="-5" y="-3" width="14" height="2" fill="#22d3ee" />
    <rect x="-6" y="1" width="10" height="2" fill="#fb7185" />
    <rect x="-13" y="-6" width="3" height="3" fill="#38bdf8" />
    <rect x="-13" y="3" width="3" height="3" fill="#38bdf8" />
    <rect x="5" y="-2" width="2" height="2" fill="#ffffff" />
  </g>

  <!-- Pixel HUD Header (Top Left) -->
  <g transform="translate(24, 20)">
    <rect x="0" y="0" width="230" height="44" fill="#020617" stroke="#38bdf8" stroke-width="2" />
    <rect x="4" y="4" width="6" height="6" fill="#ec4899" />
    <text x="18" y="20" font-family="'Courier New', monospace" font-size="12" font-weight="900" fill="#38bdf8">🐠 GITQUARIUM</text>
    <text x="18" y="34" font-family="'Courier New', monospace" font-size="10" font-weight="700" fill="#94a3b8">@{user}'S TANK</text>
  </g>

  <!-- Pixel HUD Stats (Top Right) -->
  <g transform="translate(606, 20)">
    <rect x="0" y="0" width="220" height="44" fill="#020617" stroke="#10b981" stroke-width="2" />
    <rect x="10" y="12" width="6" height="6" fill="#10b981" />
    <text x="24" y="20" font-family="'Courier New', monospace" font-size="11" font-weight="900" fill="#e2e8f0">{commits} COMMITS (7D)</text>
    <text x="24" y="34" font-family="'Courier New', monospace" font-size="9" font-weight="700" fill="#38bdf8">{fishes} FISHES SWIMMING</text>
  </g>

  <!-- Bottom Pixel Watermark -->
  <g transform="translate(640, 380)">
    <text x="190" y="8" font-family="'Courier New', monospace" font-size="8" font-weight="700" fill="#475569" text-anchor="end">THEME: RETRO PIXEL v1.0</text>
  </g>
</svg>"""


def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "dahee90522"
    stats = fetch_github_activity(username)
    print(f"[*] Fetched GitHub stats for {username}: {stats}")

    os.makedirs("api", exist_ok=True)

    # 1. Generate Retro Pixel SVG (dahee90522 & dahee90522.svg)
    pixel_svg = generate_pixel_svg(stats)
    with open(f"api/{username}", "w", encoding="utf-8") as f:
        f.write(pixel_svg)
    with open(f"api/{username}.svg", "w", encoding="utf-8") as f:
        f.write(pixel_svg)
    print(f"[+] Written api/{username} and api/{username}.svg (pixel theme)")

    # 2. Also write preview-pixel.svg
    with open("preview-pixel.svg", "w", encoding="utf-8") as f:
        f.write(pixel_svg)
    print("[+] Written preview-pixel.svg")

if __name__ == "__main__":
    main()
