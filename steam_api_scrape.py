# Import Files
import requests
import json


def get_account_info(steam_ids):
    """
    Returns the results of a steam api get request containing a summary of one or more steam users.
    :param steam_ids: A list containing the steam ids of all steam accounts you want info for.
    :return: A list containing information about one or more Steam profiles. None if request fails
    """

    api_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={0}&steamids={1}"\
        .format(api_token, steam_ids)

    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def get_friends(steam_id):
    """
    Returns the results of a steam api get request containing information about a users friend list.
    :param steam_id: A string containing the steam ID of the user to check.
    :return: The response of the aforementioned get request. None if request fails
    """

    api_url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={0}&steamid={1}&relationship=friend"\
        .format(api_token, steam_id)

    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def get_steam_name(steam_id):
    """
    Returns a user's steam display name given their steam ID
    :param steam_id: The ID of the steam user as a string
    :return: A string containing rhe user's steam display name. None if request fails.
    """

    data = get_account_info(steam_id)
    if data:
        return data["response"]["players"][0]["personaname"]
    else:
        return None


def get_friend_ids(steam_id):
    """
    Returns a list of steam IDs corresponding to a user's friend list.
    :param steam_id: The user who's friend list should be checked.
    :return: A list of strings containing the steam ids of the user's friends. None if request fails.
    """

    output = []
    data = get_friends(steam_id)
    if data:
        for i in data["friendslist"]["friends"]:
            if get_account_info(i)["response"]["players"][0]["communityvisibilitystate"] == 3: #account is visible
                output.append(i["steamid"])
        return output
    else:
        return None


def get_owned_games(steam_id):
    """
    Returns the results of a steam api get request containing information about a user's owned games.
    :param steam_id: The steam user to check.
    :return: The results of the aforementioned get request. None if request fails.
    """

    api_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={0}&steamid={1}&include_appinfo=1" \
        .format(api_token, steam_id)

    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def get_game_list(steam_id):
    """
    Returns a list of owned games given a user's steam ID.
    :param steam_id: A string containing the user's steam ID.
    :return: A list containing the names of all of the user's owned games.
    """

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
