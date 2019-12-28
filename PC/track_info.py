import os
from metadata_by_track_id import metadata
from PIL import Image, ImageDraw, ImageFont
import urllib.request
import tkinter

#get screensize
root=tkinter.Tk()
width=root.winfo_screenwidth()
height=root.winfo_screenheight()

screensize=(width, height)

#track_info=metadata(os.environ["TRACK_ID"])
#DEBUG
track_info=metadata("2Rk4JlNc2TPmZe2af99d45")

print(f"Track-Info for: {track_info['title'][0]}")
track_title=str(track_info["title"][0])
track_artists=""
for art in range(len(track_info["artists"])):
    track_artists+=str(track_info["artists"][art])+", "
track_artists=track_artists[0:-2]
print(screensize)

#get cover
urllib.request.urlretrieve("https://"+str(track_info["cover_url"][0]), "cache/cover_art.png")

#make info-screen using pillow
cover_art=Image.open("cache/cover_art.png")

img=Image.new("RGB", screensize, color="black")

font_title=ImageFont.truetype("arial.ttf", 40)
font_artists=ImageFont.truetype("arial.ttf", 30)

d=ImageDraw.Draw(img)
d.text((screensize[0]/2.15, screensize[1]/2), track_title, font=font_title, fill=(255,255,255))
d.text((screensize[0]/2.15, screensize[1]/1.75), track_artists, font=font_artists, fill=(255,255,255))

img.paste(cover_art, (int(screensize[0]/4), int(screensize[1]/2.75)))

img.save("cache/current_info.png")