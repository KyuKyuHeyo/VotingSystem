from django.contrib import admin
from .models import Poll, Option, Vote

class OptionInline(admin.TabularInline):
    model = Option
    extra = 2

class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'user_limit', 'voting_security_email', 'display_names']
    inlines = [OptionInline]

class VoteAdmin(admin.ModelAdmin):
    list_display = ['poll', 'option', 'email', 'name', 'voted_at']
    list_filter = ['poll']
    search_fields = ['email', 'name']

admin.site.register(Poll, PollAdmin)
admin.site.register(Vote, VoteAdmin)
