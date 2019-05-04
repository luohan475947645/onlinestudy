from startX.serivce.v1 import StartXHandler, get_field_display, StartXModelForm, get_m2m_display
from generic import models
from django.urls import reverse, re_path
from django.utils.safestring import mark_safe


class StudentModelForm(StartXModelForm):
    """编辑操作，分配导师"""

    class Meta:
        model = models.Student
        fields = ['tutor']


class StudentHandler(StartXHandler):
    order_by = ['id']
    model_form_class = StudentModelForm

    def display_consult_record(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '跟进记录'
        record_url = reverse('startX:generic_consultrecord_list', kwargs={'student_id': model.pk})
        return mark_safe('<a target="_blank" href="%s">跟进记录</a>' % record_url)

    def get_add_btn(self, request, *args, **kwargs):
        return None

    def get_list_display(self, request, *args, **kwargs):
        """
        预留的钩子函数
        :return: 为不同权限的用户设置预留的扩展，自定义显示列
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
            value.append(type(self).display_edit)
        return value

    list_display = ['account', 'qq', 'mobile', 'emergency_contract', 'score',
                    get_field_display('状态', 'student_status'),
                    get_m2m_display('已买课程', 'courses'), 'tutor', display_consult_record]
