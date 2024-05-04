from ninja import NinjaAPI
from ninja.security import django_auth
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from ninja import ModelSchema
from core.models import *

#api = NinjaExtraAPI(auth=django_auth)
api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

class DoctorSchema(ModelSchema):
    class Meta:
        model = Doctor
        fields = "__all__"

class PatientSchema(ModelSchema):
    
    class Meta:
        model = Patient
        fields = "__all__"

class ReportSchema(ModelSchema):
    class Meta:
        model = ReportFile
        exclude = ["patient_file"]

class PatientFileSchema(ModelSchema):
    report_files : list[ReportSchema]
    class Meta:
        model = PatientFile
        exclude = ["record", "patient"]

class RecordSchema(ModelSchema):
    patient : PatientSchema
    doctor : DoctorSchema
    patient_files : list[PatientFileSchema]
    class Meta:
        model = Record
        fields = "__all__"






@api.get("/hello")
def hello(request):
    return {"message": "Hello, world!"}

@api.get("/history")
def history(request):
    return {"message": "Hello, history!"}

