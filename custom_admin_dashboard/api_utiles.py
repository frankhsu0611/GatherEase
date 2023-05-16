from django.http import HttpResponse
import openpyxl
from openpyxl.utils import get_column_letter
import json
from django.http import JsonResponse
from authentication.models import Ticket

def download_userprofiles_template(request):
    wb = openpyxl.Workbook()
    sheet = wb.active

    headers = ["Username", "First Name", "Last Name", "Email", "Password", "User Category", "User Country", "Track Code", "User University"]
    for i, header in enumerate(headers, start=1):
        col_letter = get_column_letter(i)
        sheet.column_dimensions[col_letter].width = 15
        sheet.cell(row=1, column=i, value=header)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=userprofiles_template.xlsx'
    wb.save(response)

    return response


def process_ticket(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ticket_id = data.get('ticket_id')
        print("Ticket ID:", ticket_id)
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
            ticket.checkin = True
            ticket.save()
            print("Check-in updated successfully")
            return JsonResponse({"success": True})
        except Ticket.DoesNotExist:
            print("Ticket not found")
            return JsonResponse({"success": False})
    return JsonResponse({"success": False})