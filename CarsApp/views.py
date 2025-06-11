from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Cars
from django.db.models import Count
from django.db.models.functions import TruncDate
import csv
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return HttpResponse("Welcome to the CRUD Application!")

def Create(request):
    if request.method == 'POST':
        name = request.POST.get('Car_Name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        if not all([name, price, quantity]):
            messages.warning(request, 'Please fill in all fields')
            return render(request, 'carsapp/Create.html')

        try:
            price = float(price)
            quantity = int(quantity)
            
            if price <= 0:
                messages.warning(request, 'Price must be greater than 0')
                return render(request, 'carsapp/Create.html')
            
            if quantity < 0:
                messages.warning(request, 'Quantity cannot be negative')
                return render(request, 'carsapp/Create.html')
                
            car = Cars(name=name, price=price, quantity=quantity)
            car.save()
            messages.success(request, f'Car "{name}" has been successfully added to inventory')
            return redirect('Read')
        except ValueError:
            messages.error(request, 'Please enter valid numbers for price and quantity')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'carsapp/Create.html')

def Read(request):
    order_by = request.GET.get('order_by', 'id')
    search_query = request.GET.get('search', '')
    cars = Cars.objects.filter(is_delete=False)
    if search_query:
        cars = cars.filter(name__icontains=search_query)
    cars = cars.order_by(order_by)
    context = {
        'cars': cars,
        'search_query': search_query,
    }
    return render(request, 'carsapp/Read.html', context)

def Update(request, uid):
    car = get_object_or_404(Cars, id=uid)
    if request.method == 'POST':
        name = request.POST.get('Car_Name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        if not all([name, price, quantity]):
            messages.warning(request, 'Please fill in all fields')
            return render(request, 'carsapp/Update.html', {'car': car})

        try:
            price = float(price)
            quantity = int(quantity)
            
            if price <= 0:
                messages.warning(request, 'Price must be greater than 0')
                return render(request, 'carsapp/Update.html', {'car': car})
            
            if quantity < 0:
                messages.warning(request, 'Quantity cannot be negative')
                return render(request, 'carsapp/Update.html', {'car': car})

            car.name = name
            car.price = price
            car.quantity = quantity
            car.save()
            messages.success(request, f'Car "{name}" has been successfully updated')
            return redirect('Read')
        except ValueError:
            messages.error(request, 'Please enter valid numbers for price and quantity')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
        return render(request, 'carsapp/Update.html', {'car': car})
    
    return render(request, 'carsapp/Update.html', {'car': car})

def Delete(request, uid):
    try:
        car = get_object_or_404(Cars, id=uid)
        name = car.name
        car.is_delete = True
        car.save()
        messages.success(request, f'Car "{name}" has been moved to archive')
    except Exception as e:
        messages.error(request, f'Failed to archive car: {str(e)}')
    return redirect('Read')

def Archive(request):
    cars = Cars.objects.filter(is_delete=True).order_by('-update_at')
    context = {
        'cars': cars
    }
    return render(request, 'carsapp/Archive.html', context)

def Retrieve(request, uid):
    try:
        car = get_object_or_404(Cars, id=uid, is_delete=True)
        name = car.name
        car.is_delete = False
        car.save()
        messages.success(request, f'Car "{name}" has been successfully restored to inventory')
    except Exception as e:
        messages.error(request, f'Failed to restore car: {str(e)}')
    return redirect('Read')

def Dashboard(request):
    # Cars over time (by date)
    cars_by_date = (
        Cars.objects.filter(is_delete=False)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(total=Count('id'))
        .order_by('date')
    )
    # Car model counts
    car_model_counts = (
        Cars.objects.filter(is_delete=False)
        .values('name')
        .annotate(total=Count('id'))
        .order_by('name')
    )
    context = {
        'cars_by_date': list(cars_by_date),
        'car_model_counts': list(car_model_counts),
    }
    return render(request, 'carsapp/Dashboard.html', context)

def HardDelete(request, uid):
    car = get_object_or_404(Cars, id=uid, is_delete=True)
    name = car.name
    car.delete()
    messages.success(request, f'Car "{name}" has been permanently deleted.')
    return redirect('Archive')

def ImportCSV(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return render(request, 'carsapp/ImportCSV.html')
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            added, updated = 0, 0
            for row in reader:
                name = row.get('name')
                price = row.get('price')
                quantity = row.get('quantity')
                if not all([name, price, quantity]):
                    continue
                try:
                    price = float(price)
                    quantity = int(quantity)
                except ValueError:
                    continue
                car, created = Cars.objects.update_or_create(
                    name=name,
                    defaults={'price': price, 'quantity': quantity, 'is_delete': False}
                )
                if created:
                    added += 1
                else:
                    updated += 1
            messages.success(request, f'Imported: {added} added, {updated} updated.')
            return redirect('Read')
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
    return render(request, 'carsapp/ImportCSV.html')

def ExportCSV(request):
    """Export all non-archived cars as a CSV file."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="car_inventory.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'name', 'price', 'quantity'])
    for car in Cars.objects.filter(is_delete=False):
        writer.writerow([car.id, car.name, car.price, car.quantity])
    return response

def ExportArchivedCSV(request):
    """Export all archived cars as a CSV file."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="archived_cars.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'name', 'price', 'quantity'])
    for car in Cars.objects.filter(is_delete=True):
        writer.writerow([car.id, car.name, car.price, car.quantity])
    return response