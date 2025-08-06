from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def add_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        number_of_projects = request.POST.get('number_of_projects')
        project_category = request.POST.get('project_category')
        number_of_publications = request.POST.get('number_of_publications')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO add_user 
                (username, number_of_projects, project_category, number_of_publications)
                VALUES (%s, %s, %s, %s)
            """, [
                username,
                int(number_of_projects),
                project_category,
                int(number_of_publications)
            ])

        return redirect('/dashboard/')

    return render(request, 'add_user.html')




@login_required
def user_dashboard_view(request):
    username = request.user.username

    with connection.cursor() as cursor:

        # ✅ Total projects from project table
        cursor.execute("""
            SELECT COUNT(DISTINCT project_name)
            FROM add_in_existing_project
            WHERE blogger_name = %s
        """, [username])
        total_projects = cursor.fetchone()[0]

        # ✅ Allocated Links
        cursor.execute("""
            SELECT COUNT(*) FROM add_in_existing_project
            WHERE blogger_name = %s
        """, [username])
        allocated_links = cursor.fetchone()[0]

        # ✅ Live Links
        cursor.execute("""
            SELECT COUNT(*) FROM add_in_existing_project
            WHERE blogger_name = %s AND status = 'Live'
        """, [username])
        live_links = cursor.fetchone()[0]

        # ✅ Pending Links
        cursor.execute("""
            SELECT COUNT(*) FROM add_in_existing_project
            WHERE blogger_name = %s AND status = 'Pending'
        """, [username])
        pending_links = cursor.fetchone()[0]

        # ✅ Bar chart (Project vs Status Count)
        cursor.execute("""
            SELECT 
                project_name,
                COUNT(*) FILTER (WHERE status = 'Allocated') as allocated,
                COUNT(*) FILTER (WHERE status = 'Live') as live,
                COUNT(*) FILTER (WHERE status = 'Pending') as pending
            FROM add_in_existing_project
            WHERE blogger_name = %s
            GROUP BY project_name
        """, [username])
        bar_chart_data = cursor.fetchall()

        # ✅ Table data
        cursor.execute("""
            SELECT 
                month, project_name, publication_site, keyword_1, url_page_1, 
                keyword_2, url_page_2, live_url, live_url_date, status, price,
                invoice_number, invoice_link, blogger_name, est_number, 
                billed_status, client_invoice_no, collected_status, 
                payment_status, released_date, transaction_id
            FROM add_in_existing_project
            WHERE blogger_name = %s
        """, [username])
        columns = [col[0] for col in cursor.description]
        table_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'user_dashboard.html', {
        'username': username,
        'total_projects': total_projects,
        'allocated_links': allocated_links,
        'live_links': live_links,
        'pending_links': pending_links,
        'bar_chart_data': bar_chart_data,
        'table_data': table_data,
    })
    
