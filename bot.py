import discord
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True  # ให้บอทสามารถอ่านข้อความได้
intents.members = True  # ให้บอทเข้าถึงข้อมูลสมาชิก

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def verify(ctx):
    await ctx.send(f"เราได้ส่งให้คุณยืนยันแล้วใน DM, {ctx.author.mention}")
    
    try:
        await ctx.author.send("กรุณากรอกเลขบัตรประชาชนของคุณ")

        def check(msg):
            return msg.author == ctx.author

        msg = await bot.wait_for('message', timeout=60.0, check=check)
        id_number = msg.content.strip()

        # คำนวณปีเกิด เดือน และวันจากเลขบัตรประชาชน
        birth_year = int(id_number[1:3]) + 2000 if id_number[0] == '0' else int(id_number[1:3]) + 1900
        birth_month = int(id_number[3:5])  # เดือนเกิด
        birth_day = int(id_number[5:7])    # วันเกิด

        # สร้างวันที่เกิด
        birth_date = datetime(birth_year, birth_month, birth_day)
        current_date = datetime.now()

        # คำนวณอายุ
        age = (current_date - birth_date).days // 365

        if age >= 16:
            await ctx.author.send("คุณผ่านการยืนยันแล้ว! ยินดีด้วย")
            await ctx.author.send(embed=discord.Embed().set_image(url='https://i.pinimg.com/originals/e9/e2/86/e9e286a9cbb4eec59d3309a1ac538182.gif'))

            role = discord.utils.get(ctx.guild.roles, name="Verified")
            if role:
                await ctx.author.add_roles(role)
                await ctx.author.send(f"คุณได้รับยศ '{role.name}' แล้ว!")
            else:
                await ctx.author.send("ไม่พบยศที่ต้องการเพิ่ม โปรดตรวจสอบชื่อยศ")
        else:
            await ctx.author.send("คุณไม่ผ่านการยืนยัน เนื่องจากอายุต่ำกว่า 16 ปี")
            await ctx.author.send(embed=discord.Embed().set_image(url='https://i.pinimg.com/originals/ae/d8/74/aed874bdf3adc009fb87be83d909171c.gif'))
    except:
        await ctx.author.send("มีข้อผิดพลาดในการตรวจสอบ โปรดลองใหม่อีกครั้ง")

bot.run('MTI4NzM1MjA0Mzc1NzEwOTI2OQ.GUALQK.hs9B7QsNC-cmw1pwgW03NJMzwhmn-2eIenasBA')
