import convert_drawings_to_video
import convert_video_to_drawing
import download_youtube_video

#max 1million frames to a video or about 27hours at 10fps

types_of_link=["A. youtube link", "B. file link"]
for link in types_of_link:
    print(link)
method_of_video=str(input("Enter method of video(eg. A): "))
method_of_video=method_of_video.lower()

if method_of_video == "a":
    link=input("Enter the link of video: ")
    path=download_youtube_video.download_youtube_video(link)

elif method_of_video == "b":
    path=input("Enter the path to the video: ")

else:
    print("this will now crash")

print("drawing frames")
convert_video_to_drawing.extract_frames(path, "output_frames", "output_frames_lines", sample_rate=0.1)

print("making the video")
convert_drawings_to_video.images_to_video("output_frames_lines", "output.mp4", fps=10)

