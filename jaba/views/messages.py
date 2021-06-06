from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from ..models import Chat, Product, User
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)


class InboxCreateView(CreateView):
    model = Chat
    fields = ('receiver', 'message',)
    template_name = "jaba/message.html"

    def form_valid(self, form):
        
        chat = form.save(commit=False)
        chat.sender = self.request.user 
        chat.save()
        return redirect('home')
