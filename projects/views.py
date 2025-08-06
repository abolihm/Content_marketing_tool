from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection


@login_required
def add_project_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        website_category = request.POST.get('website_category')
        number_of_publications = request.POST.get('number_of_publications')
        domain_authority = request.POST.get('domain_authority')
        domain_rating = request.POST.get('domain_rating')
        team_allocation = request.POST.get('team_allocation')
        geolocation = request.POST.get('geolocation')
        targets = request.POST.get('targets')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO add_new_project 
                (name, website_category, number_of_publications, domain_authority, domain_rating, team_allocation, geolocation, targets)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                name, website_category, number_of_publications,
                domain_authority, domain_rating, team_allocation,
                geolocation, targets
            ])

        return redirect('/dashboard/')

    return render(request, 'add_project.html')


@login_required
def add_in_existing_project_view(request):
    if request.method == 'POST':
        data = {
            'month': request.POST.get('month'),
            'project_name': request.POST.get('project_name'),
            'publication_site': request.POST.get('publication_site'),
            'keyword_1': request.POST.get('keyword_1'),
            'url_page_1': request.POST.get('url_page_1'),
            'keyword_2': request.POST.get('keyword_2'),
            'url_page_2': request.POST.get('url_page_2'),
            'live_url': request.POST.get('live_url'),
            'live_url_date': request.POST.get('live_url_date') or None,
            'status': request.POST.get('status'),
            'price': request.POST.get('price'),
            'invoice_number': request.POST.get('invoice_number'),
            'invoice_link': request.POST.get('invoice_link'),
            'blogger_name': request.POST.get('blogger_name'),
            'est_number': request.POST.get('est_number'),
            'billed_status': request.POST.get('billed_status'),
            'client_invoice_no': request.POST.get('client_invoice_no'),
            'collected_status': request.POST.get('collected_status'),
            'payment_status': request.POST.get('payment_status'),
            'released_date': request.POST.get('released_date') or None,
            'transaction_id': request.POST.get('transaction_id'),
        }

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO add_existing_project (
                    month, project_name, publication_site,
                    keyword_1, url_page_1, keyword_2, url_page_2,
                    live_url, live_url_date, status, price,
                    invoice_number, invoice_link, blogger_name,
                    est_number, billed_status, client_invoice_no,
                    collected_status, payment_status, released_date,
                    transaction_id
                )
                VALUES (
                    %(month)s, %(project_name)s, %(publication_site)s,
                    %(keyword_1)s, %(url_page_1)s, %(keyword_2)s, %(url_page_2)s,
                    %(live_url)s, %(live_url_date)s, %(status)s, %(price)s,
                    %(invoice_number)s, %(invoice_link)s, %(blogger_name)s,
                    %(est_number)s, %(billed_status)s, %(client_invoice_no)s,
                    %(collected_status)s, %(payment_status)s, %(released_date)s,
                    %(transaction_id)s
                )
            """, data)

        return redirect('/dashboard/')

    return render(request, 'add_in_existing_project.html')
