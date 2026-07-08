from typing import Dict, List, Tuple
import html

# Common SVG elements (gradients, grid patterns, filters)
SVG_DEFS = """<defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#09080d" />
      <stop offset="100%" stop-color="#150f24" />
    </linearGradient>
    <linearGradient id="barGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#842cb3" />
      <stop offset="100%" stop-color="#39ff14" />
    </linearGradient>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#25163f" stroke-width="0.5" opacity="0.3"/>
    </pattern>
    <filter id="glow">
      <feGaussianBlur stdDeviation="1.5" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>"""

def create_terminal_header(width: int, title: str) -> str:
    """Generates the macOS-style window controls and title bar for the cyber terminal."""
    escaped_title = html.escape(title)
    return f"""
    <!-- Terminal Top Bar -->
    <rect x="1" y="1" width="{width - 2}" height="28" fill="#1b122e" rx="9" ry="9" />
    <rect x="1" y="15" width="{width - 2}" height="14" fill="#1b122e" /> 
    <line x1="1" y1="28" x2="{width - 1}" y2="28" stroke="#3c0d68" stroke-width="1.5" />
    <circle cx="15" cy="14" r="5" fill="#ff5f56" />
    <circle cx="30" cy="14" r="5" fill="#ffbd2e" />
    <circle cx="45" cy="14" r="5" fill="#27c93f" />
    <text x="70" y="18" font-family="'Courier New', Courier, monospace" font-size="11" fill="#ba75ff" font-weight="bold">{escaped_title}</text>
    """

def generate_profile_card(username: str, name: str, avatar_base64: str, followers: int, following: int, public_repos: int, created_at: str) -> str:
    """Generates a 380x180 profile analytics card."""
    width = 380
    height = 180
    
    escaped_username = html.escape(username)
    escaped_name = html.escape(name)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  {SVG_DEFS}
  <!-- Outer boundary -->
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="10" fill="url(#cardGrad)" stroke="#3c0d68" stroke-width="1.5" />
  
  <!-- Grid background overlay -->
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="10" fill="url(#grid)" />
  
  {create_terminal_header(width, "PROFILE_MONITOR v1.0.4")}
  
  <!-- Avatar image with clip path -->
  <clipPath id="avatar-clip">
    <circle cx="65" cy="105" r="38" />
  </clipPath>
  <circle cx="65" cy="105" r="40" fill="none" stroke="#39ff14" stroke-width="2" filter="url(#glow)" />
  <image href="{avatar_base64}" x="27" y="67" width="76" height="76" clip-path="url(#avatar-clip)" />
  
  <!-- Info Text -->
  <text x="130" y="65" font-family="'Segoe UI', sans-serif" font-weight="bold" font-size="16" fill="#39ff14" filter="url(#glow)">&gt; {escaped_username}</text>
  <text x="130" y="80" font-family="'Segoe UI', sans-serif" font-size="11" fill="#a59bb0">{escaped_name}</text>
  
  <g font-family="'Courier New', Courier, monospace" font-size="12" fill="#e4e4e7">
    <text x="130" y="105">Repos:     <tspan fill="#ba75ff" font-weight="bold">{public_repos}</tspan></text>
    <text x="130" y="123">Followers: <tspan fill="#ba75ff" font-weight="bold">{followers}</tspan></text>
    <text x="130" y="141">Following: <tspan fill="#ba75ff" font-weight="bold">{following}</tspan></text>
    <text x="130" y="159">Created:   <tspan fill="#a83ccc">{created_at}</tspan></text>
  </g>
  
  <!-- Glowing bottom border accent -->
  <line x1="1" y1="179" x2="379" y2="179" stroke="#39ff14" stroke-width="2" filter="url(#glow)" />
</svg>"""
    return svg

def generate_activity_card(username: str, total_contributions: int, stars_received: int, forks: int, public_repos: int) -> str:
    """Generates a 380x180 activity analytics card."""
    width = 380
    height = 180
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  {SVG_DEFS}
  <!-- Outer boundary -->
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="10" fill="url(#cardGrad)" stroke="#3c0d68" stroke-width="1.5" />
  
  <!-- Grid background overlay -->
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="10" fill="url(#grid)" />
  
  {create_terminal_header(width, "ACTIVITY_MONITOR // STATUS: ACTIVE")}
  
  <!-- Left Side: Contributions Metric -->
  <text x="30" y="60" font-family="'Courier New', Courier, monospace" font-size="10" fill="#a59bb0">[TOTAL CONTRIBUTIONS]</text>
  <text x="30" y="98" font-family="'Segoe UI', sans-serif" font-weight="bold" font-size="34" fill="#39ff14" filter="url(#glow)">{total_contributions}</text>
  
  <!-- Terminal Status Code -->
  <text x="30" y="125" font-family="'Courier New', Courier, monospace" font-size="10" fill="#a59bb0">SYS_STATUS: <tspan fill="#39ff14">SYS_OK</tspan></text>
  <text x="30" y="140" font-family="'Courier New', Courier, monospace" font-size="10" fill="#a59bb0">METRIC_SRC: <tspan fill="#ba75ff">GH_REST_API</tspan></text>
  
  <!-- Right Side: Stats Panel -->
  <rect x="200" y="45" width="150" height="110" rx="6" fill="#110a1f" stroke="#3c0d68" stroke-width="1" />
  <line x1="200" y1="81" x2="350" y2="81" stroke="#3c0d68" stroke-width="0.5" />
  <line x1="200" y1="118" x2="350" y2="118" stroke="#3c0d68" stroke-width="0.5" />
  
  <!-- Stars Row -->
  <text x="215" y="67" font-family="'Courier New', Courier, monospace" font-size="12" fill="#e4e4e7">★ Stars: <tspan fill="#39ff14" font-weight="bold">{stars_received}</tspan></text>
  
  <!-- Forks Row -->
  <text x="215" y="104" font-family="'Courier New', Courier, monospace" font-size="12" fill="#e4e4e7">⑂ Forks: <tspan fill="#ba75ff" font-weight="bold">{forks}</tspan></text>
  
  <!-- Repos Row -->
  <text x="215" y="140" font-family="'Courier New', Courier, monospace" font-size="12" fill="#e4e4e7">🖿 Repos: <tspan fill="#a83ccc" font-weight="bold">{public_repos}</tspan></text>
  
  <!-- Glowing bottom border accent -->
  <line x1="1" y1="179" x2="379" y2="179" stroke="#39ff14" stroke-width="2" filter="url(#glow)" />
</svg>"""
    return svg

def generate_languages_card(username: str, languages: Dict[str, float]) -> str:
    """Generates a 380x180 top languages analytics card."""
    width = 380
    height = 180
    
    # Get top 4 languages or show placeholder
    lang_items = list(languages.items())[:4]
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  {SVG_DEFS}
  <!-- Outer boundary -->
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="10" fill="url(#cardGrad)" stroke="#3c0d68" stroke-width="1.5" />
  
  <!-- Grid background overlay -->
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="10" fill="url(#grid)" />
  
  {create_terminal_header(width, "LANGUAGE_ANALYZER // RUNNING")}
  
  <!-- Languages List -->
  <g font-family="'Segoe UI', sans-serif">
  """
    
    if not lang_items:
        svg += f"""
        <text x="{width / 2}" y="105" font-family="'Courier New', Courier, monospace" font-size="14" fill="#a59bb0" text-anchor="middle">No language data found.</text>
        """
    else:
        for i, (lang, pct) in enumerate(lang_items):
            y_offset = 62 + (i * 28)
            y_bar_offset = 53 + (i * 28)
            escaped_lang = html.escape(lang)
            
            # Progress bar dimensions
            bg_bar_width = 160
            fill_bar_width = int(bg_bar_width * (pct / 100))
            
            svg += f"""
            <!-- Language {i+1}: {escaped_lang} -->
            <text x="30" y="{y_offset}" font-family="'Courier New', Courier, monospace" font-size="12" fill="#e4e4e7" font-weight="bold">{escaped_lang}</text>
            <text x="135" y="{y_offset}" font-family="'Courier New', Courier, monospace" font-size="11" fill="#ba75ff">{pct}%</text>
            
            <!-- Progress Bar -->
            <rect x="180" y="{y_bar_offset}" width="{bg_bar_width}" height="10" rx="5" fill="#110a1f" stroke="#3c0d68" stroke-width="1" />
            """
            
            if fill_bar_width > 0:
                svg += f"""
                <rect x="180" y="{y_bar_offset}" width="{fill_bar_width}" height="10" rx="5" fill="url(#barGrad)" />
                """
                
    svg += """
  </g>
  <!-- Glowing bottom border accent -->
  <line x1="1" y1="179" x2="379" y2="179" stroke="#39ff14" stroke-width="2" filter="url(#glow)" />
</svg>"""
    return svg

def generate_capsule_badge(label: str, value: str, label_width: int, value_width: int) -> str:
    """Generates a standard capsule badge with custom widths."""
    total_width = label_width + value_width
    height = 28
    
    escaped_label = html.escape(label)
    escaped_value = html.escape(value)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{height}" viewBox="0 0 {total_width} {height}">
  <defs>
    <filter id="badgeGlow">
      <feGaussianBlur stdDeviation="1" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <!-- Entire badge boundary -->
  <rect x="0.75" y="0.75" width="{total_width - 1.5}" height="{height - 1.5}" rx="5" fill="#150f24" stroke="#3c0d68" stroke-width="1.5" />
  
  <!-- Right side background (dark contrast) -->
  <path d="M {label_width} 1 L {total_width - 5} 1 A 4 4 0 0 1 {total_width - 1} 5 L {total_width - 1} {height - 5} A 4 4 0 0 1 {total_width - 5} {height - 1} L {label_width} {height - 1} Z" fill="#09080d" />
  
  <!-- Vertical separator -->
  <line x1="{label_width}" y1="1" x2="{label_width}" y2="{height - 1}" stroke="#3c0d68" stroke-width="1.5" />
  
  <!-- Left text (label) -->
  <text x="{label_width / 2}" y="18" font-family="'Courier New', Courier, monospace" font-size="11" fill="#ba75ff" font-weight="bold" text-anchor="middle">{escaped_label}</text>
  
  <!-- Right text (value) -->
  <text x="{label_width + value_width / 2}" y="18" font-family="'Courier New', Courier, monospace" font-size="11" fill="#39ff14" font-weight="bold" text-anchor="middle" filter="url(#badgeGlow)">{escaped_value}</text>
</svg>"""
    return svg
