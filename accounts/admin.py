from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, VendorProfile

admin.site.register(User, UserAdmin)

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_vendors']

    def approve_vendors(self, request, queryset):
        queryset.update(is_approved=True)
    approve_vendors.short_description = "Approve selected vendors"