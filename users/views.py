from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from .decorators import role_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def add_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email_id = request.POST.get('email_id')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO add_user (username, email_id)
                VALUES (%s, %s)
            """, [username, email_id])

        return redirect('/dashboard/')

    return render(request, 'add_user.html')



@login_required
def user_dashboard_view(request):
    selected_user = request.GET.get('user', '')

    # Fetch distinct usernames from add_in_existing_project
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT username FROM add_in_existing_project")
        users = [row[0] for row in cursor.fetchall()]

    if not selected_user and users:
        selected_user = users[0]

    # Fetch project names for selected user from add_new_project
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT name
            FROM add_new_project
            WHERE %s = ANY (string_to_array(team_allocation, ','))
        """, [selected_user])
        project_names = [row[0] for row in cursor.fetchall()]

    if not project_names:
        return render(request, 'user_dashboard.html', {
            'users': users,
            'selected_user': selected_user,
            'total_projects': 0,
            'allocated_links': 0,
            'live_links': 0,
            'pending_links': 0,
            'bar_chart_data': [],
            'table_data': [],
        })

    # Get chart data from add_in_existing_project
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                project_name,
                COUNT(*) FILTER (WHERE status IS NOT NULL) AS allocated,
                COUNT(*) FILTER (WHERE status = 'Live') AS live,
                COUNT(*) FILTER (WHERE status = 'Pending') AS pending
            FROM add_in_existing_project
            WHERE project_name IN %s
            GROUP BY project_name
        """, [tuple(project_names)])
        bar_chart_data = cursor.fetchall()

    # Get table data from add_in_existing_project
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                project_name, publication_site, month, keyword_1, url_page_1, 
                keyword_2, url_page_2, status, live_url, live_url_date,
                price, invoice_number, invoice_link, blogger_name, 
                billed_status, client_invoice_no, collected_status, payment_status, released_date, transaction_id
            FROM add_in_existing_project
            WHERE project_name IN %s
        """, [tuple(project_names)])
        table_data = [
            dict(zip([col[0] for col in cursor.description], row))
            for row in cursor.fetchall()
        ]

    context = {
        'users': users,
        'selected_user': selected_user,
        'total_projects': len(project_names),
        'allocated_links': sum(row[1] for row in bar_chart_data),
        'live_links': sum(row[2] for row in bar_chart_data),
        'pending_links': sum(row[3] for row in bar_chart_data),
        'bar_chart_data': bar_chart_data,
        'table_data': table_data,
    }

    return render(request, 'user_dashboard.html', context)


def no_permission_view(request):
    return render(request, 'no_permission.html')
