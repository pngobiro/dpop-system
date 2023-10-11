# views.py
from django_unicorn.components import UnicornView
from apps.statistics.models import DcrtData
from django_pandas.io import read_frame
from django.utils.html import format_html

class CaseSummaryView(UnicornView):
    selected_column = None
    queryset = None
    columns = None 
    summary = {}
    shape = None
    df = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = DcrtData.objects.all()
        if self.queryset:
            df = read_frame(self.queryset)
            self.columns = df.columns.tolist()
            self.shape = df.shape

    def changeColumn(self):
        if self.selected_column and self.queryset:
            df = read_frame(self.queryset)
            self.summary = df[self.selected_column].describe().to_dict()
            self.shape = df.shape
            
