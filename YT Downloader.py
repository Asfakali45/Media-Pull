import yt_dlp

url = input("Paste Youtube Video Link:- ")

print("\nChoose the Quality of video ")
print("1. Best Quality")
print("2. 1080p")
print("3. 720p")
print("4. 480p")

choice = input("Enter the choosen option her :- ")

quality = {
    
    "1": "bestvideo+bestaudio/best",
    "2": "bestvideo[height<=1080]+bestaudio/best",
    "3": "bestvideo[height<=720]+bestaudio/best",
    "4": "bestvideo[height<=480]+bestaudio/best",
}

option = {
    "format":quality.get(choice, "bestvideo+bestaudio/best"),
    "outtmpl": "%(title)s.%(ext)s",
    "merge_output_format": "mp4"
}

with yt_dlp.YoutubeDL(option)as ydl:
    ydl.download([url])

print("\nDownload Completed")