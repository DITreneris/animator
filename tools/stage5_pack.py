#!/usr/bin/env python3
"""Tier A1 Stage 5 Distribution Pack Exporter & Gate Checker.

Compiles a single episode (from 4 Stage 5 board PNGs, explicit frame paths, or an
approved 9:16 MP4 + optional POST.md / timing JSON) into an omnichannel demand pack:
  - panel_01.png .. panel_04.png  (1080x1350 4:5 uncropped comic slides)
  - panel_05_cta.png              (1080x1350 Prompt Anatomy takeaway slide for LinkedIn)
  - carousel_linkedin.pdf         (multi-page 1080x1350 PDF for LinkedIn document posts)
  - comic_grid_x.png              (2160x2700 4:5 2x2 newspaper comic page for X / blog)
  - POST_PACK.md + post_pack.json (channel-isolated UTMs, clean YouTube title, Related Video pill,
                                   pinned loop-bait comment, and Gate S5 audit report)

Fails (exit 1) on any Gate S5 violation:
  - S5-1 Loop-Safe Ending Gate: catches static closing cards / appended 4-5s bumpers
    that caused -29% to -38% tail retention cliffs on YouTube Shorts.
  - S5-2 YouTube Shorts Title Hygiene: blocks episode numbers (E06, Ep. 2), >2 hashtags,
    known typos (BOS -> BOSS), ALL-CAPS shouting, or >75-char truncation.
  - S5-3 Channel-Isolated UTM & Related-Video Gate: guarantees YouTube copy never leaks
    utm_source=tiktok/blog, every channel gets its own utm_source + utm_medium + utm_campaign,
    and Shorts specify a clickable Related Video pill target.
  - S5-4 Visual Panel Gate: verifies 4 distinct, non-blank 9:16 frames rendered whole without cropping.

Usage:
  python3 tools/stage5_pack.py --selftest
  python3 tools/stage5_pack.py --series hoodyz --slug just_one_line \\
      --title "He Asked AI for Just One Line" \\
      --video hoodyz/just-one-line/film/just_one_line.mp4 \\
      --times 0.15,6.8,11.2,15.6 \\
      --post-md hoodyz/just-one-line/film/POST.md \\
      --lesson "Scope-lock file budgets in the prompt before an agent touches your repo." \\
      --related-video "Prompt Anatomy: How to Scope-Lock Coding Agents (Long-form)" \\
      --out hoodyz/just-one-line/film/stage5_pack
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat

REPO_ROOT = Path(__file__).resolve().parent.parent
FONTS_DIR = REPO_ROOT / "fonts"

# --- Series themes (matching uptimez/src/brand.py & hoodyz paper-cutout palettes) ---
SERIES_THEMES: dict[str, dict[str, object]] = {
    "uptimez": {
        "label": "UPTIMEZ INC.",
        "tagline": "99.9% uptime. 0% findability.",
        "primary_tag": "#uptimez",
        "secondary_tag": "#cartoon",
        "paper": (245, 242, 235),       # #F5F2EB board paper
        "ink": (25, 26, 31),            # #191A1F ink outline
        "brand_bg": (31, 42, 68),       # #1F2A44 UptimeZ navy
        "accent": (43, 182, 115),       # #2BB673 UptimeZ pulse green
        "muted": (92, 98, 112),
        "card_bg": (255, 255, 255),
    },
    "hoodyz": {
        "label": "HOODYZ · ME + MY AI",
        "tagline": "Ask an AI to help. Watch it take your job.",
        "primary_tag": "#hoodyz",
        "secondary_tag": "#cartoon",
        "paper": (247, 245, 239),       # #F7F5EF warm comic sheet
        "ink": (20, 22, 27),            # #14161B bold cartoon ink
        "brand_bg": (27, 40, 56),       # #1B2838 Hoody navy
        "accent": (245, 158, 11),       # #F59E0B MY AI amber accent
        "muted": (88, 94, 108),
        "card_bg": (255, 255, 255),
    },
    "seashellz": {
        "label": "SEASHELLZ · NINE LAWS",
        "tagline": "The bugs do not get fixed. The bugs train you.",
        "primary_tag": "#seashellz",
        "secondary_tag": "#devhumor",
        "paper": (246, 243, 236),
        "ink": (20, 28, 36),
        "brand_bg": (19, 42, 56),
        "accent": (224, 109, 83),
        "muted": (88, 100, 110),
        "card_bg": (255, 255, 255),
    },
    "promptanatomy": {
        "label": "PROMPT ANATOMY",
        "tagline": "Field-tested prompt engineering & AI workflows.",
        "primary_tag": "#promptanatomy",
        "secondary_tag": "#aiworkflows",
        "paper": (247, 245, 239),
        "ink": (24, 24, 27),
        "brand_bg": (24, 24, 27),
        "accent": (37, 99, 235),
        "muted": (95, 99, 110),
        "card_bg": (255, 255, 255),
    },
}

KNOWN_TITLE_TYPOS: dict[str, str] = {
    "BOS": "BOSS",
    "TEH": "THE",
    "AI'S": "AIS",
    "RECIEVE": "RECEIVE",
    "DEFINATELY": "DEFINITELY",
    "OBSELETE": "OBSOLETE",
}

EPISODE_TOKEN_RE = re.compile(
    r"\b(?:E\d{1,3}|EP\.?\s*\d{1,3}|EPISODE\s+\d{1,3}|PART\s+\d{1,2})\b",
    re.IGNORECASE,
)
HASHTAG_RE = re.compile(r"(?:^|\s)(#[A-Za-z0-9_]+)")


@dataclass
class GateResult:
    code: str
    name: str
    passed: bool
    detail: str
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Fonts & vector drawing helpers
# ---------------------------------------------------------------------------

def load_font(filename: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        FONTS_DIR / filename,
        Path.home() / ".fonts" / filename,
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def draw_brand_mark(
    draw: ImageDraw.ImageDraw,
    series: str,
    x: int,
    y: int,
    size: int,
    theme: dict[str, object],
) -> None:
    """Draw a clean geometric series mark (no external assets required)."""
    bg = theme["brand_bg"]
    fg = theme["accent"]
    r = max(6, int(size * 0.22))
    draw.rounded_rectangle((x, y, x + size, y + size), radius=r, fill=bg)
    u = size / 100.0
    if series == "uptimez":
        pts = [
            (12, 58), (26, 58), (31, 50), (36, 64), (41, 58),
            (47, 58), (53, 26), (59, 72), (63, 58), (66, 58),
            (66, 40), (86, 40), (66, 70), (88, 70),
        ]
        xy = [(x + px * u, y + py * u) for px, py in pts]
        draw.line(xy, fill=fg, width=max(3, int(7.5 * u)), joint="curve")
    elif series == "hoodyz":
        # Robot visor + antenna dot
        vx0, vy0, vx1, vy1 = x + 20 * u, y + 34 * u, x + 80 * u, y + 76 * u
        draw.rounded_rectangle((vx0, vy0, vx1, vy1), radius=max(4, int(10 * u)), outline=(255, 255, 255), width=max(2, int(6 * u)))
        draw.line([(x + 50 * u, y + 18 * u), (x + 50 * u, y + 34 * u)], fill=(255, 255, 255), width=max(2, int(5 * u)))
        draw.ellipse((x + 43 * u, y + 11 * u, x + 57 * u, y + 25 * u), fill=fg)
        draw.ellipse((x + 33 * u, y + 48 * u, x + 43 * u, y + 60 * u), fill=fg)
        draw.ellipse((x + 57 * u, y + 48 * u, x + 67 * u, y + 60 * u), fill=fg)
    else:
        fnt = load_font("Inter-800.ttf", max(14, int(size * 0.44)))
        txt = "PA" if series == "promptanatomy" else "SZ"
        bb = draw.textbbox((0, 0), txt, font=fnt)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        draw.text((x + (size - tw) / 2 - bb[0], y + (size - th) / 2 - bb[1]), txt, font=fnt, fill=fg)


# ---------------------------------------------------------------------------
# Video inspection & Gate S5-1 (Loop-Safe Ending / Anti-Cliff Gate)
# ---------------------------------------------------------------------------

def probe_video_duration(video_path: Path) -> tuple[float, int, int]:
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height:format=duration",
        "-of", "json", str(video_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    info = json.loads(proc.stdout)
    dur = float(info["format"]["duration"])
    st = info["streams"][0]
    return dur, int(st["width"]), int(st["height"])


def extract_video_frame(video_path: Path, t_sec: float, scale: tuple[int, int] | None = None) -> Image.Image:
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{max(0.0, t_sec):.3f}", "-i", str(video_path), "-frames:v", "1"]
    if scale is not None:
        cmd += ["-vf", f"scale={scale[0]}:{scale[1]}"]
    cmd += ["-f", "image2pipe", "-vcodec", "png", "-"]
    proc = subprocess.run(cmd, capture_output=True, check=True)
    if not proc.stdout:
        # Fallback very close to EOF if exact seek hit past last packet
        cmd_eof = ["ffmpeg", "-v", "error", "-sseof", "-0.12", "-i", str(video_path), "-frames:v", "1"]
        if scale is not None:
            cmd_eof += ["-vf", f"scale={scale[0]}:{scale[1]}"]
        cmd_eof += ["-f", "image2pipe", "-vcodec", "png", "-"]
        proc = subprocess.run(cmd_eof, capture_output=True, check=True)
    return Image.open(io.BytesIO(proc.stdout)).convert("RGB")


def mean_rgb_diff(a: Image.Image, b: Image.Image) -> float:
    if a.size != b.size:
        b = b.resize(a.size, Image.Resampling.BILINEAR)
    stat = ImageStat.Stat(ImageChops.difference(a, b))
    return round(sum(stat.mean) / 3.0, 2)


def analyze_frames_loop_safety(
    f0: Image.Image,
    f_mid: Image.Image,
    tail_frames: Sequence[Image.Image],
    duration_sec: float,
    strict_shorts_runtime: bool = False,
) -> GateResult:
    """Core Gate S5-1 evaluator over sampled RGB frames.

    tail_frames corresponds to [-2.0s, -1.5s, -1.0s, -0.5s, -0.1s] before EOF.
    Catches two proven YouTube Shorts retention killers:
      1. Appended static bumper / outro card (final 1.5s completely frozen <1.5 diff,
         diverging from frame 0 so it does not form a hold-loop).
      2. Hard cut in the last 2.0s into a low-motion closing card (cut step >= 45
         followed by final 1.0s motion <= 5.8, matching Prompt Telephone v04.3's
         post card [62.74, 5.14, 5.11] which dropped retention -28.9% in the last 2.6s).
    """
    if os.environ.get("TAG") == "1":
        return GateResult(
            code="S5-1",
            name="Loop-Safe Ending Gate",
            passed=False,
            detail="TAG=1 environment flag is active; closing brand cards cause -29% to -38% Shorts tail cliffs.",
        )

    f_last = tail_frames[-1]
    seam_diff = mean_rgb_diff(f0, f_last)
    tail_steps = [mean_rgb_diff(tail_frames[i], tail_frames[i + 1]) for i in range(len(tail_frames) - 1)]
    last_1s_max = max(tail_steps[-2:]) if len(tail_steps) >= 2 else tail_steps[-1]
    last_15s_max = max(tail_steps[-3:]) if len(tail_steps) >= 3 else last_1s_max
    earlier_jump = max(tail_steps[:-2]) if len(tail_steps) >= 3 else 0.0
    cut_from_mid = mean_rgb_diff(f_mid, f_last)

    warnings: list[str] = []
    if duration_sec > 35.0:
        msg = (
            f"Runtime is {duration_sec:.1f}s (>35s Shorts sweet spot: 13-31s hit 900-5,654 views, "
            f"40-46s stalled at 264-397). Ship an 18-25s seamless-loop teaser linked via Related Video."
        )
        if strict_shorts_runtime:
            return GateResult("S5-1", "Loop-Safe Ending Gate", False, msg)
        warnings.append(msg)

    # Case A: Dead-frozen appended bumper (>1.5s near-zero motion, not matching frame 0)
    if last_15s_max < 1.8 and seam_diff > 14.0:
        return GateResult(
            code="S5-1",
            name="Loop-Safe Ending Gate",
            passed=False,
            detail=(
                f"Static outro bumper detected in final 1.5s (max step={last_15s_max:.2f}, "
                f"seam0_last={seam_diff:.2f}). Appended 4-5s bumpers drop end-retention to 12-25%."
            ),
            warnings=warnings,
        )

    # Case B: Hard cut in last 2s into a static closing card (e.g. closing social/post card)
    if earlier_jump >= 45.0 and last_1s_max <= 5.8 and seam_diff > 25.0:
        return GateResult(
            code="S5-1",
            name="Loop-Safe Ending Gate",
            passed=False,
            detail=(
                f"Closing-card tail cliff detected: hard cut ({earlier_jump:.1f}) into static final 1.0s "
                f"(steps={tail_steps[-2:]}, seam0_last={seam_diff:.1f}). Cut on active comedy beat instead."
            ),
            warnings=warnings,
        )

    if seam_diff <= 12.0:
        mode = "EXACT_SEAM_LOOP"
    elif seam_diff <= 32.0:
        mode = "VISUAL_ACTION_LOOP"
    else:
        mode = "ACTIVE_PAYOFF_CUT"
        if last_1s_max < 6.0 and cut_from_mid > 60.0:
            warnings.append(
                f"Low final-second motion ({last_1s_max:.1f}) with non-matching frame 0 ({seam_diff:.1f}); "
                "verify final beat does not hold on a static card."
            )

    return GateResult(
        code="S5-1",
        name="Loop-Safe Ending Gate",
        passed=True,
        detail=(
            f"{mode} (duration={duration_sec:.2f}s, seam0_last={seam_diff:.1f}, "
            f"tail_steps={tail_steps})"
        ),
        warnings=warnings,
    )


def check_video_loop_and_endcard(video_path: Path, strict_shorts_runtime: bool = False) -> GateResult:
    dur, _, _ = probe_video_duration(video_path)
    scale = (180, 320)
    f0 = extract_video_frame(video_path, 0.0, scale=scale)
    f_mid = extract_video_frame(video_path, dur * 0.5, scale=scale)
    span = min(2.0, max(0.4, dur * 0.45))
    offsets = [span, span * 0.75, span * 0.50, span * 0.25, min(0.1, span * 0.05)]
    tail = [extract_video_frame(video_path, max(0.0, dur - off), scale=scale) for off in offsets]
    return analyze_frames_loop_safety(f0, f_mid, tail, dur, strict_shorts_runtime=strict_shorts_runtime)


# ---------------------------------------------------------------------------
# Gate S5-2 (YouTube Shorts Title Hygiene) & Gate S5-3 (Channel-Isolated UTMs)
# ---------------------------------------------------------------------------

def format_youtube_shorts_title(clean_hook: str, series: str) -> str:
    theme = SERIES_THEMES[series]
    hook = re.sub(r"\s+", " ", clean_hook).strip()
    # Strip any trailing hashtags from caller hook so we append canonical max-2 tags cleanly
    hook_wo_tags = re.sub(r"(?:\s+#[A-Za-z0-9_]+)+\s*$", "", hook).strip()
    tags = [str(theme["primary_tag"]), str(theme["secondary_tag"])]
    candidate = f"{hook_wo_tags} {' '.join(tags)}"
    if len(candidate) > 75:
        candidate = f"{hook_wo_tags} {tags[0]}"
    return candidate


def check_youtube_title(full_title: str) -> GateResult:
    issues: list[str] = []
    tags = HASHTAG_RE.findall(full_title)
    if len(tags) > 2:
        issues.append(f"has {len(tags)} hashtags ({', '.join(tags)}); max 2 allowed (6-7 tags tanked CTR to 49 views)")

    if EPISODE_TOKEN_RE.search(full_title):
        issues.append("contains episode/part numbering (e.g. E06 / Ep. 2); standalone hooks convert 20x higher on Shorts")

    body_words = re.findall(r"[A-Za-z']+", re.sub(r"#[A-Za-z0-9_]+", "", full_title))
    for w in body_words:
        up = w.upper()
        if up in KNOWN_TITLE_TYPOS:
            issues.append(f"typo '{w}' -> '{KNOWN_TITLE_TYPOS[up]}'")

    alpha_chars = [ch for ch in re.sub(r"#[A-Za-z0-9_]+", "", full_title) if ch.isalpha()]
    if len(alpha_chars) >= 8:
        upper_ratio = sum(1 for ch in alpha_chars if ch.isupper()) / len(alpha_chars)
        if upper_ratio > 0.68:
            issues.append(f"ALL-CAPS title ({upper_ratio:.0%} uppercase); use sentence/title case like 'Make It Original!'")

    if len(full_title) > 75:
        issues.append(f"length is {len(full_title)} chars (>75 chars truncates on mobile Shorts shelf)")
    if len(full_title.strip()) < 10:
        issues.append("title is too short (<10 chars)")

    if issues:
        return GateResult("S5-2", "YouTube Shorts Title Hygiene", False, "; ".join(issues))
    return GateResult(
        "S5-2",
        "YouTube Shorts Title Hygiene",
        True,
        f'"{full_title}" ({len(full_title)} chars, {len(tags)} tags, 0 episode numbers/typos)',
    )


def build_channel_utms(base_url: str, slug: str) -> dict[str, str]:
    clean_slug = re.sub(r"[^a-z0-9_]+", "_", slug.strip().lower()).strip("_")
    if not clean_slug:
        raise ValueError("UTM campaign slug must be non-empty")

    parsed = urlparse(base_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(f"Invalid target URL: {base_url}")

    channels = {
        "youtube_shorts": ("youtube", "shorts_desc"),
        "youtube_related": ("youtube", "related_video"),
        "linkedin": ("linkedin", "carousel"),
        "x": ("x", "comic_strip"),
        "tiktok": ("tiktok", "short_desc"),
    }
    base_path = parsed.path if parsed.path else "/"
    base_params = [(k, v) for k, v in parse_qsl(parsed.query) if not k.startswith("utm_")]
    out: dict[str, str] = {}
    for key, (src, med) in channels.items():
        q = base_params + [
            ("utm_source", src),
            ("utm_medium", med),
            ("utm_campaign", clean_slug),
        ]
        out[key] = urlunparse(parsed._replace(path=base_path, query=urlencode(q)))
    return out


def check_channel_copy_isolation(sections: dict[str, str], related_video_spec: str) -> GateResult:
    """Verify every channel section contains ONLY its own utm_source and Shorts names a Related Video."""
    expected_source = {
        "youtube_shorts": "youtube",
        "linkedin": "linkedin",
        "x": "x",
        "tiktok": "tiktok",
    }
    issues: list[str] = []
    utm_re = re.compile(r"utm_source=([a-z0-9_-]+)", re.IGNORECASE)

    for section_key, want_src in expected_source.items():
        text = sections.get(section_key, "")
        found = [m.lower() for m in utm_re.findall(text)]
        if not found:
            issues.append(f"{section_key} is missing utm_source={want_src}")
        for got in found:
            if got != want_src:
                issues.append(f"{section_key} leaked wrong utm_source={got} (expected {want_src})")

    if not related_video_spec or len(related_video_spec.strip()) < 6:
        issues.append("YouTube Studio 'Related Video' pill target is empty (Shorts descriptions do not click on mobile)")

    if issues:
        return GateResult("S5-3", "Channel-Isolated UTM & Related-Video Gate", False, "; ".join(issues))
    return GateResult(
        "S5-3",
        "Channel-Isolated UTM & Related-Video Gate",
        True,
        f"4 channel blocks isolated (youtube/linkedin/x/tiktok) + Related Video pill wired -> '{related_video_spec}'",
    )


# ---------------------------------------------------------------------------
# 4-Panel Comic Carousel & X 2x2 Strip Renderer (Uncropped 9:16 inside 4:5)
# ---------------------------------------------------------------------------

def wrap_lines(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    normalized = re.sub(r"\s*—\s*", " — ", text)
    words = normalized.split()
    if not words:
        return []
    lines: list[str] = []
    cur = words[0]
    for w in words[1:]:
        trial = f"{cur} {w}"
        bb = draw.textbbox((0, 0), trial, font=font)
        if bb[2] - bb[0] <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def render_carousel_panel(
    frame_img: Image.Image,
    idx: int,
    total_story_panels: int,
    series: str,
    episode_title: str,
    beat_caption: str,
) -> Image.Image:
    """Render one 1080x1350 (4:5) LinkedIn/X slide keeping the 9:16 source 100% uncropped."""
    W, H = 1080, 1350
    theme = SERIES_THEMES[series]
    paper = theme["paper"]
    ink = theme["ink"]
    brand_bg = theme["brand_bg"]
    accent = theme["accent"]
    muted = theme["muted"]

    canvas = Image.new("RGB", (W, H), paper)
    draw = ImageDraw.Draw(canvas)

    f_series = load_font("Inter-800.ttf", 24)
    f_pill = load_font("Inter-800.ttf", 22)
    f_title = load_font("LilitaOne-Regular.ttf", 38)
    f_beat = load_font("Inter-700.ttf", 26)
    f_foot = load_font("Inter-700.ttf", 21)

    # Top header bar (y: 28..92)
    draw_brand_mark(draw, series, 48, 28, 52, theme)
    draw.text((114, 34), str(theme["label"]), font=f_series, fill=brand_bg)
    ep_clean = re.sub(r"(?:\s+#[A-Za-z0-9_]+)+\s*$", "", episode_title).strip()
    f_sub = load_font("Inter-700.ttf", 20)
    draw.text((114, 62), ep_clean[:48], font=f_sub, fill=muted)

    pill_txt = f"PANEL {idx} / {total_story_panels}"
    pbb = draw.textbbox((0, 0), pill_txt, font=f_pill)
    pw = (pbb[2] - pbb[0]) + 36
    px0 = W - 48 - pw
    draw.rounded_rectangle((px0, 34, W - 48, 78), radius=22, fill=brand_bg)
    draw.text((px0 + 18, 43), pill_txt, font=f_pill, fill=(255, 255, 255))

    # Central uncropped 9:16 viewport: height = 1088 -> width = 612 (exact 9:16!)
    has_caption = bool(beat_caption.strip())
    vp_h = 1040 if has_caption else 1104
    vp_w = int(round(vp_h * 9 / 16))
    vp_x = (W - vp_w) // 2
    vp_y = 104

    # Flat paper-cutout offset ink block + crisp white mat + 5px ink frame
    draw.rounded_rectangle(
        (vp_x + 8, vp_y + 8, vp_x + vp_w + 8, vp_y + vp_h + 8),
        radius=14,
        fill=ink,
    )
    resized = frame_img.convert("RGB").resize((vp_w, vp_h), Image.Resampling.LANCZOS)
    canvas.paste(resized, (vp_x, vp_y))
    draw.rounded_rectangle(
        (vp_x - 3, vp_y - 3, vp_x + vp_w + 3, vp_y + vp_h + 3),
        radius=12,
        outline=ink,
        width=6,
    )

    # Corner comic panel number badge (outside safe story zone, top-left of panel border)
    bx0, by0 = vp_x - 24, vp_y - 18
    draw.ellipse((bx0, by0, bx0 + 54, by0 + 54), fill=accent, outline=ink, width=4)
    n_txt = str(idx)
    nbb = draw.textbbox((0, 0), n_txt, font=f_title)
    draw.text(
        (bx0 + (54 - (nbb[2] - nbb[0])) / 2 - nbb[0], by0 + (54 - (nbb[3] - nbb[1])) / 2 - nbb[1] - 2),
        n_txt,
        font=f_title,
        fill=ink if series == "hoodyz" else (255, 255, 255),
    )

    # Optional beat caption strip under the frame
    if has_caption:
        lines = wrap_lines(draw, beat_caption.strip(), f_beat, W - 140)[:2]
        cy = vp_y + vp_h + 24
        for ln in lines:
            lbb = draw.textbbox((0, 0), ln, font=f_beat)
            lw = lbb[2] - lbb[0]
            draw.text(((W - lw) / 2, cy), ln, font=f_beat, fill=ink)
            cy += 34

    # Footer bar
    fy = H - 52
    draw.line([(48, fy - 12), (W - 48, fy - 12)], fill=(216, 212, 202), width=2)
    draw.text((48, fy), "promptanatomy.app", font=f_foot, fill=brand_bg)
    right_cue = "SWIPE FOR NEXT BEAT ->" if idx < total_story_panels else "SWIPE FOR PROMPT LESSON ->"
    rbb = draw.textbbox((0, 0), right_cue, font=f_foot)
    draw.text((W - 48 - (rbb[2] - rbb[0]), fy), right_cue, font=f_foot, fill=muted)

    return canvas


def render_cta_panel(
    series: str,
    episode_title: str,
    lesson_text: str,
    domain_display: str,
    pinned_question: str,
) -> Image.Image:
    """Render Slide 5 (1080x1350) takeaway card for LinkedIn PDF carousels."""
    W, H = 1080, 1350
    theme = SERIES_THEMES[series]
    paper = theme["paper"]
    ink = theme["ink"]
    brand_bg = theme["brand_bg"]
    accent = theme["accent"]
    muted = theme["muted"]

    canvas = Image.new("RGB", (W, H), paper)
    draw = ImageDraw.Draw(canvas)

    f_kicker = load_font("Inter-800.ttf", 24)
    f_head = load_font("LilitaOne-Regular.ttf", 58)
    f_body = load_font("Inter-700.ttf", 34)
    f_q = load_font("Inter-700.ttf", 28)
    f_cta = load_font("Inter-800.ttf", 32)
    f_small = load_font("Inter-700.ttf", 22)

    # Outer editorial card
    cx0, cy0, cx1, cy1 = 68, 76, W - 68, H - 76
    draw.rounded_rectangle((cx0 + 10, cy0 + 10, cx1 + 10, cy1 + 10), radius=24, fill=ink)
    draw.rounded_rectangle((cx0, cy0, cx1, cy1), radius=24, fill=(255, 255, 255), outline=ink, width=6)

    # Header band inside card
    draw.rounded_rectangle((cx0, cy0, cx1, cy0 + 150), radius=20, fill=brand_bg)
    draw.rectangle((cx0, cy0 + 120, cx1, cy0 + 150), fill=brand_bg)
    draw_brand_mark(draw, series, cx0 + 40, cy0 + 36, 76, theme)
    draw.text((cx0 + 138, cy0 + 44), "PROMPT ANATOMY TAKEAWAY", font=f_kicker, fill=accent)
    ep_clean = re.sub(r"(?:\s+#[A-Za-z0-9_]+)+\s*$", "", episode_title).strip()
    draw.text((cx0 + 138, cy0 + 82), ep_clean[:42], font=f_small, fill=(255, 255, 255))

    # Main Lesson Headline + Body
    y = cy0 + 206
    draw.text((cx0 + 48, y), "WHY THIS HAPPENS IN REAL AI WORK:", font=f_kicker, fill=muted)
    y += 52
    for ln in wrap_lines(draw, lesson_text, f_head, (cx1 - cx0) - 96)[:5]:
        draw.text((cx0 + 48, y), ln, font=f_head, fill=ink)
        y += 68

    # Comment prompt box
    if pinned_question.strip():
        y += 28
        qx0, qx1 = cx0 + 48, cx1 - 48
        q_lines = wrap_lines(draw, f"Question: {pinned_question.strip()}", f_q, (qx1 - qx0) - 48)[:3]
        qh = 44 + len(q_lines) * 38
        draw.rounded_rectangle((qx0, y, qx1, y + qh), radius=16, fill=paper, outline=ink, width=3)
        qy = y + 20
        for ln in q_lines:
            draw.text((qx0 + 24, qy), ln, font=f_q, fill=brand_bg)
            qy += 38

    # Bottom CTA button block pointing to clickable post link
    bx0, by0, bx1, by1 = cx0 + 48, cy1 - 190, cx1 - 48, cy1 - 54
    draw.rounded_rectangle((bx0 + 6, by0 + 6, bx1 + 6, by1 + 6), radius=18, fill=ink)
    draw.rounded_rectangle((bx0, by0, bx1, by1), radius=18, fill=accent, outline=ink, width=4)
    btn_fg = ink if series == "hoodyz" else (255, 255, 255)
    draw.text((bx0 + 34, by0 + 26), f"Try the interactive patterns -> {domain_display}", font=f_cta, fill=btn_fg)
    draw.text((bx0 + 34, by0 + 76), "Clickable link in the post caption above", font=f_small, fill=btn_fg)

    return canvas


def render_x_comic_grid(
    frames: Sequence[Image.Image],
    series: str,
    episode_title: str,
    beats: Sequence[str],
    domain_display: str,
) -> Image.Image:
    """Render a 2160x2700 (4:5) 2x2 newspaper-style 4-panel comic strip for X / blog."""
    W, H = 2160, 2700
    theme = SERIES_THEMES[series]
    paper = theme["paper"]
    ink = theme["ink"]
    brand_bg = theme["brand_bg"]
    accent = theme["accent"]
    muted = theme["muted"]

    canvas = Image.new("RGB", (W, H), paper)
    draw = ImageDraw.Draw(canvas)

    f_series = load_font("Inter-800.ttf", 34)
    f_title = load_font("LilitaOne-Regular.ttf", 64)
    f_num = load_font("LilitaOne-Regular.ttf", 44)
    f_beat = load_font("Inter-700.ttf", 30)
    f_foot = load_font("Inter-800.ttf", 32)

    # Masthead
    draw_brand_mark(draw, series, 84, 52, 86, theme)
    draw.text((192, 54), str(theme["label"]), font=f_series, fill=brand_bg)
    ep_clean = re.sub(r"(?:\s+#[A-Za-z0-9_]+)+\s*$", "", episode_title).strip()
    draw.text((192, 94), ep_clean[:52], font=f_title, fill=ink)

    # 2x2 grid of uncropped 9:16 panels: each panel 648 x 1152 (exact 9:16)
    pw, ph = 648, 1152
    col_x = [340, 1172]
    row_y = [196, 1428]

    for idx in range(4):
        c_idx = idx % 2
        r_idx = idx // 2
        x0 = col_x[c_idx]
        y0 = row_y[r_idx]

        draw.rounded_rectangle((x0 + 10, y0 + 10, x0 + pw + 10, y0 + ph + 10), radius=16, fill=ink)
        im = frames[idx].convert("RGB").resize((pw, ph), Image.Resampling.LANCZOS)
        canvas.paste(im, (x0, y0))
        draw.rounded_rectangle((x0 - 4, y0 - 4, x0 + pw + 4, y0 + ph + 4), radius=14, outline=ink, width=8)

        # Panel number circle
        bx, by = x0 - 28, y0 - 24
        draw.ellipse((bx, by, bx + 66, by + 66), fill=accent, outline=ink, width=5)
        nt = str(idx + 1)
        nbb = draw.textbbox((0, 0), nt, font=f_num)
        draw.text(
            (bx + (66 - (nbb[2] - nbb[0])) / 2 - nbb[0], by + (66 - (nbb[3] - nbb[1])) / 2 - nbb[1] - 2),
            nt,
            font=f_num,
            fill=ink if series == "hoodyz" else (255, 255, 255),
        )

        beat = beats[idx].strip() if idx < len(beats) else ""
        if beat:
            ln = wrap_lines(draw, beat, f_beat, pw)[0]
            lbb = draw.textbbox((0, 0), ln, font=f_beat)
            draw.text((x0 + (pw - (lbb[2] - lbb[0])) / 2, y0 + ph + 16), ln, font=f_beat, fill=ink)

    # Bottom masthead strip
    fy = H - 76
    draw.line([(84, fy - 18), (W - 84, fy - 18)], fill=(210, 205, 194), width=3)
    draw.text((84, fy), f"{theme['tagline']}", font=f_beat, fill=muted)
    rtxt = f"{domain_display}  ·  Watch the animated loop w/ sound"
    rbb = draw.textbbox((0, 0), rtxt, font=f_foot)
    draw.text((W - 84 - (rbb[2] - rbb[0]), fy - 2), rtxt, font=f_foot, fill=brand_bg)

    return canvas


# ---------------------------------------------------------------------------
# POST.md Parser & Pack Compiler
# ---------------------------------------------------------------------------

def parse_existing_post_md(post_md: Path | None) -> dict[str, str]:
    if post_md is None or not post_md.exists():
        return {}
    raw = post_md.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    m_cap = re.search(r"\*\*Caption:\*\*\s*(.+)", raw)
    if m_cap:
        out["caption"] = m_cap.group(1).strip()
    m_pin = re.search(r"\*\*Pinned comment:\*\*\s*(.+)", raw)
    if m_pin:
        out["pinned_comment"] = m_pin.group(1).strip()
    m_tags = re.search(r"\*\*Hashtags:\*\*\s*(.+)", raw)
    if m_tags:
        out["hashtags"] = m_tags.group(1).strip()
    return out


def check_panels_integrity(frames: Sequence[Image.Image]) -> GateResult:
    if len(frames) != 4:
        return GateResult("S5-4", "Visual Panel Gate", False, f"Expected 4 panels, got {len(frames)}")
    issues: list[str] = []
    for idx, im in enumerate(frames, start=1):
        w, h = im.size
        ratio = w / max(1, h)
        if not (0.50 <= ratio <= 0.62):
            issues.append(f"panel {idx} size {w}x{h} is not 9:16 vertical ({ratio:.3f})")
        st = ImageStat.Stat(im.convert("RGB"))
        if max(st.stddev) < 4.0:
            issues.append(f"panel {idx} looks blank/flat (stddev={max(st.stddev):.2f})")
    for i in range(3):
        d = mean_rgb_diff(frames[i], frames[i + 1])
        if d < 1.5:
            issues.append(f"panel {i + 1} and panel {i + 2} are near-identical (diff={d:.2f})")
    if issues:
        return GateResult("S5-4", "Visual Panel Gate", False, "; ".join(issues))
    sizes = ", ".join(f"{im.size[0]}x{im.size[1]}" for im in frames)
    return GateResult("S5-4", "Visual Panel Gate", True, f"4 distinct 9:16 source frames verified ({sizes}), rendered 100% uncropped")


def pick_default_times(video_path: Path) -> list[float]:
    dur, _, _ = probe_video_duration(video_path)
    cuts_json = video_path.parent / "cuts.json"
    if cuts_json.exists():
        cuts = json.loads(cuts_json.read_text(encoding="utf-8"))
        if isinstance(cuts, list) and len(cuts) >= 4:
            # Pick Hook (first cut midpoint), Escalation, Turn, and Final Loop Beat
            indices = [0, len(cuts) // 3, (2 * len(cuts)) // 3, len(cuts) - 1]
            times = []
            for ix in indices:
                _, t0, t1 = cuts[ix]
                times.append(round(float(t0) + (float(t1) - float(t0)) * 0.55, 2))
            return times
    return [
        round(min(0.45, dur * 0.05), 2),
        round(dur * 0.34, 2),
        round(dur * 0.68, 2),
        round(max(0.5, dur - 1.1), 2),
    ]


def build_pack(
    *,
    series: str,
    slug: str,
    clean_title: str,
    out_dir: Path,
    frames: Sequence[Image.Image],
    frame_sources: Sequence[str],
    beats: Sequence[str],
    target_url: str,
    lesson_text: str,
    related_video: str,
    caption_hook: str,
    pinned_comment: str,
    video_path: Path | None = None,
    include_cta_slide: bool = True,
    strict_shorts_runtime: bool = False,
) -> tuple[list[GateResult], dict[str, object]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    theme = SERIES_THEMES[series]
    yt_title = format_youtube_shorts_title(clean_title, series)
    utms = build_channel_utms(target_url, slug)
    parsed_target = urlparse(target_url)
    domain_display = parsed_target.netloc + (parsed_target.path if parsed_target.path not in ("", "/") else "")

    # Copy blocks per channel (strictly isolated UTMs)
    yt_desc = "\n".join([
        caption_hook,
        "",
        f"Prompt Anatomy takeaway: {lesson_text}",
        f"Full breakdown & interactive prompt patterns: {utms['youtube_shorts']}",
        "",
        f"{theme['primary_tag']} {theme['secondary_tag']} #promptanatomy #aihumor",
    ])

    linkedin_copy = "\n".join([
        caption_hook,
        "",
        f"Why this keeps happening in real teams: {lesson_text}",
        "",
        f"Read the full Prompt Anatomy breakdown -> {utms['linkedin']}",
        "",
        f"({pinned_comment})",
        "",
        f"{theme['primary_tag']} #PromptEngineering #AIAgents #SoftwareEngineering",
    ])

    x_copy = "\n".join([
        f"{caption_hook}",
        "",
        f"Lesson: {lesson_text}",
        "",
        f"Reply 1 (clickable breakdown): {utms['x']}",
    ])

    tiktok_copy = "\n".join([
        f"{caption_hook} {theme['primary_tag']} {theme['secondary_tag']} #aihumor #workhumor",
        f"Bio / Breakdown reference: {utms['tiktok']}",
    ])

    channel_sections = {
        "youtube_shorts": yt_desc,
        "linkedin": linkedin_copy,
        "x": x_copy,
        "tiktok": tiktok_copy,
    }

    # Run all Gate S5 checks
    gates: list[GateResult] = []
    if video_path is not None:
        gates.append(check_video_loop_and_endcard(video_path, strict_shorts_runtime=strict_shorts_runtime))
    else:
        gates.append(
            GateResult(
                "S5-1",
                "Loop-Safe Ending Gate",
                True,
                "Stage 5 board mode (pre-film): enforce TAG=0 and zero appended 4-5s outro bumper at master render.",
            )
        )
    gates.append(check_youtube_title(yt_title))
    gates.append(check_channel_copy_isolation(channel_sections, related_video))
    gates.append(check_panels_integrity(frames))

    # Render visual carousel panels + PDF + X 2x2 comic strip
    rendered_slides: list[Image.Image] = []
    panel_paths: list[str] = []
    padded_beats = list(beats) + [""] * max(0, 4 - len(beats))
    for i, src_im in enumerate(frames, start=1):
        slide = render_carousel_panel(src_im, i, 4, series, clean_title, padded_beats[i - 1])
        p_out = out_dir / f"panel_0{i}.png"
        slide.save(p_out, format="PNG", optimize=True)
        rendered_slides.append(slide)
        panel_paths.append(str(p_out))

    if include_cta_slide:
        cta_slide = render_cta_panel(series, clean_title, lesson_text, domain_display, pinned_comment)
        cta_path = out_dir / "panel_05_cta.png"
        cta_slide.save(cta_path, format="PNG", optimize=True)
        rendered_slides.append(cta_slide)
        panel_paths.append(str(cta_path))

    pdf_path = out_dir / "carousel_linkedin.pdf"
    rendered_slides[0].save(
        pdf_path,
        format="PDF",
        resolution=144.0,
        save_all=True,
        append_images=rendered_slides[1:],
    )

    x_grid = render_x_comic_grid(frames, series, clean_title, padded_beats, domain_display)
    x_grid_path = out_dir / "comic_grid_x.png"
    x_grid.save(x_grid_path, format="PNG", optimize=True)

    manifest = {
        "series": series,
        "slug": slug,
        "youtube_shorts_title": yt_title,
        "target_url": target_url,
        "utms": utms,
        "related_video_pill": related_video,
        "pinned_comment": pinned_comment,
        "lesson": lesson_text,
        "frame_sources": list(frame_sources),
        "beats": padded_beats[:4],
        "artifacts": {
            "panels": panel_paths,
            "linkedin_pdf": str(pdf_path),
            "x_comic_grid": str(x_grid_path),
        },
        "gates": [
            {
                "code": g.code,
                "name": g.name,
                "passed": g.passed,
                "detail": g.detail,
                "warnings": g.warnings,
            }
            for g in gates
        ],
    }

    (out_dir / "post_pack.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    md_lines = [
        f"# Stage 5 Omnichannel Pack — {clean_title} (`{slug}`)",
        "",
        "## Gate S5 Verification",
    ]
    for g in gates:
        badge = "PASS" if g.passed else "FAIL"
        md_lines.append(f"- **{badge} [{g.code}] {g.name}:** {g.detail}")
        for w in g.warnings:
            md_lines.append(f"  - *Advisory:* {w}")

    md_lines += [
        "",
        "## Generated Visual Assets",
        f"- **LinkedIn Swipeable Carousel PDF (4:5, {len(rendered_slides)} slides):** `carousel_linkedin.pdf`",
        "- **X / Blog 2x2 4-Panel Comic Page (2160x2700):** `comic_grid_x.png`",
        "- **Individual 1080x1350 Panel PNGs:** " + ", ".join(f"`{Path(p).name}`" for p in panel_paths),
        "",
        "---",
        "",
        "## 1. YouTube Shorts (Tomas Manual Upload)",
        f"**Title ({len(yt_title)} chars):**",
        "```text",
        yt_title,
        "```",
        "",
        "**YouTube Studio -> 'Related video' Pill (MANDATORY for mobile clicks):**",
        f"- Link to: **{related_video}**",
        f"- Long-form video top-of-description clickable link: `{utms['youtube_related']}`",
        "",
        "**Shorts Description:**",
        "```text",
        yt_desc,
        "```",
        "",
        "**Pinned Comment (post immediately after upload for rewatch loop):**",
        "```text",
        pinned_comment,
        "```",
        "",
        "**Loop-Safe Upload Checklist (Empirical Gate G7 Law):**",
        "- [ ] Upload the pure master MP4 directly (`TAG=0`) — **DO NOT** append a 4-5s static outro/brand card (appended bumpers caused -29% to -38% tail drop-off and capped Shorts at ~1,200 views vs 5,654 on seamless loops).",
        "- [ ] Wire the **Related video** pill in YouTube Studio before flipping from `Private` to `Public`.",
        "",
        "---",
        "",
        "## 2. LinkedIn Document Carousel (`carousel_linkedin.pdf`)",
        "**Attachment:** Upload `carousel_linkedin.pdf` as a LinkedIn Document post (title: "
        f"`{clean_title}`).",
        "",
        "**Post Copy:**",
        "```text",
        linkedin_copy,
        "```",
        "",
        "---",
        "",
        "## 3. X (Twitter) 4-Panel Comic Strip (`comic_grid_x.png`)",
        "**Attachment:** Attach `comic_grid_x.png` (single 2x2 comic page) or `panel_01.png`..`panel_04.png`.",
        "",
        "**Main Post + Reply 1:**",
        "```text",
        x_copy,
        "```",
        "",
        "---",
        "",
        "## 4. TikTok / Reels",
        "```text",
        tiktok_copy,
        "```",
        "",
    ]
    (out_dir / "POST_PACK.md").write_text("\n".join(md_lines), encoding="utf-8")
    return gates, manifest


# ---------------------------------------------------------------------------
# Self-Test Suite (Validates on Real Known Passes AND Known Historical Failures)
# ---------------------------------------------------------------------------

def run_selftest() -> int:
    """Series rule: no check counts until it catches a known failure and passes a real clean case."""
    checks: list[tuple[str, bool, str]] = []

    def record(label: str, ok: bool, detail: str) -> None:
        checks.append((label, ok, detail))
        print(f"{'PASS' if ok else 'FAIL'}  {label}: {detail}")

    # 1. Known Title Pass: Make It Original! (#1 hit, 5,654 views)
    t_good = check_youtube_title("Make It Original! #hoodyz #cartoon")
    record("title pass (Make It Original!)", t_good.passed, t_good.detail)

    # 2. Known Title Failure #1: Live private video 9uUv2nc2834 ('MY BOS IS AI?' + 7 tags)
    t_bos = check_youtube_title(
        "MY BOS IS AI? #hoodyz #promptanatomy #animation #aitraining #aivideo #viralshorts #cartoon"
    )
    record(
        "title catches 'BOS' typo + 7 tags + ALL-CAPS (9uUv2nc2834)",
        (not t_bos.passed) and ("BOS" in t_bos.detail) and ("7 hashtags" in t_bos.detail),
        t_bos.detail,
    )

    # 3. Known Title Failure #2: Live video O7rtkF0zP00 ('Make IT Better. HoodyZ E06' + 6 tags, 49 views)
    t_e06 = check_youtube_title(
        "Make IT Better. HoodyZ E06 #hoodyz #promptanatomy #animation #aitraining #aivideo #viralshorts"
    )
    record(
        "title catches 'E06' episode token + 6 tags (O7rtkF0zP00)",
        (not t_e06.passed) and ("episode/part" in t_e06.detail) and ("6 hashtags" in t_e06.detail),
        t_e06.detail,
    )

    # 4. Known UTM Leak Failures: utm_source=tiktok / utm_source=blog inside YouTube description
    utms = build_channel_utms("https://promptanatomy.app/patterns/scope-lock", "just_one_line")
    leaked_sections = {
        "youtube_shorts": "Watch more: https://promptanatomy.app/?utm_source=tiktok&utm_campaign=make_it_better",
        "linkedin": f"Read: {utms['linkedin']}",
        "x": f"Read: {utms['x']}",
        "tiktok": f"Read: {utms['tiktok']}",
    }
    u_bad = check_channel_copy_isolation(leaked_sections, "Prompt Anatomy Ep 12")
    record(
        "UTM gate catches tiktok leak inside YouTube copy (LT93eJ8lfnA / O7rtkF0zP00)",
        (not u_bad.passed) and ("leaked wrong utm_source=tiktok" in u_bad.detail),
        u_bad.detail,
    )

    clean_sections = {
        "youtube_shorts": f"Read: {utms['youtube_shorts']}",
        "linkedin": f"Read: {utms['linkedin']}",
        "x": f"Read: {utms['x']}",
        "tiktok": f"Read: {utms['tiktok']}",
    }
    u_no_rel = check_channel_copy_isolation(clean_sections, "")
    record(
        "UTM gate catches missing Related Video pill target",
        (not u_no_rel.passed) and ("Related Video" in u_no_rel.detail),
        u_no_rel.detail,
    )
    u_good = check_channel_copy_isolation(clean_sections, "Prompt Anatomy Long-Form Breakdown")
    record("UTM gate passes clean 4-channel isolation + Related Video", u_good.passed, u_good.detail)

    # 5. Synthetic & Real Video Loop-Safe Ending Gate Validation
    f_scene_a = Image.new("RGB", (180, 320), (245, 242, 235))
    ImageDraw.Draw(f_scene_a).rectangle((30, 80, 150, 240), fill=(31, 42, 68))
    f_scene_b = Image.new("RGB", (180, 320), (245, 242, 235))
    ImageDraw.Draw(f_scene_b).rectangle((45, 95, 165, 255), fill=(43, 182, 115))
    f_bumper = Image.new("RGB", (180, 320), (12, 14, 20))
    ImageDraw.Draw(f_bumper).rectangle((20, 130, 160, 190), fill=(255, 255, 255))

    g_bumper = analyze_frames_loop_safety(
        f_scene_a, f_scene_b, [f_bumper, f_bumper, f_bumper, f_bumper, f_bumper], 29.8
    )
    record(
        "Loop gate catches appended 4-5s static outro bumper",
        not g_bumper.passed and "Static outro bumper" in g_bumper.detail,
        g_bumper.detail,
    )

    # Real video checks if renders are present on disk
    mio = REPO_ROOT / "hoodyz/make-it-original/v53/make_it_original_v53.mp4"
    rtb = REPO_ROOT / "hoodyz/remove-the-bottleneck/final/remove_the_bottleneck.mp4"
    pt_cliff = REPO_ROOT / "uptimez/prompt-telephone/uptimez_PT_v04_3.mp4"
    mf_40s = REPO_ROOT / "uptimez/mandatory-fun/uptimez_mf_anim_v2.mp4"

    if mio.exists():
        g_mio = check_video_loop_and_endcard(mio)
        record("Real video PASS: Make It Original v5.3 (5,654 views, 84.6% end-hold)", g_mio.passed, g_mio.detail)
    if rtb.exists():
        g_rtb = check_video_loop_and_endcard(rtb)
        record("Real video PASS: Remove the Bottleneck exact loop", g_rtb.passed, g_rtb.detail)
    if pt_cliff.exists():
        g_pt = check_video_loop_and_endcard(pt_cliff)
        record(
            "Real video FAIL caught: Prompt Telephone v04.3 closing post-card cliff (-28.9% tail drop)",
            not g_pt.passed and "Closing-card tail cliff" in g_pt.detail,
            g_pt.detail,
        )
    if mf_40s.exists():
        g_mf = check_video_loop_and_endcard(mf_40s, strict_shorts_runtime=False)
        record(
            "Real 40s video emits >35s Shorts runtime teaser advisory (Mandatory Fun)",
            bool(g_mf.warnings) and ">35s" in g_mf.warnings[0],
            g_mf.warnings[0] if g_mf.warnings else g_mf.detail,
        )

    shot_candidates = [Path("cs_board_12.1.png"), Path("cs_board_2.1.png"), Path("cs_board_22.1.png")]
    picked_21 = match_shot_pngs(shot_candidates, "2.1")
    record(
        "Shot-ID boundary match selects 2.1 without colliding on 12.1 or 22.1",
        [p.name for p in picked_21] == ["cs_board_2.1.png"],
        f"matched={[p.name for p in picked_21]}",
    )

    failed = [name for name, ok, _ in checks if not ok]
    print(f"\nSELFTEST SUMMARY: {len(checks) - len(failed)}/{len(checks)} passed")
    return 1 if failed else 0


def match_shot_pngs(candidates: Sequence[Path], sid: str) -> list[Path]:
    pat = re.compile(rf"(?:^|[_.-]){re.escape(sid)}\.png$", re.IGNORECASE)
    return sorted([p for p in candidates if pat.search(p.name)])


# ---------------------------------------------------------------------------
# CLI Entrypoint
# ---------------------------------------------------------------------------

def load_frames_from_args(args: argparse.Namespace) -> tuple[list[Image.Image], list[str]]:
    if args.frames:
        if len(args.frames) != 4:
            raise SystemExit(f"--frames requires exactly 4 PNG paths, got {len(args.frames)}")
        paths = [Path(p) for p in args.frames]
        return [Image.open(p).convert("RGB") for p in paths], [str(p) for p in paths]

    if args.board_dir:
        bdir = Path(args.board_dir)
        if args.shots:
            if len(args.shots) != 4:
                raise SystemExit("--shots requires exactly 4 shot IDs")
            all_pngs = sorted(bdir.glob("*.png"))
            paths = []
            for sid in args.shots:
                matches = match_shot_pngs(all_pngs, sid)
                if not matches:
                    raise SystemExit(f"No board PNG matching shot ID '{sid}' in {bdir}")
                paths.append(matches[0])
        else:
            all_pngs = sorted(bdir.glob("*.png"))
            if len(all_pngs) < 4:
                raise SystemExit(f"Need at least 4 PNGs in {bdir}, found {len(all_pngs)}")
            n = len(all_pngs)
            paths = [all_pngs[0], all_pngs[n // 3], all_pngs[(2 * n) // 3], all_pngs[-1]]
        return [Image.open(p).convert("RGB") for p in paths], [str(p) for p in paths]

    if args.video:
        vpath = Path(args.video)
        if args.times:
            times = [float(x.strip()) for x in args.times.split(",") if x.strip()]
            if len(times) != 4:
                raise SystemExit(f"--times requires 4 comma-separated seconds, got {args.times}")
        else:
            times = pick_default_times(vpath)
        imgs = [extract_video_frame(vpath, t) for t in times]
        srcs = [f"{vpath.name}@{t:.2f}s" for t in times]
        return imgs, srcs

    raise SystemExit("Provide one of: --frames (4 PNGs), --board-dir, or --video")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Tier A1 Stage 5 carousel & clean UTM post-pack exporter.")
    ap.add_argument("--selftest", action="store_true", help="Run Gate S5 self-tests against known pass/fail cases.")
    ap.add_argument("--series", choices=sorted(SERIES_THEMES.keys()), default="hoodyz")
    ap.add_argument("--slug", help="UTM campaign slug, e.g. just_one_line or customer_success")
    ap.add_argument("--title", help="Clean standalone episode hook title (without episode numbers)")
    ap.add_argument("--frames", nargs=4, help="Explicit paths to 4 vertical 9:16 PNG frames")
    ap.add_argument("--board-dir", help="Path to Stage 5 board PNG directory")
    ap.add_argument("--shots", nargs=4, help="4 shot IDs to pick from --board-dir, e.g. 1.1 2.2 3.2 5.4b")
    ap.add_argument("--video", help="Path to rendered 9:16 MP4 master/preview")
    ap.add_argument("--times", help="4 comma-separated timestamps in seconds for --video, e.g. 0.2,6.8,11.2,15.6")
    ap.add_argument("--beats", nargs=4, default=["", "", "", ""], help="Optional 4 short beat captions under panels")
    ap.add_argument("--post-md", help="Optional existing POST.md to inherit caption & pinned comment")
    ap.add_argument("--caption", help="Override main social hook caption")
    ap.add_argument("--pinned-comment", help="Override pinned loop-bait question")
    ap.add_argument("--lesson", default="Specify hard boundaries in the prompt, or the agent optimizes the wrong metric.")
    ap.add_argument(
        "--target-url",
        default="https://promptanatomy.app",
        help="Destination URL on promptanatomy.app or promptanatomy.blog",
    )
    ap.add_argument(
        "--related-video",
        default="Prompt Anatomy Long-Form Breakdown (link in YouTube Studio -> Related Video)",
        help="Target long-form/companion YouTube video for the Shorts 'Related video' pill",
    )
    ap.add_argument("--no-cta-slide", action="store_true", help="Omit Slide 5 takeaway card from LinkedIn PDF")
    ap.add_argument("--strict-shorts-runtime", action="store_true", help="Fail S5-1 if Shorts runtime exceeds 35s")
    ap.add_argument(
        "--out",
        help="Output folder for the generated Stage 5 pack (defaults to gitignored build/stage5_pack/<slug>)",
    )

    args = ap.parse_args(argv)
    if args.selftest:
        return run_selftest()

    if not args.slug or not args.title:
        ap.error("--slug and --title are required unless running --selftest")
    out_path = Path(args.out) if args.out else (REPO_ROOT / "build" / "stage5_pack" / args.slug)

    post_meta = parse_existing_post_md(Path(args.post_md) if args.post_md else None)
    caption = args.caption or post_meta.get("caption") or args.title
    pinned = args.pinned_comment or post_meta.get("pinned_comment") or "Did you spot what changed between Frame 1 and the ending?"

    frames, sources = load_frames_from_args(args)
    gates, manifest = build_pack(
        series=args.series,
        slug=args.slug,
        clean_title=args.title,
        out_dir=out_path,
        frames=frames,
        frame_sources=sources,
        beats=args.beats,
        target_url=args.target_url,
        lesson_text=args.lesson,
        related_video=args.related_video,
        caption_hook=caption,
        pinned_comment=pinned,
        video_path=Path(args.video) if args.video else None,
        include_cta_slide=not args.no_cta_slide,
        strict_shorts_runtime=args.strict_shorts_runtime,
    )

    failed = [g for g in gates if not g.passed]
    for g in gates:
        print(f"{'PASS' if g.passed else 'FAIL'}  [{g.code}] {g.name}: {g.detail}")
        for w in g.warnings:
            print(f"WARN  [{g.code}] {w}")
    print(f"Wrote Stage 5 pack -> {out_path} ({len(manifest['artifacts']['panels'])} slides, PDF, X grid, POST_PACK.md)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
