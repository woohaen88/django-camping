from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    title = forms.CharField(
        required=True,
        label="캠핑장이름",
        widget=forms.TextInput(
            attrs={"class": "form-control mt-2", "placeholder": "",}
        ),
    )

    review = forms.CharField(
        required=False,
        label="캠핑장리뷰",
        widget=forms.Textarea(attrs={"class": "form-control mt-2", "placeholder": "",}),
    )

    # category: 드롭다운
    CHOICES = [
        ("Choose...", "Choose..."),
        ("a", "a"),
        ("v", "v"),
        ("c", "c"),
    ]  # (DB, View)
    category = forms.CharField(
        required=True,
        label="카테고리",
        help_text="카테고리 입력",
        widget=forms.Select(
            choices=CHOICES, attrs={"class": "custom-select d-block w-100 mt-2,"},
        ),
    )

    # def save(self, commit=True):
    #     instance = super(PostForm, self).save(commit=False)
    #     if instance.category == "Choose...":
    #         instance.category = "default_value"
    #     # if commit:
    #     instance.save()
    #     return instance

    class Meta:
        model = Post
        fields = (
            "title",
            "review",
            "thumbnail",
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
