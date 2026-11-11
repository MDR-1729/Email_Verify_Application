from django.db import models

class VerifiedEmail(models.Model):
	email = models.EmailField(unique=True)
	verified_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-verified_at']
		verbose_name = 'verified email'
		verbose_name_plural = 'verified emails'

	def __str__(self):
		return self.email
