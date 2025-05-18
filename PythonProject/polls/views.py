from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Option, Vote
from .forms import VoteForm
from django.db.models import Count

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    if request.method == 'POST':
        form = VoteForm(request.POST, poll=poll)

        if form.is_valid():
            email = form.cleaned_data.get('email', None)

            if poll.voting_security_email and email:
                existing_votes = Vote.objects.filter(poll=poll, email=email).count()
                if existing_votes >= poll.user_limit:
                    error = f"You have reached the vote limit for this poll ({poll.user_limit} vote(s))."
                    return render(request, 'polls/poll_detail.html', {
                        'poll': poll,
                        'form': form,
                        'error_message': error
                    })

            vote = form.save(commit=False)
            vote.poll = poll
            vote.save()
            return redirect('poll_result', poll_id=poll.id)

    else:
        form = VoteForm(poll=poll)

    return render(request, 'polls/poll_detail.html', {
        'poll': poll,
        'form': form
    })


def poll_result(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    options = poll.options.all()

    total_votes = sum(option.vote_set.count() for option in options) or 1

    for option in options:
        option.vote_count = option.vote_set.count()
        option.percentage = round(option.vote_count / total_votes * 100, 2)

    return render(request, 'polls/poll_result.html', {'poll': poll, 'options': options})


def poll_list(request):
    polls = Poll.objects.all()
    return render(request, 'polls/poll_list.html', {'polls': polls})
