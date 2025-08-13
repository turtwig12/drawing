import yt_dlp
import re



def download_youtube_video(link):

    pattern = r"^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+(&\S*)?$"
    while re.match(pattern, link) is None:
        link = input("Enter a valid link to the video: ")

    # downloads video
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',  # Output file name template
        'quiet': True,  # Show progress bar (optional)
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)
        video_title = info_dict.get('title', 'video')
        ext = info_dict.get('ext', 'mp4')
        filename = f"{video_title}.{ext}"
        print(f"\nDownloaded file: {filename}")
        return filename
