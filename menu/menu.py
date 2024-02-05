from django.http import HttpResponse
from django.shortcuts import render
 
def menu(request):
    
    return render(request, 'state.html', {'con' : "function_menu.html"})

def User_Agreement_txt(request):
    return render(request, 'User_Agreement.html')