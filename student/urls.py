from django.urls import path
from . import views
urlpatterns = [
    path('', views.studenthome,name="home"),
    path('teacherhome/', views.teacherhome,name="teacherhomepage"),
    path('teacher/', views.teacherupdate,name="teacher"),
    path('arrange/',views.arrangment,name="arrangment"),
    path('login/',views.loginpage,name="login"),
    path('logout/',views.logoutpage,name="logout"),
    path('asses/<str:pk>/',views.fillmark,name='assesment'),
    path('students/',views.studentslist,name="sts"),
    path('teacherarrange/',views.arrangetea,name="teacherarrange"),
    path('fillmark/',views.teacherpage,name='fillmark'),
    path('assesmentresult/',views.assesmentresult,name='assesmentresult'),
    path('assessmenttpe/',views.assesmenttype,name='assessmenttype'),
    path('accountsetting/',views.registerstud,name='accountsetting'),
    path('teacherarrange/<str:pk>/',views.sectioning,name='reg'),
    path('regcourse/',views.registercourse,name='regcourse'),
    path('departmenthomepage/',views.departmenthomepage,name='departmenthomepage'),
    path('transcript/',views.transcript,name='transcript'),
]
