import subprocess
import os

# 🔹 Input: YouTube video URL
url = input("Enter YouTube 360° video URL: ").strip()

# 🔹 Filenames
downloaded = "video_raw.mp4"
with_metadata = "video_360.mp4"
final = "video_final.mp4"
spatialmedia_path = "spatialmedia/spatialmedia.py"  # Update this path if needed

# 🔸 1. Download
print("📥 Downloading video from YouTube...")
subprocess.run(["yt-dlp", "-f", "best", "-o", downloaded, url])

# 🔸 2. Inject Metadata
print("🛠 Injecting 360° metadata...")
subprocess.run(["python", spatialmedia_path, "-i", downloaded, with_metadata])

# 🔸 3. Compress / Scale
print("📦 Compressing and resizing to 2:1 equirectangular...")
subprocess.run([
    "ffmpeg", "-i", with_metadata,
    "-vf", "scale=3840:1920",
    "-c:v", "libx264", "-crf", "23", "-preset", "slow",
    final
])

print(f"\n✅ Done! Your equirectangular video is ready: {final}")
