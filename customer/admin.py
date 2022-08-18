from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from customer.models import Account, Address, Customer, Producer, Telephone


class AccountAdmin(UserAdmin):
	list_display = ('email','username','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('email','username',)
	readonly_fields=('id', 'date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(Account, AccountAdmin) 
admin.site.register(Telephone)
admin.site.register(Address) 
admin.site.register(Producer)
admin.site.register(Customer)
