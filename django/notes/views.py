from django.shortcuts import render
from .models import Topic

def index(request):
  """Home page for Note"""
  return render(request, 'notes/index.html')

def topics(request):
  """Show all topics"""
  topics = Topic.objects.order_by('date_added')
  context = {'topics':topics}
  return render(request, 'notes/topics.html', context)

def topic(request, topic_id):
  """Show one topic and all articles for it"""
  topic = Topic.objects.get(id=topic_id)
  entries = topic.entry_set.order_by('-date_added')
  context = {'topic':topic, 'entries':entries}
  return render(request, 'notes/topic.html', context)
