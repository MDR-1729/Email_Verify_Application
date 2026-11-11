from django.contrib import admin
from .models import VerifiedEmail

@admin.register(VerifiedEmail)
class VerifiedEmailAdmin(admin.ModelAdmin):
	list_display = ('email', 'verified_at')
	search_fields = ('email',)
	ordering = ('-verified_at',)
	list_per_page = 50
	readonly_fields = ('email', 'verified_at')

	def has_add_permission(self, request):
		return False