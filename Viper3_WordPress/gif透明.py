from PIL import Image, ImageSequence

global frame


def write_gif3(gif):
    global frame
    frames = []
    img = Image.open(gif)
    mask = Image.new("RGBA", img.size, (255, 255, 255, 0))
    for frame in ImageSequence.Iterator(img):
        f = frame.copy().convert("RGBA")
        frames.append(Image.alpha_composite(mask, f))

    img = Image.new("RGBA", frame.size, (255, 255, 255, 0))
    img.save("pipixia4.gif", save_all=True, append_images=frames, loop=0, transparency=0, disposal=2)


write_gif3('E:/北京石油化工学院/rfzf.top/加载中.gif')
