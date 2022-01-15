from django.shortcuts import render

def inicio(req):
    return render(req,'index.html')
