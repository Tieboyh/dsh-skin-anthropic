#!/usr/bin/env python3
"""Generate src/tokens.css: the Anthropic paper palette expressed on the
DeepSeek Harness design-token layer.
"""
import re, pathlib, colorsys, json

LIGHT = {
 "--dsw-static-amber-100":"#fef5e7","--dsw-static-amber-400":"#f7ad31","--dsw-static-amber-500":"#f59e0b",
 "--dsw-static-amber-600":"#dd8629","--dsw-static-amber-900":"#27241f",
 "--dsw-static-blue-100":"#dbeafe","--dsw-static-blue-300":"#93c5fd","--dsw-static-blue-400":"#60a5fa",
 "--dsw-static-blue-450":"#4d93f8","--dsw-static-blue-50":"#eff6ff","--dsw-static-blue-500":"#3b82f6",
 "--dsw-static-blue-50p":"#eaf3ff","--dsw-static-blue-600":"#2563eb","--dsw-static-blue-75":"#e5f0ff",
 "--dsw-static-blue-800":"#1e40af","--dsw-static-blue-900":"#0e3074","--dsw-static-blue-950":"#172554",
 "--dsw-static-deepseek-100":"#e4edfd","--dsw-static-deepseek-200":"#d3e2ff","--dsw-static-deepseek-300":"#b7c8fe",
 "--dsw-static-deepseek-400":"#7aaaff","--dsw-static-deepseek-450":"#5686fe","--dsw-static-deepseek-50":"#edf3fe",
 "--dsw-static-deepseek-500":"#4176e6","--dsw-static-deepseek-600":"#4868b2","--dsw-static-deepseek-700-delete":"#2f4c8f",
 "--dsw-static-deepseek-800":"#34415b","--dsw-static-deepseek-900":"#283142",
 "--dsw-static-green-100":"#e6faed","--dsw-static-green-400":"#4ed17e","--dsw-static-green-500":"#22c55e",
 "--dsw-static-green-500-a08":"#22c55e14","--dsw-static-green-500-a12":"#22c55e1f","--dsw-static-green-900":"#233c2c",
 "--dsw-static-neutral-00":"#fff","--dsw-static-neutral-100":"#f5f5f5","--dsw-static-neutral-1000":"#000",
 "--dsw-static-neutral-150":"#ededed","--dsw-static-neutral-200":"#e5e5e5","--dsw-static-neutral-250":"#dcdcdc",
 "--dsw-static-neutral-300":"#d4d4d4","--dsw-static-neutral-400":"#a2a4a6","--dsw-static-neutral-50":"#fafafa",
 "--dsw-static-neutral-500":"#7f8287","--dsw-static-neutral-550":"#65676b","--dsw-static-neutral-600":"#545557",
 "--dsw-static-neutral-700":"#3c3c3d","--dsw-static-neutral-800":"#292929","--dsw-static-neutral-850":"#212123",
 "--dsw-static-neutral-900":"#0f0f0f",
 "--dsw-static-neutral-bluish-00":"#fff","--dsw-static-neutral-bluish-100":"#ebeef2",
 "--dsw-static-neutral-bluish-1000":"#0f1115","--dsw-static-neutral-bluish-150":"#e9ecf2",
 "--dsw-static-neutral-bluish-200":"#e1e5ee","--dsw-static-neutral-bluish-300":"#cfd3d6",
 "--dsw-static-neutral-bluish-310":"#cad2db","--dsw-static-neutral-bluish-400":"#adb2b8",
 "--dsw-static-neutral-bluish-50":"#f9fafb","--dsw-static-neutral-bluish-500":"#979da6",
 "--dsw-static-neutral-bluish-55":"#f5f7fa","--dsw-static-neutral-bluish-60":"#f5f6f7",
 "--dsw-static-neutral-bluish-600":"#81858c","--dsw-static-neutral-bluish-700":"#61666b",
 "--dsw-static-neutral-bluish-75":"#f1f3f5","--dsw-static-neutral-bluish-750":"#43454a",
 "--dsw-static-neutral-bluish-800":"#353638","--dsw-static-neutral-bluish-850":"#2c2c2e",
 "--dsw-static-neutral-bluish-875":"#232324","--dsw-static-neutral-bluish-90":"#edf0f4",
 "--dsw-static-neutral-bluish-900":"#1b1b1c","--dsw-static-neutral-bluish-950":"#151517",
 "--dsw-static-red-100":"#fee2e2","--dsw-static-red-400":"#f25a5a","--dsw-static-red-400-a12":"#f25a5a1f",
 "--dsw-static-red-50":"#fef2f2","--dsw-static-red-500":"#ef4444","--dsw-static-red-600":"#ec1313",
 "--dsw-static-red-600-a08":"#ec131314","--dsw-static-red-900":"#570c0c",
 "--dsw-static-violet-400":"#a78bfa","--dsw-static-violet-600":"#7c3aed",
}

def hex2rgb(h):
    h=h.lstrip('#'); 
    if len(h)==3: h=''.join(c*2 for c in h)
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

def rgb2hex(r): return '#%02x%02x%02x' % tuple(max(0,min(255,round(c))) for c in r)

def lightness(h):
    r,g,b=[c/255 for c in hex2rgb(h)]
    return colorsys.rgb_to_hls(r,g,b)[1]*100

ANTHRO_GRAY = ["#faf9f5","#f5f4ed","#f0eee6","#e8e6dc","#dedcd1","#d1cfc5","#c2c0b6",
               "#b0aea5","#9c9a92","#87867f","#73726c","#5e5d59","#4d4c48","#3d3d3a",
               "#30302e","#262624","#1f1e1d","#1a1918","#141413","#0d0d0c"]

CLAY  = ["#fdf3ef","#fbe6de","#f6d2c3","#f0bda8","#e9a68d","#e08b6e","#d97757",
         "#c6613f","#b0512f","#954226","#7a331d","#5f2616"]
ERROR = ["#fdf0ef","#f9dbd8","#f3bcb7","#ea9b93","#e07b71","#d16156","#bf4d43",
         "#a83f36","#8f322a","#752720","#5b1d17","#42140f"]
OLIVE = ["#f4f6ef","#e6ebdc","#d3ddc3","#bdcda6","#a7bc89","#8ea56e","#788c5d",
         "#64764c","#51603d","#3f4b2f","#2d3622","#1d2416"]
OCHRE = ["#fdf7ec","#faecd3","#f4d9ab","#ecc37f","#e2ab55","#d19743","#c08a3e",
         "#a57433","#886028","#6b4b1e","#4e3615","#33230d"]
IRIS  = ["#f4f2fb","#e6e1f7","#cfc7ef","#b4a9e6","#9789d9","#7a68c6","#6350b3",
         "#4a3aa7","#3d2f8a","#30246d","#241a51"]

def rung(ramp, h):
    L = lightness(h)
    return min(ramp, key=lambda c: abs(lightness(c)-L))

def map_value(token, value):
    m = re.match(r'^(#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}))([0-9a-fA-F]{2})?$', value)
    if not m: return value
    base, alpha = m.group(1), m.group(2)
    t = token
    if 'neutral' in t:            out = rung(ANTHRO_GRAY, base)
    elif 'blue' in t or 'deepseek' in t: out = rung(CLAY, base)
    elif 'green' in t:            out = rung(OLIVE, base)
    elif 'red' in t:              out = rung(ERROR, base)
    elif 'amber' in t:            out = rung(OCHRE, base)
    elif 'violet' in t:           out = rung(IRIS, base)
    else:                         out = rung(ANTHRO_GRAY, base)
    return out + (alpha or '')

EXPLICIT = {
 "--dsw-static-neutral-bluish-00":"#faf9f5",
 "--dsw-static-neutral-bluish-50":"#f5f4ed",
 "--dsw-static-neutral-bluish-55":"#f2f1e9",
 "--dsw-static-neutral-bluish-60":"#f0eee6",
 "--dsw-static-neutral-bluish-75":"#eeebe2",
 "--dsw-static-neutral-bluish-90":"#e8e6dc",
 "--dsw-static-neutral-bluish-100":"#e8e6dc",
 "--dsw-static-neutral-bluish-150":"#e2e0d5",
 "--dsw-static-neutral-bluish-200":"#dedcd1",
 "--dsw-static-neutral-bluish-300":"#d1cfc5",
 "--dsw-static-neutral-bluish-310":"#cdcbc0",
 "--dsw-static-neutral-bluish-400":"#b0aea5",
 "--dsw-static-neutral-bluish-500":"#9c9a92",
 "--dsw-static-neutral-bluish-600":"#87867f",
 "--dsw-static-neutral-bluish-700":"#73726c",
 "--dsw-static-neutral-bluish-750":"#5e5d59",
 "--dsw-static-neutral-bluish-800":"#4d4c48",
 "--dsw-static-neutral-bluish-850":"#3d3d3a",
 "--dsw-static-neutral-bluish-875":"#30302e",
 "--dsw-static-neutral-bluish-900":"#262624",
 "--dsw-static-neutral-bluish-950":"#1f1e1d",
 "--dsw-static-neutral-bluish-1000":"#141413",

 "--dsw-static-neutral-00":"#faf9f5",
 "--dsw-static-neutral-50":"#f5f4ed",
 "--dsw-static-neutral-100":"#f0eee6",
 "--dsw-static-neutral-150":"#e8e6dc",
 "--dsw-static-neutral-200":"#dedcd1",
 "--dsw-static-neutral-250":"#d1cfc5",
 "--dsw-static-neutral-300":"#c2c0b6",
 "--dsw-static-neutral-400":"#9c9a92",
 "--dsw-static-neutral-500":"#87867f",
 "--dsw-static-neutral-550":"#73726c",
 "--dsw-static-neutral-600":"#5e5d59",
 "--dsw-static-neutral-700":"#3d3d3a",
 "--dsw-static-neutral-800":"#262624",
 "--dsw-static-neutral-850":"#1f1e1d",
 "--dsw-static-neutral-900":"#141413",
 "--dsw-static-neutral-1000":"#141413",

 "--dsw-static-blue-500":"#d97757",
 "--dsw-static-blue-600":"#c6613f",
 "--dsw-static-blue-900":"#954226",
 "--dsw-static-deepseek-50":"#fdf3ef",
 "--dsw-static-deepseek-100":"#fbe6de",
 "--dsw-static-deepseek-200":"#f6d2c3",
 "--dsw-static-deepseek-500":"#d97757",
 "--dsw-static-deepseek-600":"#c6613f",
}

DARK_LADDER = {
 "--dsw-static-neutral-bluish-50":"#f0eee6",
 "--dsw-static-neutral-bluish-800":"#30302e",
 "--dsw-static-neutral-bluish-850":"#262624",
 "--dsw-static-neutral-bluish-875":"#1f1e1d",
 "--dsw-static-neutral-bluish-900":"#1a1918",
 "--dsw-static-neutral-bluish-950":"#141413",
}

ALIAS_LIGHT = {
 "--dsw-alias-bg-base":"#faf9f5",
 "--dsw-alias-bg-layer-1":"#fcfbf8",
 "--dsw-alias-bg-layer-2":"#ffffff",
 "--dsw-alias-bg-layer-3":"#ffffff",
 "--dsw-alias-bg-mask-1":"#1414133d",
 "--dsw-alias-bg-mask-2":"#1414131f",
 "--dsw-alias-bg-mask-3":"#1414137a",
 "--dsw-alias-bg-mask-drop":"#faf9f5b3",
 "--dsw-alias-bg-mask-photo":"#000000e0",
 "--dsw-alias-bg-skeleton":"#1414130a",
 "--dsw-alias-border-inverted":"#0000",
 "--dsw-alias-border-inverted2":"#0000",
 "--dsw-alias-border-l1":"#1414130a",
 "--dsw-alias-border-l2":"#1414131a",
 "--dsw-alias-border-l2-darkmode-thin":"#1414131a",
 "--dsw-alias-border-l3":"#1414131f",
 "--dsw-alias-border-l4":"#14141329",
 "--dsw-alias-brand-primary-new-colorprimary-new-color":"#141413",
 "--dsw-alias-button-tool-bar-fill":"#3d3d3a80",
 "--dsw-alias-button-tool-bar-fill-invisible":"#1414135c",
 "--dsw-alias-button-tool-bar-hover":"#3d3d3a99",
 "--dsw-alias-file-diff-added-bg":"#eef1e7",
 "--dsw-alias-file-diff-added-gutter":"#f4f6ef",
 "--dsw-alias-file-diff-added-marker":"#788c5d",
 "--dsw-alias-file-diff-deleted-bg":"#fbeeeb",
 "--dsw-alias-file-diff-deleted-gutter":"#fdf3f0",
 "--dsw-alias-file-diff-deleted-marker":"#bf4d43",
 "--dsw-alias-interactive-bg-active":"#1414131a",
 "--dsw-alias-interactive-bg-hover":"#1414130f",
 "--dsw-alias-interactive-bg-hover-accent":"#d9775724",
 "--dsw-alias-interactive-bg-hover-danger":"#bf4d430d",
 "--dsw-alias-label-deep-diving":"#c6613f",
 "--dsw-alias-label-deep-diving-shimmer":"#f0bda8",
 "--dsw-alias-label-shimmer":"rgba(217, 119, 87, 0.38)",
 "--dsw-alias-menu-group-header-fill":"#f5f4edf0",
 "--dsw-alias-onboarding-accent":"#d97757",
 "--dsw-linear-gradient-think":"linear-gradient(180deg, #faf9f5 20.19%, rgba(250, 249, 245, 0) 100%)",
 "--dsw-linear-think-select":"linear-gradient(180deg, #f0eee6 20.19%, rgba(240, 238, 230, 0) 100%)",
 "--dsw-menu-surface-fill":"#faf9f5f2",
 "--dsw-specific-input-major":"#ffffff",
 "--dsw-specific-sidebar-fill":"#f5f4ed",
}

ALIAS_DARK = {
 "--dsw-alias-bg-base":"#161514",
 "--dsw-alias-bg-layer-1":"#1c1b19",
 "--dsw-alias-bg-layer-2":"#22211f",
 "--dsw-alias-bg-layer-3":"#282725",
 "--dsw-alias-bg-mask-1":"#00000080",
 "--dsw-alias-bg-mask-2":"#0003",
 "--dsw-alias-bg-mask-3":"#0000007a",
 "--dsw-alias-bg-mask-drop":"#1f1e1db3",
 "--dsw-alias-bg-mask-photo":"#000000e0",
 "--dsw-alias-bg-skeleton":"#f0eee614",
 "--dsw-alias-border-inverted":"#f0eee60f",
 "--dsw-alias-border-inverted2":"#f0eee614",
 "--dsw-alias-border-l1":"#f0eee60f",
 "--dsw-alias-border-l2":"#f0eee61f",
 "--dsw-alias-border-l2-darkmode-thin":"#f0eee60f",
 "--dsw-alias-border-l3":"#f0eee629",
 "--dsw-alias-border-l4":"#f0eee633",
 "--dsw-alias-button-tool-bar-fill":"#4d4c4880",
 "--dsw-alias-button-tool-bar-fill-invisible":"#1414135c",
 "--dsw-alias-button-tool-bar-hover":"#4d4c4899",
 "--dsw-alias-file-diff-added-bg":"#223022",
 "--dsw-alias-file-diff-added-gutter":"#1a241a",
 "--dsw-alias-file-diff-added-marker":"#8ea56e",
 "--dsw-alias-file-diff-deleted-bg":"#33201c",
 "--dsw-alias-file-diff-deleted-gutter":"#261713",
 "--dsw-alias-file-diff-deleted-marker":"#d16156",
 "--dsw-alias-interactive-bg-active":"#f0eee624",
 "--dsw-alias-interactive-bg-hover":"#f0eee614",
 "--dsw-alias-interactive-bg-hover-accent":"#d977573d",
 "--dsw-alias-interactive-bg-hover-danger":"#d1615626",
 "--dsw-alias-label-deep-diving":"#e08b6e",
 "--dsw-alias-label-deep-diving-shimmer":"#f6d2c3",
 "--dsw-alias-label-shimmer":"rgba(233, 166, 141, 0.45)",
 "--dsw-alias-menu-group-header-fill":"#262624f0",
 "--dsw-linear-gradient-think":"linear-gradient(180deg, #161514 20.19%, rgba(22, 21, 20, 0) 100%)",
 "--dsw-linear-think-select":"linear-gradient(180deg, #22211f 20.19%, rgba(34, 33, 31, 0) 100%)",
 "--dsw-menu-surface-fill":"#262624ed",
 "--dsw-specific-input-major":"#201f1d",
 "--dsw-specific-sidebar-fill":"#111110",
}

# macOS vibrancy overrides: strip cold blue/purple sidebar washes & cold grey menus.
MACOS_LIGHT = {
 "--dsw-specific-menu":"rgba(250, 249, 245, 0.94)",
 "--dsw-specific-sidebar-glass-fill":"rgb(250 249 245 / 0.62)",
 "--dsw-specific-sidebar-glass-hover":"rgb(245 244 237 / 0.45)",
 "--dsw-specific-sidebar-tint":"color-mix(in srgb, var(--dsw-specific-sidebar-fill) 48%, transparent)",
 "--dsw-specific-sidebar-wash-bottom":"rgb(214 208 196 / 0.08)",
 "--dsw-specific-sidebar-wash-top":"rgb(250 249 245 / 0.08)",
}

MACOS_DARK = {
 "--dsw-specific-menu":"rgba(34, 33, 31, 0.94)",
 "--dsw-specific-sidebar-glass-fill":"rgb(240 238 230 / 0.10)",
 "--dsw-specific-sidebar-glass-hover":"rgb(240 238 230 / 0.16)",
 "--dsw-specific-sidebar-tint":"color-mix(in srgb, var(--dsw-specific-sidebar-fill) 56%, transparent)",
 "--dsw-specific-sidebar-wash-bottom":"rgb(20 20 19 / 0.12)",
 "--dsw-specific-sidebar-wash-top":"rgb(240 238 230 / 0.03)",
}

static = {t: map_value(t, v) for t, v in LIGHT.items()}
static.update(EXPLICIT)
dark_static = {**static, **DARK_LADDER}

# Calculate diffs
static_diff = {k: v for k, v in dark_static.items() if v != static.get(k)}
alias_diff = {k: v for k, v in ALIAS_DARK.items() if v != ALIAS_LIGHT.get(k)}

def block(static_map, alias_map, indent=4):
    out=[]
    for k in sorted(static_map):
        out.append(f"{' '*indent}{k}: {static_map[k]} !important;")
    if static_map and alias_map:
        out.append("")
    for k in sorted(alias_map):
        out.append(f"{' '*indent}{k}: {alias_map[k]} !important;")
    return "\n".join(out)

css = f"""/* dsh-skin-anthropic — generated by scripts/build-tokens.py. Do not edit by hand.
 *
 * Anthropic's public palette expressed on the --dsw-static-* ladder + CDS Surface 0-3.
 */
body[data-dsh-skin="anthropic"] {{
{block(static, ALIAS_LIGHT)}
    /* Restrained blue focus ring (kept non-!important so pointer-modality suppression still works). */
    --dsw-focus-ring-color: #2a78d6;
}}

body[data-dsh-skin="anthropic"][data-ds-dark-theme] {{
{block(static_diff, alias_diff)}
    --dsw-focus-ring-color: #6da7ec;
}}

html[data-platform='darwin'] body[data-dsh-skin="anthropic"] {{
{block({}, MACOS_LIGHT)}
}}

html[data-platform='darwin'] body[data-dsh-skin="anthropic"][data-ds-dark-theme] {{
{block({}, MACOS_DARK)}
}}
"""
base_dir = pathlib.Path(__file__).parent.parent
pathlib.Path(base_dir, 'src/tokens.css').write_text(css)
print(f'src/tokens.css updated (diff-based dark mode + Surface 0-3 + macOS vibrancy)')

# Finish: fold the stylesheets into the client bundle.
parts = [css]
for extra_name in ('src/sidebar.css', 'src/ergonomics.css'):
    extra_path = pathlib.Path(base_dir, extra_name)
    if extra_path.exists():
        parts.append(extra_path.read_text())
css = '\n'.join(parts)

template = pathlib.Path(base_dir, 'src/client.template.js').read_text()
marker = '/* __TOKENS_CSS__ */ ""'
bundle = template.replace(marker, json.dumps(css))
pathlib.Path(base_dir, 'client.js').write_text(bundle)
print(f'client.js written: {len(bundle)} bytes')
