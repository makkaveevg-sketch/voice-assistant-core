from pystray import Icon, Menu, MenuItem
from PIL import Image

def quit_app(icon):
    icon.stop()

image = Image.new(
    "RGB",
    (64, 64),
    color=(0, 0, 255)
)

icon = Icon(
    "Vik",
    image,
    menu=Menu(
        MenuItem("Выход", quit_app)
    )
)

icon.run()