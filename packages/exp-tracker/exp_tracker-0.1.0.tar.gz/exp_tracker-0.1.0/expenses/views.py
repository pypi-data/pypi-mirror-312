from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ExpenseForm
#from chartjs import get_chart_data
from .models import Expense
from django.db.models import Sum, F
from django.core.paginator import Paginator
from django.contrib import messages
import json,csv
from django.http import HttpResponse
from django.db.models.functions import ExtractYear

def home(request):
    # if user_login == 'POST':
    #     return redirect('expense_list')
    # else:
    #     form = AuthenticationForm()
    return render(request, 'expenses/home.html')
    
    

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('expense_list')
    else:
        form = RegisterForm()
    return render(request, 'expenses/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('expense_list')
    else:
        form = AuthenticationForm()
    return render(request, 'expenses/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    category_totals = (
        expenses.values('category')
        .annotate(total=Sum('amount'))
        .order_by('category')
    )
    paginator = Paginator(expenses, 5)  # It will help to show 5 records
    page_number = request.GET.get('page')  # page numbers
    page_obj = paginator.get_page(page_number)
    # categories = expenses.values('category').annotate(total=Sum('amount'))
    category_labels = [entry['category'] for entry in category_totals]
    category_sums = [float(entry['total']) for entry in category_totals]

    category_labels_json = json.dumps(category_labels)
    category_sums_json = json.dumps(category_sums)
    return render(request, 'expenses/expense_list.html', {
        'page_obj': page_obj,
        'expenses': expenses,
        'category_labels': category_labels_json,
        'category_sums': category_sums_json,
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def delete_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expenses/delete_expense.html', {'expense': expense})

@login_required
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)   
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expense_list')
        else:
            print("Form errors:", form.errors)
            messages.error(request, 'There was an error updating the expense.')
    else:
        form = ExpenseForm(instance=expense)
    
    return render(request, 'expenses/edit_expense.html', {'form': form})

@login_required
def download_expenses_csv(request):
    # Create the HttpResponse object with the appropriate CSV headers.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    # Write header row
    writer.writerow(['Title', 'Amount', 'Category', 'Date', 'Description'])

    # Write expense data
    expenses = Expense.objects.filter(user=request.user).values_list('title', 'amount', 'category', 'date', 'description')
    for expense in expenses:
        writer.writerow(expense)

    return response

@login_required
def expense_graph(request):
    # Group expenses by year and category
    expenses = Expense.objects.filter(user=request.user).annotate(
        year=ExtractYear('date')  # Extract year from the date field
    ).values('year', 'category').annotate(
        total_amount=Sum('amount')
    ).order_by('year')

    # Organize data for the graph
    data = {}
    for expense in expenses:
        year = str(expense['year'])  
        category = expense['category']
        amount = float(expense['total_amount'])

        if category not in data:
            data[category] = {}

        data[category][year] = amount
    
    category_colors = {
        'Food': '#FF5733',  # Red-Orange
        'Transport': '#33FF57',  # Green
        'Shopping': '#5733FF',  # Blue
        'Utilities': '#FFD133',  # Yellow
        'Others': '#33FFF5',  # Cyan
    }

    # Create datasets for Chart.js
    years = sorted({str(expense['year']) for expense in expenses})  # It is for show unique years
    datasets = []

    for category, values in data.items():
        color = category_colors.get(category, '#CCCCCC')
        datasets.append({
            'label': category,
            'data': [values.get(year, 0) for year in years],
            'fill': False,
            'borderColor': color,  # To give colour to the line
            'backgroundColor': color,  # Its for background colour
            'tension': 0.3,
        })

    context = {
        'labels': json.dumps(years),
        'datasets': json.dumps(datasets),
    }
    return render(request, 'expenses/yearly_expense.html', context)




@login_required
def expense_report(request):
    expenses = Expense.objects.filter(user=request.user)
    categories = [expense.category for expense in expenses]
    amounts = [expense.amount for expense in expenses]

    # Get chart data
    # chart_data = get_chart_data(categories, amounts)
    # return render(request, 'expenses/report.html', {'chart_data': chart_data})

