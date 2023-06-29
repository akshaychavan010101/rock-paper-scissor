from django.shortcuts import render, redirect
from django.http import HttpResponse
import random


def game(request):
    if request.method == 'POST':
        choices = ['rock', 'paper', 'scissors', 'lizard', 'spock']
        user_choice = request.POST.get('choice')
        computer_choice = random.choice(choices)

        # Game Logic
        if user_choice in choices:
            if user_choice == computer_choice:
                result = "It's a draw!"
                score = 'draw'
            elif (
                (user_choice == 'rock' and computer_choice in [
                 'scissors', 'lizard'])
                or (user_choice == 'paper' and computer_choice in ['rock', 'spock'])
                or (user_choice == 'scissors' and computer_choice in ['paper', 'lizard'])
                or (user_choice == 'lizard' and computer_choice in ['paper', 'spock'])
                or (user_choice == 'spock' and computer_choice in ['rock', 'scissors'])
            ):
                result = "You win!"
                score = 'user'
            else:
                result = "Computer wins!"
                score = 'computer'
        else:
            result = "Please select a valid choice."
            score = None

        # Update scores
        user_score = request.session.get('user_score', 0)
        computer_score = request.session.get('computer_score', 0)
        draw_count = request.session.get('draw_count', 0)

        if score == 'user':
            user_score += 1
        elif score == 'computer':
            computer_score += 1
        elif score == 'draw':
            draw_count += 1

        # Store scores in session
        request.session['user_score'] = user_score
        request.session['computer_score'] = computer_score
        request.session['draw_count'] = draw_count

        context = {
            'user_choice': user_choice,
            'computer_choice': computer_choice,
            'result': result,
            'user_score': user_score,
            'computer_score': computer_score,
            'draws': draw_count,
        }

        return render(request, 'game/game.html', context)
    else:
        # Retrieve scores from session or initialize to 0
        user_score = request.session.get('user_score', 0)
        computer_score = request.session.get('computer_score', 0)
        draw_count = request.session.get('draw_count', 0)

        if 'reset' in request.GET:
            # Reset scores
            request.session['user_score'] = 0
            request.session['computer_score'] = 0
            request.session['draw_count'] = 0
            return redirect('game')  # Redirect to avoid resubmitting the form

        context = {
            'user_score': user_score,
            'computer_score': computer_score,
            'draws': draw_count,
        }

        return render(request, 'game/game.html', context)
