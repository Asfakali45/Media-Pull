import os
import tempfile
import streamlit as st
import yt_dlp

st.set_page_config(page_title="YT Downloader", page_icon="▼", layout="centered")

# ---------- Styling ----------
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #ff4b4b, #ff8a4b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        padding-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #9a9a9a;
        margin-top: -10px;
        margin-bottom: 30px;
        font-size: 15px;
    }
    div.stButton > button, div.stDownloadButton > button {
        width: 100%;
        background: linear-gradient(45deg, #ff4b4b, #ff8a4b);
        color: white;
        font-weight: 700;
        font-size: 1.15em;
        border: none;
        border-radius: 12px;
        padding: 1.1em 0;
        margin-top: 6px;
        transition: 0.2s ease;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 18px rgba(255, 75, 75, 0.4);
    }
    .stTextInput input {
        border-radius: 8px;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
        padding: 6px 6px 0 6px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>&#8595; YouTube Downloader</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Paste a link, pick your format, download in one click</div>", unsafe_allow_html=True)

# ---------- Inputs ----------
with st.container(border=True):
    url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

    col1, col2 = st.columns(2)
    with col1:
        mode = st.radio("Type", ["Video", "Audio Only"], horizontal=True)
    with col2:
        if mode == "Video":
            quality_label = st.selectbox(
                "Quality",
                ["Best Quality", "1080p", "720p", "480p", "360p"]
            )
        else:
            quality_label = st.selectbox(
                "Audio Quality",
                ["Best Quality", "192 kbps", "128 kbps"]
            )

    start = st.button("Download  ↓", use_container_width=True)

VIDEO_QUALITY_MAP = {
    "Best Quality": "bestvideo+bestaudio/best",
    "1080p": "bestvideo[height<=1080]+bestaudio/best",
    "720p": "bestvideo[height<=720]+bestaudio/best",
    "480p": "bestvideo[height<=480]+bestaudio/best",
    "360p": "bestvideo[height<=360]+bestaudio/best",
}

AUDIO_QUALITY_MAP = {
    "Best Quality": "0",
    "192 kbps": "192",
    "128 kbps": "128",
}

# ---------- Download logic ----------
def run_download(url: str, mode: str, quality_label: str, out_dir: str,
                  progress_bar, status_text):

    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            if total:
                pct = min(downloaded / total, 1.0)
                progress_bar.progress(pct)
                status_text.text(
                    f"Downloading... {pct * 100:.1f}%  "
                    f"({d.get('_speed_str', '').strip() or 'calculating speed'})"
                )
            else:
                status_text.text("Downloading...")
        elif d["status"] == "finished":
            progress_bar.progress(1.0)
            status_text.text("Processing / merging file, please wait...")

    outtmpl = os.path.join(out_dir, "%(title)s.%(ext)s")

    if mode == "Video":
        options = {
            "format": VIDEO_QUALITY_MAP.get(quality_label, "bestvideo+bestaudio/best"),
            "outtmpl": outtmpl,
            "merge_output_format": "mp4",
            "progress_hooks": [hook],
            "quiet": True,
            "noprogress": True,
        }
    else:
        options = {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": AUDIO_QUALITY_MAP.get(quality_label, "0"),
            }],
            "progress_hooks": [hook],
            "quiet": True,
            "noprogress": True,
        }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if mode == "Audio Only":
            base, _ = os.path.splitext(filename)
            filename = base + ".mp3"
        elif not filename.endswith(".mp4"):
            base, _ = os.path.splitext(filename)
            candidate = base + ".mp4"
            if os.path.exists(candidate):
                filename = candidate

    return filename, info.get("title", "download")


if start:
    if not url.strip():
        st.error("Pehle ek valid YouTube URL daaliye.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                status_text.text("Fetching video info...")
                filepath, title = run_download(
                    url.strip(), mode, quality_label, tmp_dir, progress_bar, status_text
                )

                if os.path.exists(filepath):
                    status_text.text("Done!")
                    with open(filepath, "rb") as f:
                        file_bytes = f.read()

                    ext = os.path.splitext(filepath)[1].lstrip(".")
                    mime = "audio/mpeg" if mode == "Audio Only" else "video/mp4"

                    st.success(f"'{title}' ready to download.")
                    st.download_button(
                        label=f"Save {ext.upper()} File  ↓",
                        data=file_bytes,
                        file_name=os.path.basename(filepath),
                        mime=mime,
                        use_container_width=True,
                    )
                else:
                    st.error("File create nahi hua. URL ya format check karke dobara try karein.")
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown(
    "<div style='text-align:center; color:#666; margin-top:30px; font-size:12px;'>"
    "Built with yt-dlp + Streamlit — for personal, non-commercial use only."
    "</div>",
    unsafe_allow_html=True,
)