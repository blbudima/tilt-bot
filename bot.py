# DON'T FORGET TO ENABLE THE VIRTUAL ENVIRONMENT VIA:
# .\bot-env\Scripts\activate.bat

# DON'T FORGET TO RESET RIOT API TOKEN
# https://developer.riotgames.com/
# SET THE TOKEN AS AN ENVIRONMENT VARIABLE NAMED "RIOT_API_KEY"

# ON WINDOWS, RUN BOT THROUGH POWERSHELL VIA: py -3 bot.py

import discord 
import config
import cassiopeia
from cassiopeia import Summoner, Patch

# set riot api key
cassiopeia.set_riot_api_key(config.riot_api_key)

# create new Discord client
client = discord.Client()

# on ready, say ready
@client.event
async def on_ready():
  print('Ready as {0.user}'.format(client))

@client.event
async def on_message(message):
  # ignore message from itself
  if message.author == client.user:
    return

  # extract content
  args = message.content.split()

  # check for search command
  if args[0] == config.prefix + 'search':
    # if there is no username, return
    if (len(args) == 1):
      return await message.channel.send('Incorrect usage! You need to supply a username as well!')

    # prepare name
    spaces = ' '
    args.pop(0)
    username = spaces.join(args)

    # just for console
    print('The extracted username is: ' + username)

    # send notice
    await message.channel.send('Let me check...')

    # create summoner object
    print('Attempting to create summoner object (Region NA)..')
    summoner_name = Summoner(name=username, region="NA")

    # attempt to look up match history
    print('Attempting to look up match history...')
    try:
      match_hist = summoner_name.match_history(begin_time=Patch.from_str("10.7", region="NA").start)
    except Exception as e:
      print(e)
      return await message.channel.send('That username does not exist!')

    # check if you are looking for a win streak or a loss streak
    looking_for_win = False
    if (match_hist[0].participants[summoner_name].team.win is True):
      looking_for_win = True

    # count match streak
    match_counter = 1
    while (True):
      next_turnout = match_hist[match_counter].participants[summoner_name].team.win
      if (looking_for_win and not next_turnout) or (not looking_for_win and next_turnout):
        break
      match_counter += 1

    # print results
    print('Printing out result for ' + username)
    if looking_for_win:
      return await message.channel.send(username + ' is on a ' + str(match_counter) + ' game winning streak.')
    else:
      return await message.channel.send(username + ' is on a ' + str(match_counter) + ' game losing streak.')

  # if user supplied a non-existant command, show search
  if args[0] == config.prefix + 'help':
    return await message.channel.send('The proper command is `' + config.prefix + 'search <username>`.')

# login with the client
client.run(config.token)