# env/usr/bin python
# encoding:utf8

'''
@Author: Jinsong Shi
@Date: 2020-07-25 11:35:21
@LastEditors: Jinsong Shi
@LastEditTime: 2020-07-26 14:07:13
@Description: 
'''

from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    """客户信息表"""
    name = models.CharField(max_length = 32, blank = True, null = True)
    qq = models.CharField(max_length  = 64, unique = True)
    qq_name = models.CharField(max_length = 64, blank = True, null = True)
    phone = models.CharField(max_length = 64, blank = True, null = True)
    source_choices = (
        (0, "转介绍"),
        (1, "QQ群"),
        (2, "官网"),
        (3, "51CTO"),
        (4, "百度推广"),
        (5, "知乎"),
        (6, "市场推广")
    )
    source = models.SmallIntegerField(choices = source_choices)
    referral_from = models.CharField(verbose_name = "转介绍人qq", max_length = 64, blank = True, null = True)
    consult_course = models.ForeignKey("Course", on_delete=models.CASCADE,  verbose_name = "咨询课程")
    consult_content = models.TextField(verbose_name = "咨询详情")
    consultent = models.ForeignKey("UserProfile", on_delete=models.CASCADE,)
    tags = models.ManyToManyField("Tag", blank = True, null = True)
    memo = models.TextField(blank = True, null = True)
    date = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.qq


class Tag(models.Model):
    name = models.CharField(max_length = 32, unique = True)

    def __str__(self):
        return self.name



class CustomerFollowUp(models.Model):
    """客户跟进表"""
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    content = models.TextField(verbose_name = "跟进内容")
    consultent = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    intention_choices = (
        (0, "2周内报名"),
        (1, "1个月内报名"),
        (2, "近期无报名计划"),
        (3, "已在其他机构报名"),
        (4, "已报名"),
        (5, "已拉黑")
    )
    intention = models.SmallIntegerField(choices = intention_choices)
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "<%s : %s>" %(self.customer.qq, self.intention)


class UserProfile(models.Model):
    """账号表"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 32)
    roles = models.ManyToManyField("Role")

    def __str__(self):
        return self.name
    



class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length = 32, unique = True)
    
    def __str__(self):
        return self.name


class Branch(models.Model):
    """校区表"""
    name = models.CharField(max_length = 128, unique = True, verbose_name = "分校")
    addr = models.CharField(max_length = 128)
    
    def __str__(self):
        return self.name



class ClassList(models.Model):
    """班级表"""
    course = models.ForeignKey("Course", on_delete=models.CASCADE,)
    branch = models.ForeignKey("Branch", on_delete=models.CASCADE,)
    classType_choices = (
        (0, "面授(脱产)"),
        (1, "面授(周末)"),
        (2, "网络班"),
    )
    classType = models.SmallIntegerField(choices = classType_choices, verbose_name = "班级类型")
    semester = models.PositiveSmallIntegerField(verbose_name = "学期")
    teachers = models.ManyToManyField("UserProfile")
    startDate = models.DateField(verbose_name = "开班日期")
    finishDate = models.DateField(verbose_name = "结业日期", )

    def __str__(self):
        return self.course

    class Meta:
        unique_together = ("branch", "course", "semester")

class CourseRecord(models.Model):
    """上课记录"""
    from_class = models.ForeignKey("ClassList", on_delete=models.CASCADE, verbose_name = "班级")
    day_num = models.PositiveSmallIntegerField(verbose_name = "第几节（天）")
    teacher = models.ForeignKey("UserProfile", on_delete=models.CASCADE,)
    has_homework = models.BooleanField(default = True)
    homework_title = models.CharField(max_length = 128, blank = True, null = True)
    homework_content = models.TextField(blank=True, null=True)
    outline = models.TextField(verbose_name="本节课大纲")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.from_class, self.day_num)
    
    class Meta:
        unique_together = ("from_class", "day_num")

class Enrollment(models.Model):
    """报名表"""
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE,)
    enrolled_class = models.ForeignKey("ClassList", on_delete=models.CASCADE, verbose_name = "所报班级")
    sonsultant = models.ForeignKey("UserProfile", on_delete=models.CASCADE, verbose_name = "课程顾问")
    contact_agreed = models.BooleanField(default = False, verbose_name = "学员已同意条款")
    contact_approved = models.BooleanField(default = False, verbose_name = "合同已审核")
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "%s %s" %(self.customer, self.enrolled_class)
    
    class Meta:
        unique_together = ("customer", "enrolled_class")



class Course(models.Model):
    """课程表"""
    course = models.CharField(max_length = 64, unique = True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name = "周期(月)")
    outline = models.TextField()

    def __str__(self):
        return self.course

class StudyRecord(models.Model):
    """学习记录表"""
    student = models.ForeignKey("Enrollment", on_delete=models.CASCADE,)
    courese_record = models.ForeignKey("CourseRecord", on_delete=models.CASCADE,)
    attendance_choices = (
        (0, "已签到"),
        (1, "迟到"),
        (2, "缺勤"),
        (3, "早退"),
    )
    attendance = models.SmallIntegerField(choices=attendance_choices, default=0, verbose_name="出勤状况")
    score_choices = (
        (100, "A+"),
        (90, "A+"),
        (85, "B+"),
        (80, "B"),
        (75, "B-"),
        (70, "C+"),
        (60, "C"),
        (40, "C-"),
        (-50, "D"),
        (-100, "COPY"),
        (0, "N/A"),
    )
    score = models.SmallIntegerField(choices= score_choices, verbose_name = "分数情况")
    memo = models.TextField(blank = True, null = True, verbose_name= "备注")
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "%s %s %s" %(self.student, self.courese_record, self.score)

class Payment(models.Model):
    """缴费记录表"""
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE,)
    amount = models.PositiveIntegerField(default = 500, verbose_name = "数额")
    consultant = models.ForeignKey("UserProfile", on_delete=models.CASCADE,)
    course = models.ForeignKey("Course", on_delete=models.CASCADE, verbose_name = "所报课程")
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "%s %s" %(self.customer, self.amount)

class Menu(models.Model):
    """菜单表"""
    name = models.CharField(max_length = 32)
    url_name = models.CharField(max_length  = 64)

    def __str__(self):
        return self.name
