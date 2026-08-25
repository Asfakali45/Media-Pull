# MediaPull

A Streamlit-based YouTube video and audio downloader built with Python and `yt-dlp`.

## Live Demo

[Launch MediaPull](https://media-pull.streamlit.app/)

## Features

* Download YouTube videos
* Download audio-only files as MP3
* Select video quality:

  * Best Quality
  * 1080p
  * 720p
  * 480p
  * 360p
* Select audio quality:

  * Best Quality
  * 192 kbps
  * 128 kbps
* Download progress tracking
* Simple Streamlit interface
* MP4 video output
* MP3 audio output

## Tech Stack

* **Python**
* **Streamlit** — web application interface
* **yt-dlp** — media extraction and downloading
* **FFmpeg** — required for media merging and audio conversion

## Project Structure

```text
Media-Pull/
├── app.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Asfakali45/Media-Pull.git
cd Media-Pull
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> FFmpeg is also required for video merging and MP3 conversion.

### 4. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## How to Use

1. Open MediaPull.
2. Paste a YouTube video URL.
3. Choose **Video** or **Audio Only**.
4. Select the desired quality.
5. Click **Download**.
6. Save the generated file.

## Screenshots

Add screenshots of the application here:

```text
![MediaPull Screenshot](screenshots/home.png)
```

## Important Note

MediaPull is intended for personal, non-commercial use. Users are responsible for ensuring that their downloads comply with YouTube's Terms of Service, copyright law, and the rights of content owners.

## Future Improvements

* Playlist downloading
* More output format options
* Improved error handling
* Download history
* Additional media-source support

## Author

**Asfakali45**

* GitHub: [github.com/Asfakali45](https://github.com/Asfakali45)
* Repository: [Media-Pull](https://github.com/Asfakali45/Media-Pull)
* Live Demo: [MediaPull](https://media-pull.streamlit.app/)
