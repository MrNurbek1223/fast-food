from django.contrib import admin
from page.models import User
from app.branch.api.branch.models import Branch
from app.food.api.food.models import FoodItem, Category
from app.order.api.order.models import Order ,OrderItem



class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'branch', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    actions = ['mark_as_preparing', 'mark_as_on_the_way']

    def mark_as_preparing(self, request, queryset):
        queryset.update(status='preparing')

    mark_as_preparing.short_description = "Tayyorlanmoqda deb belgilash"

    def mark_as_on_the_way(self, request, queryset):
        queryset.update(status='on_the_way')

    mark_as_on_the_way.short_description = "Yo'lga chiqdi deb belgilash"


admin.site.register(User)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Branch)
admin.site.register(FoodItem)
admin.site.register(Category)
