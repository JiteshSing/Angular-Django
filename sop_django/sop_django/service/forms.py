from django import forms
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = "__all__"

class VehicleForm(forms.ModelForm):
    class Meta:
        model = vehicle
        fields = "__all__"

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = "__all__"

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = "__all__"

class PortfoliomanagementForm(forms.ModelForm):
    class Meta:
        model = Portfoliomanagement
        fields = "__all__"

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

# class OwnerForm(forms.ModelForm):
#     class Meta:
#         model = Owner
#         fields = "__all__"

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

class MarketForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = "__all__"
class PurchaseorderForm(forms.ModelForm):
    class Meta:
        model = Purchaseorder
        fields = "__all__"

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = "__all__"

class StaffmemberForm(forms.ModelForm):
    class Meta:
        model = Staffmember
        fields = "__all__"

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

# class IssueForm(forms.ModelForm):
#     class Meta:
#         model = Issue
#         fields = "__all__"

class InitiativeForm(forms.ModelForm):
    class Meta:
        model = Initiative
        fields = "__all__"


class CollegeForm(forms.ModelForm):
    class Meta:
        model = College
        fields = "__all__"


class CourseForm(forms.ModelForm):
    class Meta:
        mdoel = Course
        fields = "__all__"


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = "__all__"


class MarksheetForm(forms.ModelForm):
    class Meta:
        model = Marksheet
        fields = "__all__"


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = "__all__"






