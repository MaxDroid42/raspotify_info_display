import os
from metadata_by_track_id import metadata
from PIL import Image, ImageDraw, ImageFont
import urllib.request

#set path to where the script is saved
home_path="/home/pi/metadata/"

#set screensize manually
screensize=(1920, 1080)

track_info=metadata(os.environ["TRACK_ID"])

print(f"Track-Info for: {track_info['title'][0]}")

#get title and artist
track_title=str(track_info["title"][0])
track_artists=""
for art in range(len(track_info["artists"])):
    track_artists+=str(track_info["artists"][art])+", "
track_artists=track_artists[0:-2]
print(screensize)

#get cover
urllib.request.urlretrieve("https://"+str(track_info["cover_url"][0]), f"{home_path}cache/cover_art.png")
cover_art=Image.open(f"{home_path}cache/cover_art.png")

#make info-screen using pillow
img=Image.new("RGB", screensize, color="black")

font_title=ImageFont.truetype("DejaVuSansMono.ttf", 65)
font_artists=ImageFont.truetype("DejaVuSansMono.ttf", 40)

d=ImageDraw.Draw(img)
d.text((screensize[0]/2.7, screensize[1]/2), track_title, font=font_title, fill=(255,255,255))
d.text((screensize[0]/2.7, screensize[1]/1.75), track_artists, font=font_artists, fill=(255,255,255))

img.paste(cover_art, (int(screensize[0]/5.1), int(screensize[1]/2.75)))

img.save(f"{home_path}cache/current_info.png")

#replace old info-screen
os.system("sudo killall -9 fbi")
os.system("sudo fbi --noverbose -T 1 -d /dev/fb0 /home/pi/metadata/cache/current_info.png")
