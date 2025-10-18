import yt_dlp

url = "https://youtu.be/gR6GVH7dyAk?si=maxDaXeUL7TuGiT_"

ydl_opts = {
    "format": "best[height<=1080]",  # 비디오+오디오가 함께 있는 최상의 포맷 선택 (ffmpeg 불필요)
    "outtmpl": "./temp.%(ext)s",
    "postprocessors": [
        {
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",  # mp4로 변환
        }
    ],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    title = info.get("title", "Unknown")
    print(f"{title} 다운로드 완료")
