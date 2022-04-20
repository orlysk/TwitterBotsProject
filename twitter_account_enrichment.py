from typing import List, Dict
import requests

bearer_token = "AAAAAAAAAAAAAAAAAAAAAK%2FHbgEAAAAAcNNLTzuXuV6ThP3fz30PTJOx294%3DAGpkjKXSxcxnEzeyPJB7XVbeP20TjmLhzpdpMndBB0gIiYk5Dk"


def get_users_lookup_url(account_ids: List[str]) -> str:
    account_ids_str = ','.join(account_ids)
    url = f"https://api.twitter.com/2/users?ids={account_ids_str}"
    print(url)
    return url


def create_auth_headers() -> Dict[str, str]:
    return {"Authorization": "Bearer {}".format(bearer_token)}


def connect_to_endpoint(url: str, params: Dict[str, str]) -> Dict:
    response = requests.request("GET", url, headers=create_auth_headers(), params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

#
# users_list = ['pankajtiwari2']
# accounts_ids = ["787405734442958848", "796216118331310080"]
#
# users_lookup_params = {
#     "user.fields": "id,name,username,created_at,description,location,pinned_tweet_id,protected,public_metrics,"
#                    "verified,withheld"
# }
#
# users_lookup_url = get_users_lookup_url(accounts_ids)
#
# json_response = connect_to_endpoint(users_lookup_url, users_lookup_params)
#
# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# print(json_response)


# {'data': [
#     {'username': 'best_in_dumbest',
#      'public_metrics': {'followers_count': 1953, 'following_count': 5, 'tweet_count': 15723, 'listed_count': 56},
#      'description': 'Blame @xaiax, Inspired by @MakingInvisible, using cmu phonetic data to produce incongruous matches.\nSome images via Lorem Flickr.',
#      'protected': False, 'verified': False, 'created_at': '2016-10-15T21:32:11.000Z',
#      'pinned_tweet_id': '787407020156522496', 'name': 'The Best In Dumbest', 'id': '787405734442958848'},
#     {'location': 'United States', 'username': 'CJRubinPhoto',
#      'public_metrics': {'followers_count': 800, 'following_count': 838, 'tweet_count': 251, 'listed_count': 5},
#      'description': 'Photographing the American West since 1980. I specialize in location portraits & events, both indoors & outside, using natural light & portable studio lighting.',
#      'protected': False, 'verified': False, 'created_at': '2016-11-09T05:01:30.000Z', 'name': 'CJ Rubin',
#      'id': '796216118331310080'}]}
