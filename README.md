# Xtra-Plugins - FridayUB ✨
> A Repo That Contains Many X-Tra Plugins From FridayDevs And Third Parties.

# Example 👊

### Plugins 🔧

```python
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply

@friday_on_cmd(['helloworld'],
    cmd_help={
    "help": "This is A TEST",
    "example": ".helloworld")
async def hello_world(client, message):
    mg = await edit_or_reply(message, "`Hello World! This Works!`")
```
### Custom Filters 📣

```python
from main_startup.core.decorators import listen

@listen(filters.mentioned & ~filters.me)
async def mentioned_(client, message):
    await message.reply_text("`Hello World! Btw Why Did You Mention Me?`")
```

# Contributing 🎨
* Contributers Are Always Welcome. You Can Contribute To This Project With Your Plugins.
### How To?
* Just Create A Pull Request With Your Plugin And Some Info in Description.
* Please Make Sure Your Plugin Passes The GuideLines.
### GuideLines
* No Stealing. Please Don't Steal Any Plugins. 
* If You Have Ported The Plugin, Make Sure To Mention Real Creator Of The Plugin.
* Plugin Should Be Linted Before Creating Pull Request

> Thats All, Happy Contributing!
