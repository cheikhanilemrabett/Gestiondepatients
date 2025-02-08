from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Doctor, Department,Patient
from django.contrib.auth.models import User



class DoctorForm(forms.ModelForm):
    # تخصيص حقل 'department' لعرض قائمة من الأقسام
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        empty_label="اختر القسم"
    )

    class Meta:
        model = Doctor
        fields = ['Name', 'department', 'address', 'age']  # تأكد من الحقول المطلوبة

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # إضافة التنسيقات للحقل (إن لزم الأمر)
        self.fields['Name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['age'].widget.attrs.update({'class': 'form-control'})


####3
class PatientSignUpForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        help_text=None,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width: 90%; font-size: 14px; margin-bottom: 10px;'  # عرض أصغر وخط أصغر مع مسافة سفلية
        })
    )
    password = forms.CharField(
        required=True,
        label="Password",
        help_text=None,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'width: 90%; font-size: 14px; margin-bottom: 10px;'  # عرض أصغر وخط أصغر مع مسافة سفلية
        })
    )
    confirmpassword = forms.CharField(
        required=True,
        label="Confirm Password",
        help_text=None,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'width: 90%; font-size: 14px; margin-bottom: 10px;'  # عرض أصغر وخط أصغر مع مسافة سفلية
        })
    )
    email = forms.EmailField(
       required=True,
        help_text=None,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'style': 'width: 90%; font-size: 14px;'  # عرض أصغر وخط أصغر
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']  # الحقول المطلوبة فقط

    def clean(self):
        """
        التحقق من تطابق كلمات المرور.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmpassword = cleaned_data.get("confirmpassword")

        if password != confirmpassword:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data




class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['Name', 'address', 'age', 'phone', 'diseases_case', 'gender']