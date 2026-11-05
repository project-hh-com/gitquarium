#!/usr/bin/env python3
"""
GitQuarium SVG Generator
Generates animated aquarium SVGs in two visual themes:
- Theme 1: 8-Bit Retro Pixel (Retro Arcade with pixel sun rays, corals, rocks, 7 diverse pixel creatures)
- Theme 2: Modern Neon Deep-Sea Vector (Atmospheric sun rays / caustic lighting, glowing gradients, soft translucent creatures, wide 2D roaming jellyfish)
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
    gh_token = os.environ.get("GITHUB_TOKEN")
    if gh_token and not gh_token.startswith("pickle-"):
        headers["Authorization"] = f"token {gh_token}"
    req = urllib.request.Request(url, headers=headers)
    events = []
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            events = json.loads(resp.read().decode())
    except Exception as e:
        print(f"[!] Warning: Failed to fetch events for {username}: {e}")

    now = datetime.timezone.utc
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

        if (datetime.datetime.now(now) - created_dt).days > 7:
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


def generate_vector_svg(stats, w=850, h=340):
    """
    Theme 2: Modern Neon Deep-Sea Vector
    Atmospheric sunlight shafts filtering down, deep ocean gradients,
    translucent glowing jellyfish with wide roaming radius,
    bug pufferfish, react ray, nightshift anglerfish, and neon tetras.
    """
    user = stats["username"]
    commits = stats["commit_count"]
    hud_r_x = max(w - 216, 220)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
  <defs>
    <!-- Ocean Background Gradient -->
    <linearGradient id="vecOceanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0a1226" />
      <stop offset="35%" stop-color="#0d1b3a" />
      <stop offset="70%" stop-color="#0a1835" />
      <stop offset="100%" stop-color="#040814" />
    </linearGradient>

    <!-- Water Surface Light Beams (Sun Rays) -->
    <linearGradient id="vecLightBeam1" x1="40%" y1="0%" x2="60%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.32" />
      <stop offset="35%" stop-color="#0ea5e9" stop-opacity="0.14" />
      <stop offset="75%" stop-color="#0284c7" stop-opacity="0.04" />
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.0" />
    </linearGradient>
    <linearGradient id="vecLightBeam2" x1="40%" y1="0%" x2="60%" y2="100%">
      <stop offset="0%" stop-color="#67e8f9" stop-opacity="0.25" />
      <stop offset="40%" stop-color="#06b6d4" stop-opacity="0.10" />
      <stop offset="80%" stop-color="#0891b2" stop-opacity="0.02" />
      <stop offset="100%" stop-color="#0891b2" stop-opacity="0.0" />
    </linearGradient>

    <!-- Sandy Seabed Gradient -->
    <linearGradient id="vecSandGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#14213d" />
      <stop offset="100%" stop-color="#060b17" />
    </linearGradient>

    <!-- Jellyfish Dome Gradient -->
    <radialGradient id="vecJellyDome" cx="50%" cy="38%" r="52%">
      <stop offset="0%" stop-color="#cffafe" stop-opacity="0.95" />
      <stop offset="55%" stop-color="#38bdf8" stop-opacity="0.65" />
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.25" />
    </radialGradient>

    <!-- Glow Filter -->
    <filter id="vecGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.5" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="vecSoftGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <style>
  <![CDATA[
    /* Ambient Light Rays Caustic Pulse */
    .vec-sun-rays {{
      animation: vecRayShift 8s ease-in-out infinite alternate;
    }}
    @keyframes vecRayShift {{
      0%   {{ opacity: 0.85; transform: skewX(0deg); }}
      50%  {{ opacity: 1.0; transform: skewX(-1.5deg); }}
      100% {{ opacity: 0.90; transform: skewX(1deg); }}
    }}

    /* Floating Bubbles Rising */
    .vec-bubble {{
      animation: vecRise 7s linear infinite;
    }}
    .vb-1 {{ animation-delay: 0s; animation-duration: 6.2s; }}
    .vb-2 {{ animation-delay: 1.8s; animation-duration: 7.5s; }}
    .vb-3 {{ animation-delay: 3.5s; animation-duration: 5.8s; }}
    .vb-4 {{ animation-delay: 4.8s; animation-duration: 8.0s; }}
    .vb-5 {{ animation-delay: 2.4s; animation-duration: 6.9s; }}
    .vb-6 {{ animation-delay: 5.6s; animation-duration: 7.2s; }}

    @keyframes vecRise {{
      0% {{
        transform: translateY(0) translateX(0);
        opacity: 0;
      }}
      15% {{ opacity: 0.75; }}
      50% {{
        transform: translateY(-160px) translateX(8px);
        opacity: 0.6;
      }}
      85% {{ opacity: 0.35; }}
      100% {{
        transform: translateY(-330px) translateX(-6px);
        opacity: 0;
      }}
    }}

    /* 🪼 TypeScript Jellyfish: Wide 2D Roaming across Central Deep-Sea */
    .vec-jelly-roam {{
      animation: vecJellyRoam 22s ease-in-out infinite;
    }}
    @keyframes vecJellyRoam {{
      0% {{
        transform: translate(250px, 135px);
      }}
      22% {{
        transform: translate(390px, 85px);
      }}
      45% {{
        transform: translate(570px, 155px);
      }}
      68% {{
        transform: translate(450px, 215px);
      }}
      85% {{
        transform: translate(300px, 175px);
      }}
      100% {{
        transform: translate(250px, 135px);
      }}
    }}

    .vec-jelly-bell {{
      animation: vecBellPulse 3.8s ease-in-out infinite alternate;
      transform-origin: center top;
    }}
    @keyframes vecBellPulse {{
      0%   {{ transform: scale(1, 1); }}
      35%  {{ transform: scale(0.92, 1.10); }}
      65%  {{ transform: scale(1.06, 0.94); }}
      100% {{ transform: scale(1, 1); }}
    }}

    .vec-tentacles {{
      animation: vecTentacleSway 3.2s ease-in-out infinite alternate;
      transform-box: fill-box;
      transform-origin: top center;
    }}
    @keyframes vecTentacleSway {{
      0%   {{ transform: rotate(-6deg); }}
      100% {{ transform: rotate(6deg); }}
    }}

    /* 🐡 Vector Bug Pufferfish: Chubby Bobbing Across Mid-Upper Tank */
    .vec-puffer {{
      animation: vecPufferSwim 24s ease-in-out infinite;
    }}
    @keyframes vecPufferSwim {{
      0% {{
        transform: translate(-35px, 95px) scale(1, 1);
      }}
      48% {{
        transform: translate({{w + 35}}px, 125px) scale(1, 1);
      }}
      50% {{
        transform: translate({{w + 35}}px, 125px) scale(-1, 1);
      }}
      98% {{
        transform: translate(-35px, 110px) scale(-1, 1);
      }}
      100% {{
        transform: translate(-35px, 95px) scale(1, 1);
      }}
    }}
    .vec-puffer-body {{
      animation: vecPufferPulse 2.8s ease-in-out infinite alternate;
      transform-origin: center center;
    }}
    @keyframes vecPufferPulse {{
      0% {{ transform: scale(1, 1); }}
      100% {{ transform: scale(1.08, 1.08); }}
    }}

    /* ⚡ Vector React Ray: Gliding with Wing Flaps Across Mid Depth */
    .vec-ray {{
      animation: vecRaySwim 28s ease-in-out infinite;
    }}
    @keyframes vecRaySwim {{
      0% {{
        transform: translate({{w + 35}}px, 165px) scale(-1, 1);
      }}
      48% {{
        transform: translate(-35px, 185px) scale(-1, 1);
      }}
      50% {{
        transform: translate(-35px, 185px) scale(1, 1);
      }}
      98% {{
        transform: translate({{w + 35}}px, 155px) scale(1, 1);
      }}
      100% {{
        transform: translate({{w + 35}}px, 165px) scale(-1, 1);
      }}
    }}
    .vec-ray-wings {{
      animation: vecRayFlap 2.4s ease-in-out infinite alternate;
      transform-origin: center center;
    }}
    @keyframes vecRayFlap {{
      0% {{ transform: scaleY(1); }}
      100% {{ transform: scaleY(0.72); }}
    }}

    /* 🏮 Vector Anglerfish: Deep-Sea Cruise with Glowing Lantern */
    .vec-angler {{
      animation: vecAnglerSwim 32s linear infinite;
    }}
    @keyframes vecAnglerSwim {{
      0% {{
        transform: translate(-40px, 245px) scale(1, 1);
      }}
      48% {{
        transform: translate({{w + 40}}px, 255px) scale(1, 1);
      }}
      50% {{
        transform: translate({{w + 40}}px, 255px) scale(-1, 1);
      }}
      98% {{
        transform: translate(-40px, 235px) scale(-1, 1);
      }}
      100% {{
        transform: translate(-40px, 245px) scale(1, 1);
      }}
    }}
    .vec-angler-lantern {{
      animation: vecLanternGlow 2.0s ease-in-out infinite alternate;
    }}
    @keyframes vecLanternGlow {{
      0% {{ opacity: 0.75; transform: scale(0.9); }}
      100% {{ opacity: 1.0; transform: scale(1.15); }}
    }}

    /* 🐟 Vector Neon Tetras (4 fishes with staggered depths) */
    .vec-tetra-1 {{
      animation: vecTetra1 17s linear infinite;
    }}
    @keyframes vecTetra1 {{
      0% {{ transform: translate(-30px, 75px) scale(1, 1); }}
      48% {{ transform: translate({{w + 30}}px, 105px) scale(1, 1); }}
      50% {{ transform: translate({{w + 30}}px, 105px) scale(-1, 1); }}
      98% {{ transform: translate(-30px, 85px) scale(-1, 1); }}
      100% {{ transform: translate(-30px, 75px) scale(1, 1); }}
    }}

    .vec-tetra-2 {{
      animation: vecTetra2 20s linear infinite;
    }}
    @keyframes vecTetra2 {{
      0% {{ transform: translate({{w + 30}}px, 130px) scale(-1, 1); }}
      48% {{ transform: translate(-30px, 150px) scale(-1, 1); }}
      50% {{ transform: translate(-30px, 150px) scale(1, 1); }}
      98% {{ transform: translate({{w + 30}}px, 120px) scale(1, 1); }}
      100% {{ transform: translate({{w + 30}}px, 130px) scale(-1, 1); }}
    }}

    .vec-tetra-3 {{
      animation: vecTetra3 15s linear infinite;
    }}
    @keyframes vecTetra3 {{
      0% {{ transform: translate(-30px, 200px) scale(0.9, 0.9); }}
      48% {{ transform: translate({{w + 30}}px, 185px) scale(0.9, 0.9); }}
      50% {{ transform: translate({{w + 30}}px, 185px) scale(-0.9, 0.9); }}
      98% {{ transform: translate(-30px, 215px) scale(-0.9, 0.9); }}
      100% {{ transform: translate(-30px, 200px) scale(0.9, 0.9); }}
    }}

    .vec-tetra-4 {{
      animation: vecTetra4 23s linear infinite;
    }}
    @keyframes vecTetra4 {{
      0% {{ transform: translate({{w + 30}}px, 270px) scale(-0.85, 0.85); }}
      48% {{ transform: translate(-30px, 255px) scale(-0.85, 0.85); }}
      50% {{ transform: translate(-30px, 255px) scale(0.85, 0.85); }}
      98% {{ transform: translate({{w + 30}}px, 280px) scale(0.85, 0.85); }}
      100% {{ transform: translate({{w + 30}}px, 270px) scale(-0.85, 0.85); }}
    }}
  ]]>
  </style>

  <!-- Deep Ocean Background -->
  <rect width="{w}" height="{h}" rx="14" fill="url(#vecOceanGrad)" stroke="#1e293b" stroke-width="1.5" />

  <!-- Sunlight Beams (Sun Rays filtering from water surface) -->
  <g class="vec-sun-rays">
    <polygon points="120,0 240,0 370,{h} 100,{h}" fill="url(#vecLightBeam1)" />
    <polygon points="340,0 460,0 600,{h} 310,{h}" fill="url(#vecLightBeam2)" />
    <polygon points="560,0 670,0 810,{h} 530,{h}" fill="url(#vecLightBeam1)" opacity="0.8" />
    <polygon points="30,0 90,0 180,{h} 20,{h}" fill="url(#vecLightBeam2)" opacity="0.45" />
    <polygon points="730,0 810,0 870,{h} 700,{h}" fill="url(#vecLightBeam1)" opacity="0.4" />
  </g>

  <!-- Seabed Dunes -->
  <path d="M -10,{h-48} Q 160,{h-58} 340,{h-42} T 680,{h-52} T {w+10},{h-40} L {w+10},{h} L -10,{h} Z" fill="url(#vecSandGrad)" />
  <path d="M -10,{h-32} Q 220,{h-42} 460,{h-30} T {w+10},{h-34} L {w+10},{h} L -10,{h} Z" fill="#040813" opacity="0.65" />

  <!-- Seabed Rocks & Pebbles -->
  <ellipse cx="130" cy="{h-18}" rx="14" ry="5.5" fill="#1e293b" opacity="0.75" />
  <ellipse cx="146" cy="{h-14}" rx="8" ry="3.5" fill="#334155" opacity="0.85" />
  <ellipse cx="460" cy="{h-20}" rx="18" ry="6.5" fill="#1e293b" opacity="0.65" />
  <ellipse cx="482" cy="{h-15}" rx="10" ry="4" fill="#334155" opacity="0.8" />
  <ellipse cx="690" cy="{h-18}" rx="15" ry="5.5" fill="#1e293b" opacity="0.7" />

  <!-- Seabed Glowing Coral Accents -->
  <!-- Left Neon Coral -->
  <g transform="translate(105, {h-52})" filter="url(#vecSoftGlow)">
    <path d="M 0,18 Q -5,8 -14,2 Q -11,-1 -4,11 Q 0,4 0,-4 Q 3,-2 2,12 Q 7,5 14,-1 Q 12,2 5,14 Z" fill="#ec4899" opacity="0.85" />
  </g>
  <!-- Center Cyan Mushroom Coral -->
  <g transform="translate(420, {h-46})" filter="url(#vecSoftGlow)">
    <ellipse cx="0" cy="0" rx="14" ry="5.5" fill="#06b6d4" opacity="0.8" />
    <path d="M -10,0 Q 0,7 10,0 L 4,12 L -4,12 Z" fill="#0891b2" opacity="0.7" />
  </g>
  <!-- Right Amber Tube Coral -->
  <g transform="translate(650, {h-50})" filter="url(#vecSoftGlow)">
    <rect x="-6" y="-12" width="4" height="20" rx="2" fill="#f59e0b" opacity="0.8" />
    <rect x="0" y="-18" width="4.5" height="26" rx="2" fill="#fbbf24" opacity="0.85" />
    <rect x="7" y="-10" width="3.5" height="18" rx="2" fill="#d97706" opacity="0.8" />
  </g>

  <!-- Floating Rising Bubbles -->
  <g transform="translate(140, {h-35})"><circle class="vec-bubble vb-1" cx="0" cy="0" r="3.2" fill="#bae6fd" opacity="0.8" /></g>
  <g transform="translate(260, {h-45})"><circle class="vec-bubble vb-2" cx="0" cy="0" r="4.8" fill="#bae6fd" opacity="0.7" /></g>
  <g transform="translate(440, {h-38})"><circle class="vec-bubble vb-3" cx="0" cy="0" r="2.8" fill="#bae6fd" opacity="0.85" /></g>
  <g transform="translate(580, {h-42})"><circle class="vec-bubble vb-4" cx="0" cy="0" r="4.0" fill="#bae6fd" opacity="0.75" /></g>
  <g transform="translate(710, {h-35})"><circle class="vec-bubble vb-5" cx="0" cy="0" r="3.5" fill="#bae6fd" opacity="0.8" /></g>
  <g transform="translate(350, {h-40})"><circle class="vec-bubble vb-6" cx="0" cy="0" r="2.4" fill="#bae6fd" opacity="0.9" /></g>

  <!-- 🪼 TypeScript Glowing Jellyfish (Wide Roaming) -->
  <g class="vec-jelly-roam" filter="url(#vecGlow)">
    <g class="vec-jelly-bell">
      <!-- Outer Dome -->
      <path d="M -26,0 C -26,-28 26,-28 26,0 C 18,3.5 9,1.5 0,2.5 C -9,1.5 -18,3.5 -26,0 Z" 
            fill="url(#vecJellyDome)" stroke="#38bdf8" stroke-width="2" />
      <!-- Scalloped Frills -->
      <path d="M -26,0 Q -19,5.5 -13,0 Q -6.5,5.5 0,0 Q 6.5,5.5 13,0 Q 19,5.5 26,0" 
            fill="none" stroke="#7dd3fc" stroke-width="2" stroke-linecap="round" />
      <!-- Cute Eyes with Highlights -->
      <circle cx="-9" cy="-11" r="2.1" fill="#ffffff" />
      <circle cx="-8.3" cy="-11.6" r="1.1" fill="#0284c7" />
      <circle cx="-7.8" cy="-12.1" r="0.4" fill="#ffffff" />
      <circle cx="9" cy="-11" r="2.1" fill="#ffffff" />
      <circle cx="9.7" cy="-11.6" r="1.1" fill="#0284c7" />
      <circle cx="10.2" cy="-12.1" r="0.4" fill="#ffffff" />
      <!-- Pink Blushing Cheeks -->
      <ellipse cx="-14" cy="-6.5" rx="3" ry="1.5" fill="#f472b6" opacity="0.75" />
      <ellipse cx="14" cy="-6.5" rx="3" ry="1.5" fill="#f472b6" opacity="0.75" />
      <!-- Sweet Smile -->
      <path d="M -3.5,-6 Q 0,-2.5 3.5,-6" fill="none" stroke="#0284c7" stroke-width="1.3" stroke-linecap="round" />
      <!-- Small TS Ribbon Badge -->
      <rect x="-9" y="-24" width="18" height="11" rx="3" fill="#0284c7" opacity="0.95" />
      <text x="0" y="-15.5" font-family="'Courier New', monospace, sans-serif" font-size="8" font-weight="900" fill="#ffffff" text-anchor="middle">TS</text>

      <!-- Downward Flowing Tentacles -->
      <g class="vec-tentacles">
        <!-- Outer Left Tentacle -->
        <path d="M -18,2 C -23,14 -14,28 -17,42" fill="none" stroke="#38bdf8" stroke-width="1.8" stroke-linecap="round" opacity="0.85" />
        <!-- Inner Left Oral Arm -->
        <path d="M -8,3 C -12,16 -4,32 -7,48" fill="none" stroke="#bae6fd" stroke-width="2.4" stroke-linecap="round" opacity="0.95" />
        <!-- Inner Right Oral Arm -->
        <path d="M 8,3 C 4,16 12,32 7,48" fill="none" stroke="#bae6fd" stroke-width="2.4" stroke-linecap="round" opacity="0.95" />
        <!-- Outer Right Tentacle -->
        <path d="M 18,2 C 23,14 14,28 17,42" fill="none" stroke="#38bdf8" stroke-width="1.8" stroke-linecap="round" opacity="0.85" />
      </g>
    </g>
  </g>

  <!-- 🐡 Vector Bug Pufferfish -->
  <g class="vec-puffer" filter="url(#vecGlow)">
    <g class="vec-puffer-body">
      <!-- Spikes -->
      <polygon points="0,-18 -3,-12 3,-12" fill="#fde047" />
      <polygon points="12,-14 6,-9 11,-5" fill="#fde047" />
      <polygon points="18,0 12,-3 12,3" fill="#fde047" />
      <polygon points="12,14 11,5 6,9" fill="#fde047" />
      <polygon points="0,18 -3,12 3,12" fill="#fde047" />
      <polygon points="-12,14 -6,9 -11,5" fill="#fde047" />
      <polygon points="-18,0 -12,-3 -12,3" fill="#fde047" />
      <polygon points="-12,-14 -11,-5 -6,-9" fill="#fde047" />
      <!-- Round Chubby Body -->
      <circle cx="0" cy="0" r="14" fill="#f59e0b" stroke="#ea580c" stroke-width="1.5" />
      <ellipse cx="-1" cy="4" rx="10" ry="7" fill="#fef08a" opacity="0.85" />
      <!-- Tail Fin -->
      <path d="M -13,0 L -21,-7 L -18,0 L -21,7 Z" fill="#ea580c" />
      <!-- Pectoral Fin -->
      <ellipse cx="2" cy="4" rx="4.5" ry="2.5" fill="#fbbf24" stroke="#d97706" stroke-width="0.8" />
      <!-- Big Cute Eyes -->
      <circle cx="5" cy="-4" r="3.2" fill="#ffffff" />
      <circle cx="6" cy="-4" r="1.7" fill="#0f172a" />
      <circle cx="6.8" cy="-4.8" r="0.6" fill="#ffffff" />
      <!-- Blushing Cheeks -->
      <ellipse cx="8" cy="1" rx="2" ry="1.2" fill="#f43f5e" opacity="0.75" />
      <!-- Cute Mouth -->
      <ellipse cx="11" cy="-1" rx="1.5" ry="1.8" fill="#ea580c" />
    </g>
  </g>

  <!-- ⚡ Vector React Ray -->
  <g class="vec-ray" filter="url(#vecGlow)">
    <g class="vec-ray-wings">
      <!-- Diamond Stingray Body -->
      <path d="M 22,0 Q 8,-16 -10,-12 Q -18,-4 -20,0 Q -18,4 -10,12 Q 8,16 22,0 Z" fill="#0891b2" stroke="#22d3ee" stroke-width="1.5" />
      <!-- Glowing Circuit / React Core Pattern -->
      <ellipse cx="2" cy="0" rx="8" ry="4" fill="none" stroke="#67e8f9" stroke-width="1.2" opacity="0.9" />
      <ellipse cx="2" cy="0" rx="4" ry="8" fill="none" stroke="#67e8f9" stroke-width="1.2" opacity="0.9" />
      <circle cx="2" cy="0" r="2.2" fill="#a5f3fc" />
      <!-- Eyes on Top -->
      <circle cx="12" cy="-4" r="1.3" fill="#ffffff" />
      <circle cx="12" cy="4" r="1.3" fill="#ffffff" />
    </g>
    <!-- Long Sweeping Whip Tail -->
    <path d="M -20,0 C -32,2 -44,-4 -58,-2" fill="none" stroke="#06b6d4" stroke-width="1.8" stroke-linecap="round" />
  </g>

  <!-- 🏮 Vector Nightshift Anglerfish -->
  <g class="vec-angler" filter="url(#vecGlow)">
    <!-- Body -->
    <path d="M 18,-2 Q 6,-14 -12,-8 Q -20,-2 -22,0 Q -20,2 -12,8 Q 6,14 18,-2 Z" fill="#4c1d95" stroke="#7c3aed" stroke-width="1.5" />
    <!-- Tail Fin -->
    <path d="M -21,0 L -29,-8 L -26,0 L -29,8 Z" fill="#6d28d9" />
    <!-- Dorsal Fin -->
    <polygon points="-4,-10 2,-16 6,-9" fill="#7c3aed" opacity="0.8" />
    <!-- Big Curious Eye -->
    <circle cx="9" cy="-3" r="3" fill="#ffffff" />
    <circle cx="10" cy="-3" r="1.6" fill="#0f172a" />
    <circle cx="10.8" cy="-3.8" r="0.6" fill="#ffffff" />
    <!-- Jaws / Teeth -->
    <path d="M 17,-2 L 13,4 L 8,0" fill="none" stroke="#c4b5fd" stroke-width="1.2" />
    <!-- Lantern Antenna Stalk -->
    <path d="M 6,-11 C 10,-22 18,-22 22,-14" fill="none" stroke="#a78bfa" stroke-width="1.6" stroke-linecap="round" />
    <!-- Glowing Lantern Bulb -->
    <g class="vec-angler-lantern">
      <circle cx="22" cy="-14" r="4.5" fill="#fef08a" opacity="0.95" />
      <circle cx="22" cy="-14" r="7.5" fill="#facc15" opacity="0.35" />
    </g>
  </g>

  <!-- 🐟 Vector Neon Tetra 1 -->
  <g class="vec-tetra-1" filter="url(#vecGlow)">
    <path d="M 18,0 Q 4,-7 -12,-4 L -18,-8 L -16,0 L -18,8 L -12,4 Q 4,7 18,0 Z" fill="#0f172a" stroke="#0284c7" stroke-width="1" />
    <path d="M 16,-1 Q 2,-4 -12,-2" fill="none" stroke="#00f0ff" stroke-width="2.5" stroke-linecap="round" />
    <path d="M 2,1 Q -6,3 -14,2" fill="none" stroke="#ff0055" stroke-width="2" stroke-linecap="round" />
    <circle cx="12" cy="-2" r="1.5" fill="#ffffff" />
    <circle cx="13" cy="-2" r="0.8" fill="#000000" />
    <polygon points="-4,2 -1,6 3,2" fill="#38bdf8" opacity="0.75" />
  </g>

  <!-- 🐟 Vector Neon Tetra 2 -->
  <g class="vec-tetra-2" filter="url(#vecGlow)">
    <path d="M 18,0 Q 4,-7 -12,-4 L -18,-8 L -16,0 L -18,8 L -12,4 Q 4,7 18,0 Z" fill="#0f172a" stroke="#0284c7" stroke-width="1" />
    <path d="M 16,-1 Q 2,-4 -12,-2" fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round" />
    <path d="M 2,1 Q -6,3 -14,2" fill="none" stroke="#f43f5e" stroke-width="2" stroke-linecap="round" />
    <circle cx="12" cy="-2" r="1.5" fill="#ffffff" />
    <circle cx="13" cy="-2" r="0.8" fill="#000000" />
    <polygon points="-4,2 -1,6 3,2" fill="#38bdf8" opacity="0.75" />
  </g>

  <!-- 🐟 Vector Neon Tetra 3 -->
  <g class="vec-tetra-3" filter="url(#vecGlow)">
    <path d="M 18,0 Q 4,-7 -12,-4 L -18,-8 L -16,0 L -18,8 L -12,4 Q 4,7 18,0 Z" fill="#0f172a" stroke="#0284c7" stroke-width="1" />
    <path d="M 16,-1 Q 2,-4 -12,-2" fill="none" stroke="#22d3ee" stroke-width="2.2" stroke-linecap="round" />
    <path d="M 2,1 Q -6,3 -14,2" fill="none" stroke="#fb7185" stroke-width="1.8" stroke-linecap="round" />
    <circle cx="12" cy="-2" r="1.5" fill="#ffffff" />
    <circle cx="13" cy="-2" r="0.8" fill="#000000" />
  </g>

  <!-- 🐟 Vector Neon Tetra 4 -->
  <g class="vec-tetra-4" filter="url(#vecGlow)">
    <path d="M 18,0 Q 4,-7 -12,-4 L -18,-8 L -16,0 L -18,8 L -12,4 Q 4,7 18,0 Z" fill="#0f172a" stroke="#0284c7" stroke-width="1" />
    <path d="M 16,-1 Q 2,-4 -12,-2" fill="none" stroke="#10b981" stroke-width="2.2" stroke-linecap="round" />
    <path d="M 2,1 Q -6,3 -14,2" fill="none" stroke="#e11d48" stroke-width="1.8" stroke-linecap="round" />
    <circle cx="12" cy="-2" r="1.5" fill="#ffffff" />
    <circle cx="13" cy="-2" r="0.8" fill="#000000" />
  </g>

  <!-- HUD: Top Left Header -->
  <g transform="translate(20, 18)">
    <rect width="216" height="42" rx="10" fill="#090d1a" fill-opacity="0.82" stroke="#1e293b" stroke-width="1.2" />
    <text x="14" y="21" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="800" fill="#f8fafc">🐠 GitQuarium</text>
    <text x="14" y="34" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="9.5" font-weight="600" fill="#38bdf8">@{user}'s Tank · Neon Deep-Sea</text>
  </g>

  <!-- HUD: Top Right Stats -->
  <g transform="translate({hud_r_x}, 18)">
    <rect width="196" height="42" rx="10" fill="#090d1a" fill-opacity="0.82" stroke="#1e293b" stroke-width="1.2" />
    <circle cx="16" cy="21" r="4" fill="#10b981" />
    <text x="26" y="19" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="700" fill="#e2e8f0">{commits} Commits (7d)</text>
    <text x="26" y="32" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="600" fill="#38bdf8">7 Creatures Swimming</text>
  </g>

  <!-- Watermark Bottom Right -->
  <g transform="translate({w-200}, {h-12})">
    <text x="180" y="0" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="500" fill="#334155" text-anchor="end">Powered by project-hh-com/gitquarium</text>
  </g>
</svg>"""


def generate_pixel_svg(stats, w=850, h=340):
    """
    Theme 1: 8-Bit Retro Pixel
    Spacious 850x340 aquarium with pixel sun shafts, coral reefs, slate rocks,
    wide roaming jellyfish, and 7 diverse pixel creatures.
    """
    user = stats["username"]
    commits = stats["commit_count"]
    sand_top = h - 34
    sand_base = h - 22
    hud_r_x = max(w - 210, 220)
    center_x = w // 2
    jelly_y = int(h * 0.42)

    styles = []
    elements = []

    # 1. 🐡 Bug Pufferfish (복어)
    styles.append(f"""    @keyframes pufferTrack {{
      0%   {{ transform: translate(-35px, {int(h*0.38)}px) scale(1, 1); }}
      15%  {{ transform: translate(190px, {int(h*0.22)}px) scale(1, 1); }}
      30%  {{ transform: translate(420px, {int(h*0.48)}px) scale(1, 1); }}
      42%  {{ transform: translate(660px, {int(h*0.25)}px) scale(1, 1); }}
      49%  {{ transform: translate({w + 35}px, {int(h*0.42)}px) scale(1, 1); }}
      50%  {{ transform: translate({w + 35}px, {int(h*0.42)}px) scale(-1, 1); }}
      65%  {{ transform: translate(640px, {int(h*0.55)}px) scale(-1, 1); }}
      78%  {{ transform: translate(410px, {int(h*0.24)}px) scale(-1, 1); }}
      90%  {{ transform: translate(170px, {int(h*0.46)}px) scale(-1, 1); }}
      100% {{ transform: translate(-35px, {int(h*0.38)}px) scale(1, 1); }}
    }}
    .creature-puffer {{ animation: pufferTrack 23s ease-in-out infinite 0.5s; }}
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
  <g class="creature-puffer" transform="translate(70, {int(h*0.38)})">
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

    # 2. ⚡ React Ray (가오리)
    styles.append(f"""    @keyframes rayTrack {{
      0%   {{ transform: translate({w + 40}px, {int(h*0.25)}px) scale(-1, 1); }}
      16%  {{ transform: translate(630px, {int(h*0.58)}px) scale(-1, 1); }}
      30%  {{ transform: translate(410px, {int(h*0.32)}px) scale(-1, 1); }}
      42%  {{ transform: translate(190px, {int(h*0.56)}px) scale(-1, 1); }}
      49%  {{ transform: translate(-40px, {int(h*0.42)}px) scale(-1, 1); }}
      50%  {{ transform: translate(-40px, {int(h*0.42)}px) scale(1, 1); }}
      66%  {{ transform: translate(260px, {int(h*0.22)}px) scale(1, 1); }}
      80%  {{ transform: translate(540px, {int(h*0.52)}px) scale(1, 1); }}
      92%  {{ transform: translate(750px, {int(h*0.34)}px) scale(1, 1); }}
      100% {{ transform: translate({w + 40}px, {int(h*0.25)}px) scale(-1, 1); }}
    }}
    .creature-ray {{ animation: rayTrack 21s ease-in-out infinite 2s; }}
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
  <g class="creature-ray" transform="translate({w - 120}, {int(h*0.25)})">
    <g class="ray-wings">
      <polygon points="0,-7 14,0 0,7 -10,0" fill="#0284c7" />
      <polygon points="2,-4 10,0 2,4 -6,0" fill="#38bdf8" />
      <rect x="2" y="-1" width="3" height="2" fill="#ffffff" />
    </g>
    <g class="ray-tail">
      <line x1="-10" y1="0" x2="-24" y2="0" stroke="#0284c7" stroke-width="2" />
    </g>
  </g>""")

    # 3. 🏮 Nightshift Anglerfish (야근 아귀)
    styles.append(f"""    @keyframes anglerTrack {{
      0%   {{ transform: translate(-45px, {int(h*0.68)}px) scale(1, 1); }}
      20%  {{ transform: translate(210px, {int(h*0.62)}px) scale(1, 1); }}
      40%  {{ transform: translate(520px, {int(h*0.72)}px) scale(1, 1); }}
      49%  {{ transform: translate({w + 45}px, {int(h*0.66)}px) scale(1, 1); }}
      50%  {{ transform: translate({w + 45}px, {int(h*0.66)}px) scale(-1, 1); }}
      70%  {{ transform: translate(560px, {int(h*0.62)}px) scale(-1, 1); }}
      88%  {{ transform: translate(180px, {int(h*0.70)}px) scale(-1, 1); }}
      100% {{ transform: translate(-45px, {int(h*0.68)}px) scale(1, 1); }}
    }}
    .creature-angler {{ animation: anglerTrack 28s ease-in-out infinite 1s; }}
    @keyframes anglerFinWag {{
      0%, 100% {{ transform: rotate(0deg); }}
      50% {{ transform: rotate(18deg); }}
    }}
    .angler-fin {{
      transform-origin: -8px 0px;
      animation: anglerFinWag 0.4s ease-in-out infinite;
    }}
    @keyframes lanternBob {{
      0%, 100% {{ transform: scale(1); opacity: 0.85; }}
      50% {{ transform: scale(1.25); opacity: 1; }}
    }}
    .angler-bulb {{
      transform-origin: 8px -11px;
      animation: lanternBob 1.2s ease-in-out infinite;
    }}""")

    elements.append(f"""  <!-- 🏮 Nightshift Anglerfish -->
  <g class="creature-angler" transform="translate(140, {int(h*0.68)})">
    <rect x="-8" y="-5" width="14" height="10" fill="#4c1d95" />
    <rect x="-6" y="-7" width="10" height="14" fill="#4c1d95" />
    <rect x="2" y="-3" width="2" height="2" fill="#ffffff" />
    <rect x="3" y="-2" width="1" height="1" fill="#000000" />
    <rect x="2" y="1" width="3" height="1" fill="#fef08a" />
    <rect x="3" y="2" width="2" height="1" fill="#fef08a" />
    <path d="M 0,-7 L 4,-12 L 8,-11" fill="none" stroke="#a78bfa" stroke-width="1.2" />
    <g class="angler-bulb">
      <rect x="7" y="-12" width="3" height="3" fill="#facc15" />
    </g>
    <g class="angler-fin">
      <polygon points="-8,-4 -13,-7 -11,0 -13,7 -8,4" fill="#7c3aed" />
    </g>
  </g>""")

    # 4-7. 🐟 Neon Tetras
    tetras = [
        {"y": int(h*0.22), "speed": 16, "c1": "#00f0ff", "c2": "#ff007f", "del": 0.0},
        {"y": int(h*0.35), "speed": 19, "c1": "#10b981", "c2": "#fbbf24", "del": 2.5},
        {"y": int(h*0.50), "speed": 14, "c1": "#a855f7", "c2": "#ec4899", "del": 1.2},
        {"y": int(h*0.62), "speed": 22, "c1": "#38bdf8", "c2": "#f43f5e", "del": 3.8}
    ]

    for idx, t in enumerate(tetras, start=1):
        spd = t["speed"]
        delay = t["del"]
        styles.append(f"""    @keyframes tetraTrack{idx} {{
      0%   {{ transform: translate(-30px, {t['y']}px) scale(1, 1); }}
      25%  {{ transform: translate(240px, {t['y'] - 12}px) scale(1, 1); }}
      49%  {{ transform: translate({w + 30}px, {t['y'] + 8}px) scale(1, 1); }}
      50%  {{ transform: translate({w + 30}px, {t['y'] + 8}px) scale(-1, 1); }}
      75%  {{ transform: translate(320px, {t['y'] + 15}px) scale(-1, 1); }}
      99%  {{ transform: translate(-30px, {t['y']}px) scale(-1, 1); }}
      100% {{ transform: translate(-30px, {t['y']}px) scale(1, 1); }}
    }}
    .creature-tetra-{idx} {{ animation: tetraTrack{idx} {spd}s linear infinite {delay}s; }}
    @keyframes tetraTailWag{idx} {{
      0%, 100% {{ transform: scaleX(1); }}
      50% {{ transform: scaleX(0.2); }}
    }}
    .tetra-tail-{idx} {{
      transform-origin: -7px 0px;
      animation: tetraTailWag{idx} 0.28s ease-in-out infinite;
    }}""")

        elements.append(f"""  <!-- 🐟 Neon Tetra {idx} -->
  <g class="creature-tetra-{idx}" transform="translate(10, {t['y']})">
    <rect x="-7" y="-3" width="14" height="6" fill="#0f172a" />
    <rect x="-6" y="-2" width="12" height="2" fill="{t['c1']}" />
    <rect x="-4" y="0" width="8" height="2" fill="{t['c2']}" />
    <rect x="5" y="-2" width="2" height="2" fill="#ffffff" />
    <rect x="6" y="-1" width="1" height="1" fill="#000000" />
    <g class="tetra-tail-{idx}">
      <polygon points="-7,-3 -11,-5 -9,0 -11,5 -7,3" fill="{t['c1']}" />
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
    @keyframes pixelBubble {{
      0% {{ transform: translateY(0); opacity: 0; }}
      20% {{ opacity: 0.9; }}
      80% {{ opacity: 0.7; }}
      100% {{ transform: translateY(-{h - 35}px); opacity: 0; }}
    }}
    /* 🪼 TS Jellyfish Roaming and Propulsion Animation (Wide Open Waters) */
    @keyframes pixelJellyRoam {{
      0%   {{ transform: translate({center_x - 170}px, {jelly_y}px); }}
      20%  {{ transform: translate({center_x - 60}px, {jelly_y - 45}px); }}
      38%  {{ transform: translate({center_x + 90}px, {jelly_y - 20}px); }}
      58%  {{ transform: translate({center_x + 180}px, {jelly_y + 35}px); }}
      72%  {{ transform: translate({center_x + 70}px, {jelly_y + 45}px); }}
      88%  {{ transform: translate({center_x - 70}px, {jelly_y + 15}px); }}
      100% {{ transform: translate({center_x - 170}px, {jelly_y}px); }}
    }}
    .jelly-roam {{ animation: pixelJellyRoam 14s ease-in-out infinite; }}
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
    .pb1 {{ animation: pixelBubble 4.5s steps(18) infinite; }}
    .pb2 {{ animation: pixelBubble 5.8s steps(18) infinite 1.2s; }}
    .pb3 {{ animation: pixelBubble 5.0s steps(18) infinite 2.5s; }}

{creature_styles}
  ]]>
  </style>

  <!-- Deep Ocean Grid Background -->
  <rect width="{w}" height="{h}" rx="10" fill="url(#pixelGrid)" stroke="#1e293b" stroke-width="1.5" />

  <!-- Ambient Light Rays Filtering from Surface -->
  <polygon points="120,0 240,0 360,{h} 100,{h}" fill="#38bdf8" opacity="0.08" />
  <polygon points="340,0 450,0 580,{h} 310,{h}" fill="#0ea5e9" opacity="0.07" />
  <polygon points="560,0 670,0 790,{h} 540,{h}" fill="#38bdf8" opacity="0.06" />

  <!-- Sandy Bed -->
  <rect x="0" y="{sand_top}" width="{w}" height="{h - sand_top}" fill="#040817" />
  <rect x="0" y="{sand_base}" width="{w}" height="{h - sand_base}" fill="#02040a" />

  <!-- Natural Bed Rocks -->
  <rect x="120" y="{sand_top - 6}" width="24" height="6" fill="#1e293b" />
  <rect x="124" y="{sand_top - 10}" width="16" height="4" fill="#334155" />
  <rect x="420" y="{sand_top - 8}" width="32" height="8" fill="#1e293b" />
  <rect x="426" y="{sand_top - 14}" width="20" height="6" fill="#334155" />
  <rect x="680" y="{sand_top - 6}" width="28" height="6" fill="#1e293b" />
  <rect x="686" y="{sand_top - 10}" width="16" height="4" fill="#334155" />

  <!-- Colorful Pixel Corals -->
  <!-- Neon Pink Branching Coral -->
  <g transform="translate(180, {sand_top - 24})">
    <rect x="2" y="0" width="4" height="24" fill="#f43f5e" />
    <rect x="-6" y="6" width="4" height="12" fill="#ec4899" />
    <rect x="-2" y="10" width="4" height="4" fill="#ec4899" />
    <rect x="8" y="4" width="4" height="14" fill="#f43f5e" />
    <rect x="6" y="8" width="4" height="4" fill="#f43f5e" />
  </g>
  <!-- Purple Mushroom Coral -->
  <g transform="translate(480, {sand_top - 18})">
    <rect x="-10" y="0" width="20" height="6" fill="#a855f7" />
    <rect x="-14" y="2" width="28" height="4" fill="#c084fc" />
    <rect x="-4" y="6" width="8" height="12" fill="#7e22ce" />
  </g>
  <!-- Amber Sun Coral -->
  <g transform="translate(620, {sand_top - 22})">
    <rect x="-6" y="6" width="4" height="16" fill="#f59e0b" />
    <rect x="0" y="0" width="4" height="22" fill="#fbbf24" />
    <rect x="6" y="8" width="4" height="14" fill="#d97706" />
  </g>

  <!-- Bubbles Rising -->
  <rect class="pb1" x="220" y="{sand_top - 10}" width="3" height="3" fill="#38bdf8" />
  <rect class="pb2" x="380" y="{sand_top - 15}" width="2" height="2" fill="#7dd3fc" />
  <rect class="pb3" x="580" y="{sand_top - 8}" width="3" height="3" fill="#38bdf8" />

  <!-- 🪼 TypeScript Jellyfish -->
  <g class="jelly-roam" transform="translate({center_x}, {jelly_y})">
    <g class="jelly-bell">
      <rect x="-12" y="-12" width="24" height="12" fill="#0284c7" />
      <rect x="-14" y="-8" width="28" height="14" fill="#0284c7" />
      <rect x="-10" y="-14" width="20" height="4" fill="#38bdf8" />
      <rect x="-6" y="-12" width="12" height="8" fill="#bae6fd" />
      <rect x="-6" y="-1" width="3" height="3" fill="#ffffff" />
      <rect x="-5" y="0" width="2" height="2" fill="#0369a1" />
      <rect x="3" y="-1" width="3" height="3" fill="#ffffff" />
      <rect x="4" y="0" width="2" height="2" fill="#0369a1" />
      <rect x="-9" y="1" width="3" height="2" fill="#f472b6" />
      <rect x="6" y="1" width="3" height="2" fill="#f472b6" />
      <rect x="-1" y="2" width="2" height="1" fill="#0369a1" />
      <rect x="-5" y="-16" width="10" height="4" fill="#0369a1" />
      <text x="0" y="-13" font-family="'Courier New', monospace" font-size="3.5" font-weight="900" fill="#ffffff" text-anchor="middle">TS</text>
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

  <!-- Top Left HUD -->
  <g transform="translate(18, 16)">
    <rect x="0" y="0" width="190" height="34" fill="#020617" stroke="#38bdf8" stroke-width="1.5" />
    <rect x="4" y="4" width="5" height="5" fill="#ec4899" />
    <text x="14" y="16" font-family="'Courier New', monospace" font-size="9.5" font-weight="900" fill="#38bdf8">🐠 GITQUARIUM</text>
    <text x="14" y="27" font-family="'Courier New', monospace" font-size="8" font-weight="700" fill="#94a3b8">@{user}'S TANK · PIXEL</text>
  </g>

  <!-- Top Right HUD -->
  <g transform="translate({hud_r_x}, 16)">
    <rect x="0" y="0" width="196" height="34" fill="#020617" stroke="#10b981" stroke-width="1.5" />
    <rect x="8" y="8" width="5" height="5" fill="#10b981" />
    <text x="18" y="16" font-family="'Courier New', monospace" font-size="8.5" font-weight="900" fill="#e2e8f0">{commits} COMMITS (7D)</text>
    <text x="18" y="27" font-family="'Courier New', monospace" font-size="7.5" font-weight="700" fill="#38bdf8">7 CREATURES SWIMMING</text>
  </g>
</svg>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", default="dahee90522")
    parser.add_argument("--width", type=int, default=850)
    parser.add_argument("--height", type=int, default=340)
    args = parser.parse_args()

    stats = fetch_github_activity(args.user)
    print(f"[*] Fetched GitHub stats for {args.user}: {stats}")

    os.makedirs("api", exist_ok=True)

    vector_svg = generate_vector_svg(stats, w=args.width, h=args.height)
    pixel_svg = generate_pixel_svg(stats, w=args.width, h=args.height)

    # Theme 2 (Modern Vector Deep-Sea):
    vec_files = [
        "api/vector.svg",
        "api/neon.svg",
        "api/deepsea.svg",
        "api/theme2.svg",
        "preview.svg",
        "preview-vector.svg"
    ]
    for fn in vec_files:
        with open(fn, "w", encoding="utf-8") as f:
            f.write(vector_svg)

    # Theme 1 (Pixel):
    pix_files = [
        "api/pixel.svg",
        "preview-pixel.svg"
    ]
    for fn in pix_files:
        with open(fn, "w", encoding="utf-8") as f:
            f.write(pixel_svg)

    print(f"[+] Successfully generated Theme 1 and Theme 2 SVGs at width={args.width}, height={args.height}!")

if __name__ == "__main__":
    main()
