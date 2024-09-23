import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

class VerifyModal(Modal):
    def __init__(self):
        super().__init__(title="การยืนยันตัวตน")
        self.birth_year = TextInput(label="พ.ศ. เกิด", placeholder="", required=True)
        self.add_item(self.birth_year)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            birth_year = int(self.birth_year.value)
            current_year = 2567  # ปี พ.ศ. ปัจจุบัน
            age = current_year - birth_year
            
            if age >= 16:
                role = discord.utils.get(interaction.guild.roles, name="Verified")
                if role:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"{interaction.user.mention} คุณผ่านการยืนยันแล้วและได้รับยศ '{role.name}'!", ephemeral=True)

                    # ส่งข้อความไปยังช่องที่กำหนดโดยใช้ ID
                    channel_id = 1287752078491390002  # เปลี่ยนเป็น ID ของช่องที่ต้องการส่ง
                    channel = bot.get_channel(channel_id)
                    if channel:
                        await channel.send(f"{interaction.user.mention} ยืนยันเรียบร้อยแล้ว! 🎉\n[ยืนยันสำเร็จ](https://i.pinimg.com/originals/e9/e2/86/e9e286a9cbb4eec59d3309a1ac538182.gif)")
                else:
                    await interaction.response.send_message(f"ไม่พบยศ 'Verified' ในเซิร์ฟเวอร์นี้", ephemeral=True)
            else:
                await interaction.response.send_message(f"{interaction.user.mention} คุณไม่ผ่านการยืนยัน เพราะอายุไม่ถึง 16 ปี\n[ยืนยันไม่สำเร็จเพราะมึงโง่](https://i.pinimg.com/originals/ae/d8/74/aed874bdf3adc009fb87be83d909171c.gif)", ephemeral=True)

        except ValueError:
            await interaction.response.send_message("กรุณากรอก พ.ศ. เป็นตัวเลข", ephemeral=True)

class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ กดตรงนี้เพื่อยืนยัน", style=discord.ButtonStyle.success)
    async def verify_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = VerifyModal()
        await interaction.response.send_modal(modal)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def pig(ctx):
    view = VerifyButton()
    await ctx.send("กดปุ่มด้านล่างเพื่อยืนยันตัวตน", view=view)

TOKEN = os.getenv('DISCORD_TOKEN')  # ใช้ Environment Variable สำหรับ Token
bot.run(TOKEN)  # เรียกใช้งานบอท
