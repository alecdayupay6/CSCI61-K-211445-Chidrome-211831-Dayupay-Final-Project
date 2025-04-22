from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

def register(request):    
    if 'username' in request.session:
        return redirect('search')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"INSERT INTO interface_user (username, password) VALUES ('{username}', '{password}')")
                return redirect("login")
            except Exception as e:
                messages.info(request, f'{e}')
    return render(request, "register.html")

def login_(request):    
    if 'username' in request.session:
        return redirect('search')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        with connection.cursor() as cursor:
            query = f"SELECT * FROM interface_user WHERE username='{username}' AND password='{password}'"
            cursor.execute(query)
            user = cursor.fetchone()
            if user:
                request.session['username'] = username
                return redirect("search")
            else:
                messages.info(request, 'Username or Password is incorrect.')
    return render(request, "login.html")

def search(request):
    if 'username' not in request.session:
        return redirect('login')
    
    results = []
    if request.method == "POST":
        search_term = request.POST['username']
        
        query = f"SELECT username FROM interface_user WHERE username = '{search_term}'"
        with connection.cursor() as cursor:
            try:
                cursor.execute(query)
                results = cursor.fetchall()
            except Exception as e:
                results = [("Error: " + str(e),)]
    
    return render(request, "search.html", {"results": results})

def delete_(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM interface_user")
        results = cursor.fetchall()
    if request.method == 'POST':
        username = request.POST['username']

        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM interface_user WHERE username = '{username}'")

        messages.info(request, f"User '{username}' deleted (if existed).")

    return render(request, 'delete.html', {"results":results})

def logout_(request):
    request.session.flush()
    return redirect("login")