from csv import reader as csv_reader
from io import StringIO
from pathlib import Path

from django import template
from django.contrib.staticfiles.storage import staticfiles_storage

register = template.Library()


@register.simple_tag
def csv_table(csv_file):
    with Path(staticfiles_storage.path(csv_file)).open() as f:
        r = csv_reader(f)
        builder = StringIO()
        builder.write("\n")
        headers = next(r)
        builder.write("|")
        for h in headers:
            builder.write(h)
            builder.write("|")
        builder.write("\n")
        builder.write("|")
        for h in headers:
            builder.write("---|")
        builder.write("\n")

        for row in r:
            builder.write("|")
            for cell in row:
                builder.write(cell)
                builder.write("|")
            builder.write("\n")

        return builder.getvalue()
