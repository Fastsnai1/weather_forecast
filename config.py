open_weather_token = "35d6f020402f4592030b0a6fbfb35ef7"
with open('/home/miritelli/Porject/token.txt', 'r') as t:
    token1 = t.readlines()
tg_bot_token = f'{token1[0]}'
