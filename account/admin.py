from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account import models


class AccountAdmin(UserAdmin):
	list_display = (
		'email', 'username', 'updated_at', 'last_login', 'is_admin',
		'is_staff'
	)
	search_fields = ('email', 'username',)
	readonly_fields = ('id', 'updated_at', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(models.Account, AccountAdmin) 


@admin.register(models.Producer)
class ProducerAdmin(admin.ModelAdmin):
	list_display = (
		"account", "business_name", "cnpj", "fantasy_name",
		"state_registration", "municype_registration"
	)
	search_fields = ("business_name", "cnpj")


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ("account", "first_name", "last_name", "cpf", "britday",)
	search_fields = ("first_name", "cpf")


@admin.register(models.Address) 
class AddressAdmin(admin.ModelAdmin):
	list_display = (
		"account", "telephone", "uf", "zipcode", "city", 
		"neighborhood", "number", "street",  
	)
	search_fields = (
		"account", "telephone", "uf", "zipcode" 
	)
