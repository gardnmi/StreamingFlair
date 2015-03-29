import datetime
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RedditCFB.settings')
from commentfilter.models import Comment

def deletecomments():
	today = datetime.date.today()
	days = datetime.timedelta(days=1)
	sevendaysago = today - days
	print sevendaysago
	Comment.objects.filter(timestamp__lt = sevendaysago).delete()

deletecomments()