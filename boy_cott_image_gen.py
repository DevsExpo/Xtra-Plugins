from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.helper_func.basic_helpers import edit_or_reply, get_readable_time, delete_or_pass, progress, is_admin_or_owner, get_user, get_text, iter_chats, edit_or_send_as_file
from PIL import Image, ImageDraw, ImageFont, ImageColor

@friday_on_cmd(['bcig'])
async def boycott_kangs(client, message):
  background = Image.open("test1.png")
  foreground = Image.open("test2.png")
  background.paste(foreground, (0, 0), foreground)
