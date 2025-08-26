# app/forms.py
from django import forms
from .models import Project, Task


# YYYYMMDD で表示・入力するための DateInput
class YmdDateInput(forms.DateInput):
    """
    DateField を YYYYMMDD で表示したいときのウィジェット。
    ブラウザの date ピッカーは使わずテキスト入力にする（input_type='text'）。
    """
    input_type = 'text'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("format", "%Y%m%d")
        attrs = kwargs.pop("attrs", {})
        base_attrs = {
            "class": "js-date form-control",
            "placeholder": "YYYYMMDD",
            "autocomplete": "off",
        }
        base_attrs.update(attrs)
        super().__init__(*args, attrs=base_attrs, **kwargs)


def _apply_ymd_format(form, names):
    """
    指定フィールドに YYYYMMDD の表示/入力設定を適用
    """
    for name in names:
        if name in form.fields:
            fld = form.fields[name]
            # 入力は YYYYMMDD と ISO どちらでも受ける
            fld.input_formats = ["%Y%m%d", "%Y-%m-%d"]
            # 表示は YYYYMMDD で統一
            fld.widget = YmdDateInput()


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "project_name",
            "scheduled_start", "scheduled_end",
            "achievement_start", "achievement_end",
            "status",
        ]
        # 初期ウィジェット（念のため）。実際は __init__ で上書きするのでどちらでもOK
        widgets = {
            "scheduled_start": YmdDateInput(),
            "scheduled_end": YmdDateInput(),
            "achievement_start": YmdDateInput(),
            "achievement_end": YmdDateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_ymd_format(self, [
            "scheduled_start", "scheduled_end",
            "achievement_start", "achievement_end",
        ])
        # ※ initial は入れない。更新時に既存値がそのまま表示されるようにする。


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "task_name",
            "scheduled_start", "scheduled_end",
            "achievement_start", "achievement_end",
            "status",
        ]
        widgets = {
            "scheduled_start": YmdDateInput(),
            "scheduled_end": YmdDateInput(),
            "achievement_start": YmdDateInput(),
            "achievement_end": YmdDateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_ymd_format(self, [
            "scheduled_start", "scheduled_end",
            "achievement_start", "achievement_end",
        ])


class TaskUpdateForm(TaskForm):
    # 非モデル項目：Meta.fields に含めない
    shift_following = forms.BooleanField(
        required=False,
        label="このタスク以降を連動シフトする",
    )
