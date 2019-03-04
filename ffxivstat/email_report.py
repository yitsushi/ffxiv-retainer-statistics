from contextlib import redirect_stdout
from io import StringIO
from .report import run as simple_report
from ffxivstat.lib import MailGun

def run():
    text = StringIO()
    with redirect_stdout(text):
        simple_report()

    html = f'''
<html>
<body>
<pre>
{text.getvalue()}
</pre>
</body>
</html>'''
    MailGun().send(text, html)
