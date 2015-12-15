from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

# Create your views here.
from .controller import get_controller

def chats(request):

    chat_list = get_controller().chats()

    return render(request, 'chats.html',{
        'chat_list': chat_list
    })

def messages(request, entity_id):

    message_list = get_controller().messages(entity_id)

    if (message_list == None):
        raise Http404 ("Message not found")

    return  render(request,'messages.html',{
        'message_list': message_list
    })