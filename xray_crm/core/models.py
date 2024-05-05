from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

from django.contrib.auth.hashers import make_password


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=50)
    username = models.CharField(unique=True, max_length=20)
    ssn = models.CharField(max_length=20, null=True, blank=True)
    note = models.TextField(max_length=200, null=True, blank=True)

    # ROLES
    ADMIN = 1
    DOCTOR = 2
    PATIENT = 3
    ROLE_CHOICES = (
        (ADMIN, "Admin"),
        (DOCTOR, 'Doctor'),
        (PATIENT, 'Patient'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f'{self.pk} - {self.first_name} {self.last_name}'

class Patient(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #profile_image = models.ImageField(upload_to='', default='')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.__str__()
    
    
class Doctor(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='', default='')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.__str__()

class Record(models.Model):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == User.DOCTOR:
            return qs.filter(user=request.user)
        elif request.user.role == User.PATIENT:
            return qs.filter(user=request.user)
        return qs
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    doctor_note = models.TextField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.patient.__str__()}'
    
    def __meta__(self):
        #permission
        return {
            'permissions': [
                ('view_record', 'Can view record'),
                ('change_record', 'Can change record'),
                ('delete_record', 'Can delete record'),
                ('add_record', 'Can add record'),
            ]
        }
        
class PatientFile(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    file = models.FileField(upload_to='patient_files/')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    record = models.ForeignKey(Record, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.file.name
    
class ReportFile(models.Model):
    patient_file = models.ForeignKey(PatientFile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    BROKEN = 1
    NOT_BROKEN = 2
    LABEL_CHOICES = (
        (BROKEN, 'Broken'),
        (NOT_BROKEN, 'Not Broken'),
    )
    label = models.PositiveSmallIntegerField(choices=LABEL_CHOICES, blank=True, null=True)
    #zone = models.CharField(max_length=20, null=True, blank=True)
    member = models.CharField(max_length=20, null=True, blank=True)
    hardware = models.BooleanField(default=False)
    number = models.PositiveSmallIntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return str(self.id)
    
    
############################################################################################################

# SIGNALS

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    
    if created:
        
        if instance.role == 3:
            Patient.objects.create(user=instance)
            instance.password = make_password(instance.password)
            instance.save()
            print('Patient is created')
        elif instance.role == 2:
            Doctor.objects.create(user=instance)
            instance.is_staff = True
            instance.password = make_password(instance.password)
            instance.save()
            print('Doctor is created')    
    else:
        try:
            if instance.role == 3:
                Patient.objects.get(user=instance)
            elif instance.role == 2:
                Doctor.objects.get(user=instance)
        except Patient.DoesNotExist:
            Patient.objects.create(user=instance)
            print('Patient is created')
        except Doctor.DoesNotExist:
            Doctor.objects.create(user=instance)
            print('Doctor is created')

@receiver(post_save, sender=PatientFile)
def post_save_patient_file(sender, instance, created, **kwargs):
    
    if created:
        filename = instance.file.path
        from xray_crm.valid import predict_image, number_fractures
        label = predict_image(filename)
        
        if label == ReportFile.BROKEN:
            number = number_fractures(filename)
        else:
            number = 0

        ReportFile.objects.create(
            patient_file = instance,
            label = label,
            member = "unknown",
            hardware = False,
            number = number
        )

@receiver(post_save, sender=ReportFile)
def post_save_report_file(sender, instance, created, **kwargs):
    if not created:
        label = instance.label
        print(f"Image {instance.id} is {label}, added in the training set.")
        # at the next training, this image will be added to the training set
    
