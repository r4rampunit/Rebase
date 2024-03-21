from django.shortcuts import render
from django.http import JsonResponse

def chart(request):
    if request.method == "GET":
        # Initialize dropdown options (replace with actual data)
        dropdown_options = {
            'variable': ['Variable1', 'Variable2', 'Variable3'],
            'dataset': ['Dataset1', 'Dataset2', 'Dataset3'],
            'country': ['Country1', 'Country2', 'Country3'],
            'model': ['Model1', 'Model2', 'Model3']
        }
        return render(request, 'chart.html', {'dropdown_options': dropdown_options})
    elif request.method == "POST":
        # Process AJAX request and return updated chart data
        variable = request.POST.get('variable')
        dataset = request.POST.get('dataset')
        country = request.POST.get('country')
        model = request.POST.get('model')

        # Example: Generate random data for demonstration purposes
        data = [random.randint(1, 100) for _ in range(10)]
        labels = [str(2020 + i) for i in range(10)]

        return JsonResponse({'data': data, 'labels': labels})
