from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return render(request, 'webapp/index.html')
	def about(request):
	return render(request, 'webapp/about.html')
	def contact(request):
	return render(request, 'webapp/contact.html')
	def advies(request):
	return render(request, 'webapp/advies.html')
	def huren(request):
	return render(request, 'webapp/huren.html')
	def kopen(request):
	return render(request, 'webapp/kopen.html')
	def login(request):
	return render(request, 'webapp/login.html')
	def partners(request):
	return render(request, 'webapp/partners.html')