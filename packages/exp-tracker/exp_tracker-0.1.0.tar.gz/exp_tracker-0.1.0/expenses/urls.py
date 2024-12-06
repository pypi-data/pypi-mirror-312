from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('expense_list/', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'), # Url for Expense_list
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'), # Url of delete function
    path('expense/edit/<int:id>/', views.edit_expense, name='edit_expense'), # Url for Edit expense
    path('expenses/download_csv/', views.download_expenses_csv, name='download_expenses_csv'), # Url for download expenses report
    path('expense_graph/', views.expense_graph, name='expense_graph'), # Url for navigate to graph of expensees
]
