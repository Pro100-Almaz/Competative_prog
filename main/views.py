from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
import requests


# def create_acc(request):
#     form = CreateAcc
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         if User.objects.filter(title=title).exists():
#             messages.add_message(request, messages.ERROR,
#                                  "Error")
#             return render(request, '', {'messages': [messages]})
#         else:
#             User.objects.create(
#                 creator=request.user,
#                 title=request.POST.get('title'),
#                 description=request.POST.get('description'),
#             )
#             room = User.objects.get(title=title)
#             room.room_members.add(request.user)
#             room.number_of_users = 1
#             room.save()
#             return redirect('')
#
#     context = {'form': form}
#     return render(request, '', context)

# To parse json use this peace of code
# data = requests.get('https://leetcode-stats-api.herokuapp.com/Pro100_language')
# print(data.json())