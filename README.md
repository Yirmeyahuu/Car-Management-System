# Django Cars Inventory CRUD 🚗

A Django web application for managing a car inventory with full CRUD (Create, Read, Update, Delete) functionality, CSV import, and search features.

## 🚦 How the System Works

This application provides a complete workflow for managing a car inventory. Here’s an overview of its main functions and how users typically interact with the system:

### 🛠️ Main Functions
- ➕ **Add Car**: Create new car records with name, price, and quantity.
- 📋 **View Inventory**: List all cars in the inventory, with options to search and filter by name.
- ✏️ **Update Car**: Edit details of existing cars.
- 🗑️ **Delete/Archive Car**: Remove cars from the active inventory (archived cars can be restored).
- ♻️ **Restore Car**: Bring back previously archived cars to the active inventory.
- 📥 **Import CSV**: Bulk add or update cars by uploading a CSV file. Existing cars (matched by name) are updated; new ones are added.
- 🔍 **Search**: Quickly find cars by typing part or all of the car name in the search bar.

### 📝 Typical User Steps
1. 🏠 **Access the Inventory**: Go to the main inventory page to see all cars.
2. ➕ **Add a Car**: Click the “Add Car” button and fill in the form.
3. ✏️/🗑️ **Edit or Delete**: Use the action buttons next to each car to update or archive them.
4. ♻️ **Restore Archived Cars**: Visit the archive page to restore any deleted cars.
5. 📥 **Import Data**: Use the “Import CSV” feature to upload a list of cars for bulk management.
6. 🔍 **Search**: Use the search bar to filter cars by name instantly.

All actions are performed through a responsive Bootstrap UI, making the system easy to use on both desktop and mobile devices.

## ✨ Features
- ➕ Add, view, update, and delete car records
- ♻️ Archive and restore deleted cars
- 📥 Import cars from a CSV file (add new or update existing by name)
- 🔍 Search car models by name
- 📱 Responsive Bootstrap UI

## ⚙️ Requirements
- 🐍 Python 3.8+
- 🌐 Django 4.x or 5.x
- 🛢️ MySQL (or compatible database)

## 🚀 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Yirmeyahuu/Car-Management-System.git
   cd django-crud
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv virt
   source virt/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Create `requirements.txt` with Django and mysqlclient if not present)*

4. **Configure the database:**
   - Edit `CrudProject/settings.py` to set your database credentials.

5. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the app:**
   Open [http://127.0.0.1:8000/read/](http://127.0.0.1:8000/read/) in your browser.

## 📥 CSV Import
- Go to the inventory page and click "Import CSV".
- Upload a CSV file with columns: `name`, `price`, `quantity`.
- Existing cars (by name) will be updated; new ones will be added.

### 🗂️ Sample CSV
```
name,price,quantity
Toyota Camry,25000.00,10
Honda Civic,22000.00,15
Ford Mustang,35000.00,5
Tesla Model 3,40000.00,8
Nissan Altima,21000.00,12
```

## 🔍 Search
- Use the search bar at the top of the inventory page to filter car models by name.

## 📝 License
MIT

---
*Created June 2025* 🚗
