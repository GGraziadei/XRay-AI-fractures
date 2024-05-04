from typing import Any
from django.contrib import admin
from django.http import HttpRequest, HttpResponse

# Register your models here.
from .models import *


admin.site.register(User)


class ReportFileInline(admin.TabularInline):
    model = ReportFile
    extra = 0

class PatientFileInline(admin.TabularInline):
    model = PatientFile
    # add external link
    
    extra = 0

class RecordInline(admin.TabularInline):
    model = Record
    extra = 0

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'modified_at']
    search_fields = ['user', 'created_at', 'modified_at']
    list_filter = ['user', 'created_at', 'modified_at']
    #fields = ['user', 'created_at', 'modified_at']
    readonly_fields = ['created_at', 'modified_at']
    #list_editable = ['doctor_note']
    #list_display_links = ['patient']
    #list_per_page = 10
    #list_max_show_all = 100
    #list_select_related
    inlines = [RecordInline]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):

    list_display = ['user', 'created_at', 'modified_at']
    search_fields = ['user', 'created_at', 'modified_at']
    list_filter = ['user', 'created_at', 'modified_at']
    #fields = ['user', 'created_at', 'modified_at']
    readonly_fields = ['created_at', 'modified_at']
    #list_editable = ['doctor_note']
    #list_display_links = ['patient']
    #list_per_page = 10
    #list_max_show_all = 100
    #list_select_related

    def has_add_permission(self, request: HttpRequest) -> bool:
        return request.user.role == User.ADMIN
    def has_change_permission(self, request, obj=None):
        return request.user.role == User.ADMIN

@admin.register(ReportFile)
class ReportFileAdmin(admin.ModelAdmin):
    list_display = ['id','label']

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    
    inlines = [PatientFileInline]
    list_display = ['id', 'patient', 'doctor',  'doctor_note', 'created_at', 'modified_at']
    search_fields = ['patient', 'doctor', 'created_at', 'modified_at']
    list_filter = ['patient', 'doctor', 'created_at', 'modified_at']
    #fields = ['patient', 'doctor', 'record', 'created_at', 'modified_at']
    
    list_editable = ['doctor_note']
    #list_display_links = ['patient']
    #list_per_page = 10
    #list_max_show_all = 100
    #list_select_related

    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> list[str] | tuple[Any, ...]:
        base = super().get_readonly_fields(request, obj) 
        
        return base + ('created_at', 'modified_at')


    def has_add_permission(self, request: HttpRequest) -> bool:
        return request.user.role == User.ADMIN
    
    actions = ['generate_pdf', 'send_pdf_email']
    def generate_pdf(self, request: HttpRequest, queryset):
        from .export import generate_pdf
        for record in queryset:
            file = generate_pdf(record.id)
            with open(file, 'rb') as f:
                response = HttpResponse(f, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{file}"'
                return response
    generate_pdf.short_description = 'Generate PDF'

    def send_pdf_email(self, request: HttpRequest, queryset):
        from .export import generate_pdf
        from django.core.mail import send_mail, EmailMessage
        for record in queryset:
            file = generate_pdf(record.id)
            mail = EmailMessage(
                subject='Patient Record',
                body='Please find attached the patient record',
                to=[record.patient.user.email],
                from_email=request.user.email,
                )
            mail.attach_file(file)
            mail.send()
    send_pdf_email.short_description = 'Send PDF via Email'
                
                