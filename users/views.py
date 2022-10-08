from django.shortcuts import render
from .models import UsersList, Contest
from .forms import CreateAcc
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
import requests
from datetime import datetime, timedelta
import pytz
import json


def main_list(request):
    utc = pytz.UTC

    users = UsersList.objects.order_by('-rating')
    contest = Contest.objects.get(id = 1)
    if datetime.today().weekday() == 6:
        contest.weekly_contest +=1

    biweekly_day = contest.biweekly_date

    if utc.localize(datetime.today()) > biweekly_day:
        contest.biweekly_date += timedelta(days=14)
        contest.biweekly_contest+=1

    contest.save()
    w_contest_day = contest.weekly_contest
    b_contest_day = contest.biweekly_contest
    w_contest_link = "https://leetcode.com/contest/weekly-contest-" + str(w_contest_day) + "/"
    b_contest_link = "https://leetcode.com/contest/biweekly-contest-" + str(b_contest_day) + "/"
    user_count = len(users)
    index_num = 1
    for i in users:
        i.index = index_num
        index_num+=1

    context = {'users': users, 'user_count': user_count, 'contest_weekly': w_contest_day,
               'contest_biweekly': b_contest_day, 'w_contest_link': w_contest_link,
               'b_contest_link': b_contest_link}
    return render(request, 'main_page.html', context)

def get_image(username):
    cookies = {
        '__stripe_mid': '7b95eb48-7e92-492c-bc68-f080d4700cdc527ad7',
        'csrftoken': '9LNO9dIUeEQy2OlTzzdCjWiE7hAbV5l7lZMuJbHu5zjcF8ljvAdVlbrqrd4ZfKPj',
        'LEETCODE_SESSION': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMzk0MDA0MiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjFiZWFiMzc0ZDE0NmNjMDgxYzljNWY2ODFjMjljNjkxYTRkYWE4YzIiLCJpZCI6Mzk0MDA0MiwiZW1haWwiOiJlbGFtaXJrYWRAZ21haWwuY29tIiwidXNlcm5hbWUiOiJlbGFtaXJrYWQiLCJ1c2VyX3NsdWciOiJlbGFtaXJrYWQiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY2MDE0NDExMC5wbmciLCJyZWZyZXNoZWRfYXQiOjE2NjA1ODM2NzcsImlwIjoiMTg1LjQ4LjE0OC4xODgiLCJpZGVudGl0eSI6IjRjYTQyZjc4ZmRhNDM3NTgyZTc3YjlmOWE0NWMzMzc2Iiwic2Vzc2lvbl9pZCI6MjU2ODY4OTh9.nEXCBrK0EImkWB4UsuOJZJAaCWJtEQva-eAAybw0eUk',
    }

    headers = {
        'authority': 'leetcode.com',
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,es;q=0.6',
        'origin': 'https://leetcode.com',
        'referer': 'https://leetcode.com/sulrz/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54',
        'x-csrftoken': '9LNO9dIUeEQy2OlTzzdCjWiE7hAbV5l7lZMuJbHu5zjcF8ljvAdVlbrqrd4ZfKPj',
        'x-kl-ajax-request': 'Ajax_Request',
    }

    json_data = {
        'query': '\n    query userProfile($username: String!) {\n  matchedUser(username: $username) {\n  profile {\n       userAvatar\n      }\n  }\n}\n    ',
        'variables': {
            'username': username,
        },
    }

    response = requests.post('https://leetcode.com/graphql/', cookies=cookies, headers=headers, json=json_data)
    data = json.loads(response.text)
    return data["data"]["matchedUser"]["profile"]["userAvatar"]

def return_rating(link):
    cookies = {
        '__stripe_mid': '7b95eb48-7e92-492c-bc68-f080d4700cdc527ad7',
        'csrftoken': '9LNO9dIUeEQy2OlTzzdCjWiE7hAbV5l7lZMuJbHu5zjcF8ljvAdVlbrqrd4ZfKPj',
        'c_a_u': 'ZWxhbWlya2Fk:1oNd3S:iLsnvAfAKpYVLmVkpz4aHeWaPd0',
        'LEETCODE_SESSION': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMzk0MDA0MiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjFiZWFiMzc0ZDE0NmNjMDgxYzljNWY2ODFjMjljNjkxYTRkYWE4YzIiLCJpZCI6Mzk0MDA0MiwiZW1haWwiOiJlbGFtaXJrYWRAZ21haWwuY29tIiwidXNlcm5hbWUiOiJlbGFtaXJrYWQiLCJ1c2VyX3NsdWciOiJlbGFtaXJrYWQiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY2MDE0NDExMC5wbmciLCJyZWZyZXNoZWRfYXQiOjE2NjA0MTAzNDYsImlwIjoiODcuMjU1LjIxNi43NSIsImlkZW50aXR5IjoiNGNhNDJmNzhmZGE0Mzc1ODJlNzdiOWY5YTQ1YzMzNzYiLCJzZXNzaW9uX2lkIjoyNTY4Njg5OH0.-rE2i8MIp42u4t5xdhLd0ikTgvREcM73w1UAkPPelIM',
    }

    headers = {
        'authority': 'leetcode.com',
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,es;q=0.6',
        # Already added when you pass json=
        # 'content-type': 'application/json',
        # Requests sorts cookies= alphabetically
        # 'cookie': '__stripe_mid=7b95eb48-7e92-492c-bc68-f080d4700cdc527ad7; csrftoken=9LNO9dIUeEQy2OlTzzdCjWiE7hAbV5l7lZMuJbHu5zjcF8ljvAdVlbrqrd4ZfKPj; c_a_u=ZWxhbWlya2Fk:1oNd3S:iLsnvAfAKpYVLmVkpz4aHeWaPd0; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMzk0MDA0MiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjFiZWFiMzc0ZDE0NmNjMDgxYzljNWY2ODFjMjljNjkxYTRkYWE4YzIiLCJpZCI6Mzk0MDA0MiwiZW1haWwiOiJlbGFtaXJrYWRAZ21haWwuY29tIiwidXNlcm5hbWUiOiJlbGFtaXJrYWQiLCJ1c2VyX3NsdWciOiJlbGFtaXJrYWQiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY2MDE0NDExMC5wbmciLCJyZWZyZXNoZWRfYXQiOjE2NjA0MTAzNDYsImlwIjoiODcuMjU1LjIxNi43NSIsImlkZW50aXR5IjoiNGNhNDJmNzhmZGE0Mzc1ODJlNzdiOWY5YTQ1YzMzNzYiLCJzZXNzaW9uX2lkIjoyNTY4Njg5OH0.-rE2i8MIp42u4t5xdhLd0ikTgvREcM73w1UAkPPelIM',
        'origin': 'https://leetcode.com',
        'referer': 'https://leetcode.com/ressley/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54',
        'x-csrftoken': '9LNO9dIUeEQy2OlTzzdCjWiE7hAbV5l7lZMuJbHu5zjcF8ljvAdVlbrqrd4ZfKPj',
        'x-kl-ajax-request': 'Ajax_Request',
    }


    json_data = {
        'query': '\n    query userContestRankingInfo($username: String!) {\n  userContestRanking(username: $username) {\n    attendedContestsCount\n    rating\n    topPercentage\n    }\n  }\n',
        'variables': {
            'username': link,
        },
    }

    response = requests.post('https://leetcode.com/graphql/', cookies=cookies, headers=headers, json=json_data)
    data = json.loads(response.text)
    try:
        temp = round(data["data"]["userContestRanking"]["rating"])
    except:
        temp = 0
    try:
        contests_num = data["data"]["userContestRanking"]["attendedContestsCount"]
    except:
        contests_num = 0
    try:
        percentage = data["data"]["userContestRanking"]['topPercentage']
    except:
        percentage = 0
    return temp, contests_num, percentage

def add_account(request):
    data = CreateAcc(request.POST)
    if request.method == "POST":
        name = request.POST.get('login')
        email = request.POST.get('email')

        get_string = 'https://leetcode-stats-api.herokuapp.com/' + str(name).lower()

        data_of_acc = requests.get(get_string)
        data_about_user = data_of_acc.json()
        user_rating = return_rating(name)

        if UsersList.objects.filter(name = name).exists():
            messages.add_message(request, messages.ERROR,
                                 "Room with this title already exists, please choose another title")
            return render(request, 'main_page.html', {'messages': [messages]})
        else:
            UsersList.objects.create(
                name = name,
                email = email,
                number_of_problems = data_about_user['totalSolved'],
                rating = user_rating[0],
                image_url = get_image(name),
                ez_problems = data_about_user['easySolved'],
                medium_problems = data_about_user['mediumSolved'],
                hard_problems = data_about_user['hardSolved'],
                contest_num = user_rating[2],
            )

            return redirect('main')

    context = {'data': data}
    return render(request, 'add_acc.html', context)