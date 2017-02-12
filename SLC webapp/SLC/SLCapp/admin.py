from django.contrib import admin
from SLCapp.models import UserProfile, SignUpPicture, ChatBotResponse, ChatBotContext

admin.site.register(UserProfile)
admin.site.register(SignUpPicture)
admin.site.register(ChatBotResponse)
admin.site.register(ChatBotContext)
