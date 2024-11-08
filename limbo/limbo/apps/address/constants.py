from django.utils.translation import gettext_lazy as _

MR, MISS, MRS, MS, DR = ("Mr", "Miss", "Mrs", "Ms", "Dr")
TITLE_CHOICES = (
    (MR, _("Mr")),
    (MISS, _("Miss")),
    (MRS, _("Mrs")),
    (MS, _("Ms")),
    (DR, _("Dr")),
)
