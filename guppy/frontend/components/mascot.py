"""Guppy Mascot & Brand Assets.

Vector SVG illustrations for GUPPY (Clinical Pharmacy & Fornas 2025 Helper):
- Circular logo badge
- Mascot with speech bubble
- Mascot swimming for sidebar & empty states
"""

import html


def get_guppy_fish_svg(width: int = 48, height: int = 48, flipped: bool = False) -> str:
    """Return inline SVG of the cute orange and blue Guppy fish mascot."""
    transform = "transform=\"scale(-1, 1) translate(-120, 0)\"" if flipped else ""
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: inline-block; vertical-align: middle;">
  <g {transform}>
    <!-- Air Bubbles -->
    <circle cx="112" cy="38" r="4" fill="#38B6FF" fill-opacity="0.35" stroke="#38B6FF" stroke-width="1"/>
    <circle cx="106" cy="24" r="2.5" fill="#38B6FF" fill-opacity="0.3" stroke="#38B6FF" stroke-width="0.8"/>
    <circle cx="116" cy="18" r="1.5" fill="#38B6FF" fill-opacity="0.4"/>

    <!-- Tail Fin (Flowing Cyan/Blue) -->
    <path d="M38 60 C 22 42, 6 36, 4 50 C 2 62, 10 70, 4 82 C 14 84, 26 78, 38 64 Z" 
          fill="url(#tail_grad)" stroke="#0288D1" stroke-width="1.2" stroke-linejoin="round"/>
    <!-- Tail Fin Texture Lines -->
    <path d="M34 60 C 22 52, 14 48, 8 50" stroke="#E1F5FE" stroke-width="1" stroke-linecap="round" opacity="0.7"/>
    <path d="M34 62 C 20 64, 12 68, 6 72" stroke="#E1F5FE" stroke-width="1" stroke-linecap="round" opacity="0.7"/>
    <path d="M35 63 C 24 72, 16 76, 8 80" stroke="#E1F5FE" stroke-width="1" stroke-linecap="round" opacity="0.7"/>

    <!-- Dorsal Fin -->
    <path d="M52 44 C 54 28, 68 24, 76 34 C 70 38, 64 42, 60 45 Z" 
          fill="url(#dorsal_grad)" stroke="#0288D1" stroke-width="1.2" stroke-linejoin="round"/>

    <!-- Ventral Fin -->
    <path d="M54 74 C 52 86, 62 90, 68 82 C 64 78, 60 76, 58 74 Z" 
          fill="url(#dorsal_grad)" stroke="#0288D1" stroke-width="1" stroke-linejoin="round"/>

    <!-- Main Body (Warm Golden Orange) -->
    <path d="M36 60 C 38 42, 60 38, 82 44 C 98 48, 108 58, 106 66 C 104 74, 92 82, 78 82 C 58 82, 38 78, 36 60 Z" 
          fill="url(#body_grad)" stroke="#E65100" stroke-width="1.5" stroke-linejoin="round"/>

    <!-- Belly Accent (Soft Cream/Yellow) -->
    <path d="M48 68 C 60 78, 76 78, 88 74 C 94 70, 96 66, 94 65 C 84 72, 66 72, 48 68 Z" 
          fill="#FFF9C4" opacity="0.8"/>

    <!-- Pectoral Fin (Cyan) -->
    <path d="M62 60 C 66 54, 74 54, 76 60 C 74 68, 66 70, 60 64 Z" 
          fill="url(#pectoral_grad)" stroke="#0288D1" stroke-width="1" opacity="0.95"/>

    <!-- Smiling Eye -->
    <circle cx="92" cy="54" r="7.5" fill="#FFFFFF"/>
    <circle cx="93.5" cy="54" r="4.5" fill="#1A237E"/>
    <circle cx="95" cy="52.5" r="1.8" fill="#FFFFFF"/>

    <!-- Cute Smile -->
    <path d="M101 64 C 99 67, 96 67, 94 65" stroke="#B71C1C" stroke-width="1.4" stroke-linecap="round"/>

    <!-- Cheek Blush -->
    <ellipse cx="86" cy="63" rx="4" ry="2.5" fill="#FF5252" fill-opacity="0.35"/>
  </g>

  <!-- Gradients -->
  <defs>
    <linearGradient id="body_grad" x1="36" y1="40" x2="108" y2="80" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFB74D"/>
      <stop offset="45%" stop-color="#FFA726"/>
      <stop offset="100%" stop-color="#FF7043"/>
    </linearGradient>
    <linearGradient id="tail_grad" x1="4" y1="40" x2="38" y2="80" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#29B6F6"/>
      <stop offset="70%" stop-color="#0288D1"/>
      <stop offset="100%" stop-color="#01579B"/>
    </linearGradient>
    <linearGradient id="dorsal_grad" x1="52" y1="24" x2="76" y2="44" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#4FC3F7"/>
      <stop offset="100%" stop-color="#0288D1"/>
    </linearGradient>
    <linearGradient id="pectoral_grad" x1="60" y1="54" x2="76" y2="70" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#81D4FA"/>
      <stop offset="100%" stop-color="#039BE5"/>
    </linearGradient>
  </defs>
</svg>"""


def get_guppy_circle_logo_svg(size: int = 44) -> str:
    """Return circular badge logo with Guppy fish mascot matching mockup sidebar."""
    inner_svg = get_guppy_fish_svg(width=int(size * 0.8), height=int(size * 0.8))
    return f"""<div style="width: {size}px; height: {size}px; border-radius: 50%; background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%); display: inline-flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(0, 130, 138, 0.2); border: 2px solid #FFFFFF;">
  {inner_svg}
</div>"""


def get_welcome_banner_mascot_html() -> str:
    """Return mascot with speech bubble for the welcome banner."""
    fish_svg = get_guppy_fish_svg(width=88, height=88, flipped=False)
    return f"""<div style="display: flex; align-items: center; gap: 12px; justify-content: flex-end;">
  <div style="background: #FFFFFF; border: 1px solid #E2EAF3; border-radius: 12px; padding: 8px 14px; font-size: 0.82rem; font-weight: 600; color: #12345A; box-shadow: 0 2px 8px rgba(18, 52, 90, 0.06); max-width: 170px; line-height: 1.35; position: relative;">
    Cek cepat kesesuaian terapi JKN di satu tempat!
    <div style="position: absolute; right: -8px; top: 50%; transform: translateY(-50%); width: 0; height: 0; border-top: 6px solid transparent; border-bottom: 6px solid transparent; border-left: 8px solid #FFFFFF;"></div>
  </div>
  <div>
    {fish_svg}
  </div>
</div>"""


def get_sidebar_footer_html() -> str:
    """Return sidebar footer with mascot and clinical commitment tagline."""
    fish_svg = get_guppy_fish_svg(width=42, height=42, flipped=False)
    return f"""<div style="background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 12px 14px; margin-top: 24px; display: flex; align-items: center; gap: 10px;">
  <div style="flex-shrink: 0;">
    {fish_svg}
  </div>
  <div style="color: #BAE6FD; font-size: 0.74rem; line-height: 1.38; font-style: italic;">
    "Informasi tepat, keputusan lebih yakin untuk layanan JKN yang lebih baik."
  </div>
</div>"""
