import requests
import json


def get_account_info(steam_ids):

    api_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={0}&steamids={1}"\
        .format(api_token, steam_ids)

    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def get_friends(steam_id):

    api_url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={0}&steamid={1}&relationship=friend"\
        .format(api_token, steam_id)

    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def get_steam_name(steam_id):

    data = get_account_info(steam_id)
    if data:
        return data["response"]["players"][0]["personaname"]
    else:
        return None


def get_friend_ids(steam_id):

    output = []
    data = get_friends(steam_id)
    if data:
        for i in data["friendslist"]["friends"]:
            output.append(i["steamid"])
        return output
    else:
        return None


def get_owned_games(steam_id):

    api_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={0}&steamid={1}&include_appinfo=1" \
        .format(api_token, steam_id)

    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def get_game_list(steam_id):

    data = get_owned_games(steam_id)
    if data:
        output = []
        for i in data["response"]["games"]:
            output.append(i["name"])
        return output
    else:
        return None


if __name__ == "__main__":
    with open("details.txt") as f:
        lines = f.readlines()
        api_token = lines[0].rstrip()
        account_id = lines[1].rstrip()

    print("Friends:")
    friends = {}
    for i, value in enumerate(get_friend_ids(account_id)):
        friends[i] = value
        print(i, get_steam_name(value))
    choices = tuple(input("List player numbers to compare (separated by a comma): ").replace(" ", "").split(","))
    games = set(get_game_list(account_id))
    for i in choices:
        games = games.intersection(set(get_game_list(friends[int(i)])))
    for game in games:
        print(game)
