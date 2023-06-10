import csv
from io import TextIOBase
import sys


def gen_youtube_channels_table(out: TextIOBase):
    out.write(
        """\
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>     
"""
    )

    with open("../content/static/files/youtube_channels.csv") as f:
        for row in csv.DictReader(f):
            out.write(
                f"""\
        <tr>
            <td><a href="{row["url"]}">{row["title"]}</a></td>
            <td>{row["description"]}</td>
        </tr>
"""
            )

    out.write(
        """\
    </tbody>
</table>        
"""
    )


targets = {"youtube_channels_table.html": gen_youtube_channels_table}


if __name__ == "__main__":
    target = sys.argv[1]
    target_gen = targets[target]
    with open(target, "w") as f:
        target_gen(f)
