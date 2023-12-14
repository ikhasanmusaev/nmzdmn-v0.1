from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from poll.models import Answers


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
def questions_view(request):
    questions = []

    with open('questions.txt') as file:
        questions_file = file.readlines()
        for q in questions_file:
            question = q.split('.')[1]
            question, answer = question.split('|')
            questions.append({
                'n': q.split('.')[0],
                'q': question.strip(),
                'a': answer.strip()
            })

    if request.method == "POST":
        counter = {
            'R_count': 0,
            'I_count': 0,
            'A_count': 0,
            'S_count': 0,
            'E_count': 0,
            'C_count': 0,
        }
        # print(request.POST)
        data = list(request.POST)
        name = request.POST.get('name')
        data.remove('name')

        for i in data:
            counter[i.split('-')[1] + '_count'] += 1

        print(counter)
        Answers.objects.create(
            user_name=name,
            ip_address=get_client_ip(request),
            **counter
        )
        sorted_result = [x[0] for x in dict(sorted(counter.items(), key=lambda item: item[1], reverse=True)[:3]).keys()]

        print(sorted_result)
        result1 = open(sorted_result[0] + '.txt', 'r').read()
        result2 = open(sorted_result[1] + '.txt', 'r').read()
        result3 = open(sorted_result[2] + '.txt', 'r').read()

        return render(request, "result.html", {'result1': result1, 'result2': result2, 'result3': result3})

    context = {
        "questions": questions,
    }

    return render(request, "base.html", context)
