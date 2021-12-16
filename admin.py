from django.contrib import admin
from .models import Contact, Category, MenuItem
from Customer.models import Order
# Register your models here.
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(MenuItem)
# admin.site.register(Order)



class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "menu_item","price", "Date_created", "is_paid")
    # search_fields = ("menu_item")

    # def get_ordering(self, request):
    #     if request.user.is_superuser:
    #         return ("menu_item", "Date_created")
    #     return ("menu_item")

admin.site.register(Order, OrderAdmin)