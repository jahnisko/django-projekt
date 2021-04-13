from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Pojistovna)
admin.site.register(Pojistenec)
admin.site.register(Osoba)
admin.site.register(Test)
admin.site.register(Laborator)
admin.site.register(Misto)