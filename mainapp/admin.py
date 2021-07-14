from django.contrib import admin

from .models import CustomerLog, PurchasedItems


admin.site.register(CustomerLog)
admin.site.register(PurchasedItems)
