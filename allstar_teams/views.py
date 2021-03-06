from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.core.mail import EmailMessage

from .models import AllstarTeam, Player, Illustrator


class AllstarTeamView(ListView):
    queryset = AllstarTeam.objects.filter(available=True)
    template_name = "allstar_teams_list.html"

    def get_queryset(self):
        self.qs = super(AllstarTeamView, self).get_queryset().filter(available=True)
        return self.qs

    def get_context_data(self):
        context = super(AllstarTeamView, self).get_context_data()
        context['teams'] = self.qs
        return context

def allstar_team_detail(request, id, slug):
    team = get_object_or_404(AllstarTeam, id=id, slug=slug)
    return render(request, 'allstar_team_detail.html', {'team': team})

def allstar_player_detail(request, id, slug):
    player = get_object_or_404(Player, id=id, slug=slug)
    return render(request, 'allstar_player_detail.html', {'player': player})

def send_mail_to_all_illustrators(request):
    if request.method == "POST":
        mail_subject = request.POST.get("subject")
        mail_content = request.POST.get("message")
        mail_content += "<br><br>Instagram: <a href='https://www.instagram.com/across_calcio/'>across_calcio</a>"
        recipients = Illustrator.objects.values_list('mail', flat=True).distinct()
        recipients_str = []
        for r in recipients:
            if r != "":
                recipients_str.append(str(r))
        mail = EmailMessage(mail_subject, mail_content, 'acrosscalcio@gmail.com', recipients_str)
        attachement = request.FILES.get('attachement', False)
        if attachement:
            mail.attach(attachement.name, attachement.read(), attachement.content_type)
        mail.content_subtype = "html"
        mail.send()
        response = redirect("/admin")
    else:
        response = render(request, 'send_mail_to_all_illustrators.html', {})
    return response