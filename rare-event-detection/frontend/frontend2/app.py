
import json
import os
from pathlib import Path
from PIL import Image

import streamlit as st

st.set_page_config(page_title="VLM-Inspector", page_icon="👁️", layout="wide")

st.markdown("""
<style>
/* Home tiles */
.tile {
  border: 1px solid rgba(255,255,255,0.10);
  background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  border-radius: 18px;
  padding: 14px 12px;
  text-align: center;
  box-shadow: 0 10px 28px rgba(0,0,0,0.45), inset 0 0 0 1px rgba(255,255,255,0.03);
  transition: transform .15s ease, box-shadow .2s ease, border-color .2s ease;
}
.tile:hover {
  transform: translateY(-2px);
  box-shadow: 0 16px 36px rgba(0,0,0,0.55);
  border-color: rgba(255,255,255,0.18);
}

/* Colored glow disc behind the logo */
.tile .badge {
  width: 140px; height: 140px; margin: 4px auto 10px auto; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  /* background set inline per-tile to use that domain's accent color */
}

/* Make white logos readable on dark by adding a gentle glow */
.tile img {
  max-height: 110px; object-fit: contain;
  filter: drop-shadow(0 2px 6px rgba(0,0,0,.65)) drop-shadow(0 0 12px rgba(255,255,255,.22));
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.hero {
  border: 1px solid rgba(255,255,255,0.10);
  background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  border-radius: 22px;
  padding: 18px 16px;
  text-align: center;
  box-shadow: 0 14px 36px rgba(0,0,0,0.45), inset 0 0 0 1px rgba(255,255,255,0.03);
}
.hero .hero-badge {
  width: 260px; height: 260px; margin: 4px auto 10px auto; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  /* background is set inline with your accent color */
}
.hero img {
  max-height: 180px; object-fit: contain;
  filter: drop-shadow(0 2px 8px rgba(0,0,0,.65)) drop-shadow(0 0 16px rgba(255,255,255,.22));
}
</style>
""", unsafe_allow_html=True)


# Tweak these until it feels right on your screen
HERO_TOP_VH = 8      # how far to push the big logo *down*
NAV_GAP_VH  = 18     # vertical gap between hero and the bottom logos
# ---------- Config ----------
CONFIG_PATH = Path(__file__).parent / "demo_config.json"
with open(CONFIG_PATH, "r") as f:
    CFG = json.load(f)

APP_NAME = CFG["branding"]["name"]
LOGO_PATH = CFG["branding"].get("logo")

ACCENTS = CFG["branding"].get("accent_colors", {})

def accent(domain):
    return ACCENTS.get(domain, "#0ea5e9")  # default teal

APP_DIR = Path(__file__).parent

HERO_LOGO = CFG["branding"].get("hero_logo", LOGO_PATH)
APP_ICONS = CFG["branding"].get("app_icons", {})       # {"tropical_med": "...", ...}
PLUS_ICON = CFG["branding"].get("plus_icon", None)

HERO_ACCENT = CFG["branding"].get("hero_accent", "#3b82f6")  # fallback blue

# Router state
st.session_state.setdefault("view", "home")            # "home" or "app"
st.session_state.setdefault("selected_domain", None)

def go_home():
    st.session_state.update(view="home", selected_domain=None)

def open_domain(dk: str):
    st.session_state.update(view="app", selected_domain=dk)

def resolve_path(p):
    p = Path(p)
    return p if p.is_absolute() else (APP_DIR / p)

from pathlib import Path

def is_url(s: str) -> bool:
    s = s.strip() if isinstance(s, str) else s
    return isinstance(s, str) and s.lower().startswith(("http://", "https://", "data:"))

def safe_image(src, **kwargs) -> bool:
    """Render an image safely. Returns True if shown, False otherwise."""
    if not src:
        return False
    src = resolve_path(src)
    try:
        if isinstance(src, Path):
            if not src.exists():
                return False
            st.image(str(src), **kwargs)
        else:
            st.image(src, **kwargs)   # URL or data: URI
        return True
    except Exception:
        return False



# ---------- Helpers ----------
def load_img(path, use_rgba=False):
    p = Path(path)
    if not p.exists():
        return None
    im = Image.open(p)
    return im.convert("RGBA") if use_rgba else im.convert("RGB")

def hex_to_rgba(hex_color: str, alpha: float = 0.28) -> str:
    if not hex_color:
        return "rgba(59,130,246,0.28)"  # fallback to blue-ish
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

def overlay_heatmap(base_img_path, heatmap_path, alpha=0.40):
    base = load_img(base_img_path, use_rgba=True)
    heat = load_img(heatmap_path, use_rgba=True)
    if base is None or heat is None:
        return base  # show whatever we have
    heat = heat.resize(base.size)
    out = Image.alpha_composite(base, Image.blend(Image.new("RGBA", base.size, (0,0,0,0)), heat, 1.0))
    # Control final opacity via alpha of composite against base
    out = Image.blend(base, out, alpha)
    return out.convert("RGB")

def section_header(text, color="#0f172a"):
    st.markdown(f"<h3 style='margin-top:0.5rem;margin-bottom:0.5rem;color:{color}'>{text}</h3>", unsafe_allow_html=True)


def render_home():
    # push the hero logo slightly DOWN from the very top
    st.markdown(f"<div style='height:{HERO_TOP_VH}vh'></div>", unsafe_allow_html=True)

    # Hero (top, centered)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        accent_rgba = hex_to_rgba(HERO_ACCENT, 0.32)
        # hero card + colored halo behind the main logo
        st.markdown(
            f'<div class="hero"><div class="hero-badge" '
            f'style="background: radial-gradient(closest-side, {accent_rgba}, rgba(0,0,0,0) 70%);">',
            unsafe_allow_html=True
        )
        if not safe_image(HERO_LOGO, use_container_width=True):
            st.markdown(f"<h1 style='text-align:center;margin:1rem 0'>{APP_NAME}</h1>", unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)  # close .hero-badge + .hero

        # (optional) brand subtitle if you have it in JSON as branding.subtitle
        subtitle = CFG["branding"].get("subtitle", "Demo-only UI • Few-shot • Generation • Classification + heatmap")
        st.caption(subtitle)

    st.markdown(f"<div style='height:{NAV_GAP_VH}vh'></div>", unsafe_allow_html=True)
    # ...bottom tiles remain as you have them...

    # Bottom nav: 3 clickable logos + a fake '+' tile
    keys   = list(CFG["domains"].keys())
    titles = [CFG["domains"][k]["title"] for k in keys]
    icons  = [APP_ICONS.get(k) for k in keys]

    colA, colB, colC, colD = st.columns(4)

    for col, k, t, icon in zip([colA, colB, colC], keys[:3], titles[:3], icons[:3]):
        with col:
            accent_rgba = hex_to_rgba(accent(k), 0.32)
            st.markdown(f'<div class="tile"><div class="badge" style="background: radial-gradient(closest-side, {accent_rgba}, rgba(0,0,0,0) 68%);">', unsafe_allow_html=True)
            shown = safe_image(icon, use_container_width=True)
            if not shown:
                st.markdown(f"### {t}")
            st.markdown('</div>', unsafe_allow_html=True)  # close .badge
            st.button(t, key=f"open_{k}", use_container_width=True, on_click=lambda kk=k: open_domain(kk))
            st.markdown('</div>', unsafe_allow_html=True)  # close .tile

    with colD:
        # Neutral halo for the fake '+' tile
        st.markdown('<div class="tile"><div class="badge" style="background: radial-gradient(closest-side, rgba(148,163,184,.28), rgba(0,0,0,0) 68%);">', unsafe_allow_html=True)
        if not safe_image(PLUS_ICON, use_container_width=True):
            st.markdown('<div style="font-size:64px;line-height:1.1;text-align:center;">+</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)  # close .badge
        st.button("+ New (coming soon)", disabled=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)  # close .tile



# ---- Overlay helpers & styles ----
# Session state defaults
for _k, _v in [("overlay_open", False), ("overlay_title", ""), ("overlay_text", "")]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

def show_overlay(text: str, title: str = "Description"):
    st.session_state["overlay_text"] = text or ""
    st.session_state["overlay_title"] = title or "Description"
    st.session_state["overlay_open"] = True

def render_overlay():
    if st.session_state.get("overlay_open"):
        title = st.session_state.get("overlay_title", "Description")
        text = st.session_state.get("overlay_text", "")

        st.markdown(
            """
<style>
.overlay-bg {{ position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 1000; }}
.overlay-card {{
  position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
  background: #fff; border-radius: 14px; padding: 1.25rem 1.5rem; width: min(90vw, 780px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.35); z-index: 1001; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
}}
.overlay-title {{ font-weight: 700; font-size: 1.1rem; margin-bottom: .35rem; color: #0f172a; }}
.overlay-text {{ font-size: 0.98rem; line-height: 1.55; color: #111827; white-space: pre-wrap; }}
</style>
<div class="overlay-bg"></div>
<div class="overlay-card">
  <div class="overlay-title">{title}</div>
  <div class="overlay-text">{text}</div>
</div>
            """.format(title=title, text=text),
            unsafe_allow_html=True,
        )

        if st.button("Close", key="overlay_close"):
            st.session_state["overlay_open"] = False

# ==== Description dialog (works on modern Streamlit) ====

# state defaults (keep yours if already present)
for k, v in [("desc_open", False), ("desc_title", ""), ("desc_text", "")]:
    st.session_state.setdefault(k, v)

def open_desc(title: str, text: str):
    st.session_state["desc_title"] = title or "Description"
    st.session_state["desc_text"]  = text or ""
    st.session_state["desc_open"]  = True

# 1) Define the dialog body once
def _desc_body():
    # show dynamic title inside the dialog body
    st.markdown(f"**{st.session_state.get('desc_title', 'Description')}**")
    st.markdown(st.session_state.get("desc_text", ""))
    if st.button("Close", use_container_width=True):
        st.session_state["desc_open"] = False
        st.rerun()

# 2) Attach the right decorator at runtime (supports older versions too)
if hasattr(st, "dialog"):  # Streamlit >= ~1.37
    desc_dialog = st.dialog(
        "Description",
        on_dismiss=lambda: st.session_state.update(desc_open=False)  # X / outside / ESC
    )(_desc_body)
elif hasattr(st, "experimental_dialog"):  # Streamlit 1.34–1.48
    desc_dialog = st.experimental_dialog("Description")(_desc_body)
else:
    desc_dialog = None  # very old Streamlit; no dialog support

def render_desc():
    if not st.session_state.get("desc_open"):
        return
    if desc_dialog:
        desc_dialog()
    else:
        # last-resort fallback if dialogs aren't available
        with st.expander(st.session_state.get("desc_title","Description"), expanded=True):
            st.markdown(st.session_state.get("desc_text",""))
            if st.button("Close"):
                st.session_state["desc_open"] = False

def render_app(domain_key: str):
    # Back button (top-left)
    st.button("← Back to home", on_click=go_home)

    D = CFG["domains"][domain_key]

    # Maintain per-domain 'trained' state
    if "trained" not in st.session_state:
        st.session_state["trained"] = {k: False for k in CFG["domains"]}
    trained = st.session_state["trained"].get(domain_key, False)

    accent_color = accent(domain_key)

    st.divider()
    left, mid, right = st.columns([1, 1, 1])

    # --------- Train ---------
    with left:
        section_header("Few-shot", color=accent_color)

        fs = D.get("fewshot", [])
        caps_cfg = D.get("fewshot_captions", [])

        if fs:
            st.markdown("**Few-shot examples**")
            captions = caps_cfg if isinstance(caps_cfg, list) and len(caps_cfg) == len(fs) \
                    else [f"Example {i+1}" for i in range(len(fs))]

            cols = st.columns(len(fs))
            for i, (col, img_path) in enumerate(zip(cols, fs)):
                with col:
                    st.image(str(resolve_path(img_path)), use_container_width=True)
                    cap = captions[i] if i < len(captions) else f"Example {i+1}"
                    if st.button("Description", key=f"desc_fs_{domain_key}_{i}", use_container_width=True):
                        open_desc("Few-shot description", cap)

        clicked = st.button("Train Model (few-shot)", type="primary", use_container_width=True)
        if clicked:
            with st.status("Training few-shot model…", expanded=False) as status:
                import time; time.sleep(0.6)  # demo pause
                st.session_state["trained"][domain_key] = True
                status.update(label="Model successfully trained ✔", state="complete")
            trained = True
            st.toast("Model successfully trained ✔", icon="✅")
        if trained:
            st.success("Status: trained", icon="🧠")
        else:
            st.info("Status: not trained")

    # --------- Generate ---------
    with mid:
        section_header("Generate new samples", color=accent_color)

        gen_cfg = D.get("generated", {})
        if st.button("Generate Image(s)", use_container_width=True, disabled=not trained):
            st.session_state[f"show_gen_{domain_key}"] = True

        if st.session_state.get(f"show_gen_{domain_key}"):
            gen_items = gen_cfg if isinstance(gen_cfg, list) else [gen_cfg]
            gen_items = [g for g in gen_items if isinstance(g, dict) and (g.get("image") or g.get("caption"))]

            if not gen_items:
                st.info("No generated samples configured.")
            elif len(gen_items) == 1:
                item = gen_items[0]
                if item.get("image"):
                    st.image(str(resolve_path(item["image"])), use_container_width=True)
                if st.button("Description", key=f"desc_gen_{domain_key}_0", use_container_width=True):
                    open_desc("Generated sample description", item.get("caption", "No description provided."))
            else:
                cols = st.columns(len(gen_items))
                for i, (col, item) in enumerate(zip(cols, gen_items)):
                    with col:
                        if item.get("image"):
                            st.image(str(resolve_path(item["image"])), use_container_width=True)
                        if st.button("Description", key=f"desc_gen_{domain_key}_{i}", use_container_width=True):
                            open_desc("Generated sample description", item.get("caption", "No description provided."))

    # --------- Classify ---------
    with right:
        section_header("Classify a new image", color=accent_color)

        is_crop = (domain_key == "crop_health")

        if is_crop:
            uploads = st.file_uploader(
                "Upload images ",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
                key=f"up_{domain_key}",
            ) or []
            uploads = uploads[:2]
            if uploads:
                st.caption(f"{len(uploads)} image(s) selected.")
                cols = st.columns(len(uploads))
                for col, f in zip(cols, uploads):
                    with col:
                        st.image(f, caption=getattr(f, "name", "uploaded"), use_container_width=True)
        else:
            _ = st.file_uploader(
                "Upload image",
                type=["jpg", "jpeg", "png"],
                key=f"up_{domain_key}",
            )
            uploads = []  # keep var defined

        if st.button("Classify", use_container_width=True, disabled=not trained):
            st.session_state[f"show_cls_{domain_key}"] = True

        if st.session_state.get(f"show_cls_{domain_key}"):
            cls_cfg = D.get("classification", {})
            cls_items = cls_cfg if isinstance(cls_cfg, list) else [cls_cfg]
            cls_items = [c for c in cls_items if isinstance(c, dict)]

            if not cls_items:
                st.info("No classification samples configured.")
            else:
                uploaded_names = [getattr(f, "name", f"image {i+1}") for i, f in enumerate(uploads, start=1)] if is_crop else []

                for idx, item in enumerate(cls_items, start=1):
                    extra = f" — Uploaded: {uploaded_names[idx-1]}" if is_crop and idx-1 < len(uploaded_names) else ""
                    st.markdown(f"**Result {idx}{extra}**")

                    test = item.get("test_image")
                    heat = item.get("heatmap")
                    alpha = float(item.get("heatmap_alpha", 0.45))

                    # show heatmap overlay if provided (works for all domains)
                    if heat and test:
                        result = overlay_heatmap(resolve_path(test), resolve_path(heat), alpha=alpha)
                        if result is not None:
                            st.image(result, caption="Heatmap overlay", use_container_width=True)
                        else:
                            st.image(str(resolve_path(test)), caption="", use_container_width=True)
                    elif test:
                        st.image(str(resolve_path(test)), caption="", use_container_width=True)

                    pred = item.get("predicted_class", "—")
                    why  = item.get("why", "")

                    if domain_key == "manufacturing":
                        observation = item.get("observation")
                        if observation:
                            st.markdown(f"**Observation**: {observation}")
                        st.markdown(f"**Presence of fatigue cracks**: {pred}")
                        if why:
                            st.markdown(f"**Where**: {why}")
                    else:
                        st.markdown(f"**Status**: {pred}")
                        if why:
                            st.markdown(f"**Reason**: {why}")

                    if idx < len(cls_items):
                        st.markdown("---")

    # Dialog + notes
    render_desc()
    st.divider()
    with st.expander("Demo notes & tips"):
        st.markdown(
            """
- This is a **demo-only** interface. All outputs are preloaded from `/assets` via `demo_config.json`.
- Replace images and texts in the `assets/<domain>/` folders and edit `demo_config.json` to update the demo.
- The **Upload image** control is for realism; the classification output is still the canned result.
- Use **Streamlit Community Cloud** to deploy quickly: push to GitHub, then “New app” → select repo.
            """
        )

# ROUTER
if st.session_state["view"] == "home":
    render_home()
else:
    dk = st.session_state.get("selected_domain") or list(CFG["domains"].keys())[0]
    render_app(dk)
