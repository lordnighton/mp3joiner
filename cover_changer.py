from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

audio = MP3("/Users/mykyta_kharchenko/Downloads/4.mp3", ID3=ID3)

try:
    audio.add_tags()
except error:
    pass

audio.tags.add(
    APIC(
        encoding=3, # 3 is for utf-8
        mime='image/jpeg', # image/jpeg or image/png
        type=3, # 3 is for the cover image
        desc=u'Front Cover',
        data=open("cover.jpg", 'rb').read()
    )
)
audio.save(v2_version=3)