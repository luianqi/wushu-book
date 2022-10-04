from django.contrib import admin

from .models import User, Referral, Club, Feedback, PhysicalIndicators, Athlete

admin.site.register(User)
admin.site.register(Referral)
admin.site.register(Club)
admin.site.register(PhysicalIndicators)
admin.site.register(Athlete)
admin.site.register(Feedback)