from .models import SiteSettings

def site_settings(request):
	return {
	'setting':SiteSettings.objects.first()
	}