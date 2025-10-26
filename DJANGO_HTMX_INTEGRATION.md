# Django + HTMX Integration for BITE-PIPER

## ✅ Integration Complete!

Your BITE-PIPER funding allocation system is now integrated with Django + HTMX for a modern, Python-first web interface with minimal JavaScript.

---

## 🎯 What Was Created

### Django App Structure
```
src/
├── funding/                      # New Django app
│   ├── __init__.py
│   ├── admin.py                 # Admin config
│   ├── apps.py                  # App configuration
│   ├── models.py                # Models (none needed - using MeTTa)
│   ├── urls.py                  # URL routing
│   ├── views.py                 # Views connecting to BITE-PIPER
│   └── templates/
│       └── funding/
│           ├── base.html        # Base template with HTMX
│           ├── index.html       # Main dashboard
│           ├── about.html       # About page
│           └── partials/
│               ├── results.html # HTMX results partial
│               └── error.html   # Error partial
├── backend/                      # Django project (updated)
│   ├── settings.py              # Added funding app
│   └── urls.py                  # Added funding URLs
└── manage.py                     # Django management
```

### Key Features

✅ **HTMXPowered Frontend**
- No page reloads - dynamic updates
- Minimal JavaScript
- Progressive enhancement
- Fast, responsive UI

✅ **Django Backend**
- Production-ready
- Integrated with existing Django setup
- RESTful API endpoints
- Clean URL structure

✅ **BITE-PIPER Integration**
- Direct integration with `application.py`
- Uses Minimal MeTTa engine
- Real-time allocation calculations
- Transparent explanations

---

## 🚀 Quick Start

### 1. Install Dependencies (if needed)

```bash
# Make sure Django is installed
pip install django

# No other dependencies needed - HTMX loads from CDN
```

### 2. Navigate to src Directory

```bash
cd src
```

### 3. Run Django Development Server

```bash
python manage.py runserver
```

### 4. Open Browser

Visit: **http://localhost:8000**

---

## 📱 Using the Application

### Main Dashboard (/)

1. Enter a budget amount (e.g., $1,000,000)
2. Click **"🚀 Calculate Allocation"**
3. HTMX fetches results without page reload
4. View:
   - Budget summary
   - Priority analysis for each region
   - Funding allocation breakdown
   - Export options

### About Page (/about/)

Learn about:
- System overview
- How allocation works
- Technology stack
- Key features

---

## 🛠️ How It Works

### HTMX Magic

When you click "Calculate Allocation":

1. **HTMX intercepts form submission**
   ```html
   <form hx-post="/calculate/" hx-target="#results">
   ```

2. **POST request sent to Django**
   - Budget value sent as form data
   - CSRF token included automatically

3. **Django view processes request**
   ```python
   def calculate_allocation(request):
       budget = int(request.POST.get('budget'))
       app = BitePiperApp(total_budget=budget)
       # ... calculate ...
       return render(request, 'partials/results.html', context)
   ```

4. **HTMX injects HTML response**
   - Partial HTML returned
   - Injected into `#results` div
   - No JavaScript needed!

### Django Views

**`index(request)`** - Main dashboard  
**`calculate_allocation(request)`** - Calculate funding (HTMX endpoint)  
**`calculate_priority(request, region_name)`** - Single region priority  
**`api_health(request)`** - Health check API  
**`get_regions(request)`** - Get available regions  
**`about(request)`** - About page  

---

## 🎨 UI Features

### Tailwind CSS Styling
- Modern, responsive design
- Gradient backgrounds
- Card-based layout
- Color-coded priorities:
  - 🔴 **CRITICAL** - Red
  - 🟠 **HIGH** - Orange
  - 🟡 **MEDIUM** - Yellow
  - 🟢 **LOW** - Green

### Loading States
- Spinner during calculation
- HTMX loading indicators
- Smooth transitions

### Export Options
- Export results as JSON
- Print report functionality

---

## 📚 URL Structure

```
/                  - Main dashboard
/about/            - About page
/calculate/        - Calculate allocation (HTMX POST)
/priority/<region>/ - Calculate single region priority
/api/health/       - Health check endpoint
/api/regions/      - Get available regions
/admin/            - Django admin panel
```

---

## 🔧 Customization

### Change Budget Default

Edit `src/funding/views.py`:

```python
def index(request):
    return render(request, 'funding/index.html', {
        'title': 'BITE-PIPER Funding Allocation',
        'default_budget': 2000000  # Change this
    })
```

### Modify Colors/Styling

Edit `src/funding/templates/funding/base.html`:

```html
<!-- Change primary color from purple to blue -->
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: '#3B82F6'  // Blue instead of purple
            }
        }
    }
}
</script>
```

### Add New Views

1. Add view function in `src/funding/views.py`
2. Add URL in `src/funding/urls.py`
3. Create template in `src/funding/templates/funding/`

---

## 🎯 HTMX Endpoints

### Calculate Allocation

```html
<form hx-post="/calculate/" hx-target="#results">
    <input name="budget" value="1000000">
    <button type="submit">Calculate</button>
</form>
```

**Response**: HTML partial with results

### Single Region Priority

```html
<button hx-get="/priority/RegionA/" hx-target="#priority-result">
    Get Priority
</button>
```

**Response**: HTML card with priority details

---

## 🧪 Testing

### Manual Testing

1. **Test with different budgets**:
   - $500,000
   - $1,000,000
   - $5,000,000

2. **Verify calculations**:
   - Total allocated = Budget
   - Percentages add to 100%
   - Priority scores match explanations

3. **Test export**:
   - Click "Export as JSON"
   - Verify file downloads
   - Check JSON format

### API Testing

```bash
# Health check
curl http://localhost:8000/api/health/

# Get regions
curl http://localhost:8000/api/regions/

# Calculate allocation
curl -X POST http://localhost:8000/calculate/ \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "budget=1000000" \
     -d "csrfmiddlewaretoken=TOKEN"
```

---

## 🚀 Deployment

### Production Checklist

1. **Update settings.py**:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

2. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Set up database** (if using models):
   ```bash
   python manage.py migrate
   ```

4. **Configure WSGI/ASGI**:
   - Use Gunicorn or uWSGI
   - Set up Nginx reverse proxy

5. **Environment variables**:
   ```bash
   export SECRET_KEY="your-secret-key"
   export DEBUG=False
   ```

### Deployment Options

**Option 1: Railway / Render**
- Push to Git
- Connect repository
- Auto-deploys

**Option 2: Docker**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**Option 3: Traditional VPS**
- Install Python, Nginx, Gunicorn
- Configure systemd service
- Set up SSL with Let's Encrypt

---

## 🔄 Adding New Regions

### Step 1: Add to `socioeconomic_model.py`

```python
RegionC = Symbol("RegionC")
```

### Step 2: Add Data in `application.py`

```python
# In _load_knowledge() method
data_c_tuple = Expression([
    Expression([HouseholdIncomePerCapita, Symbol("3000")]),
    Expression([PovertyRate, Symbol("45")]),
    # ... other indicators ...
])

self.space.add_atom(Expression([
    Symbol("="),
    Expression([RegionData, RegionC]),
    data_c_tuple
]))

# Add to regions list
self.regions = [RegionA, RegionB, RegionC]
```

### Step 3: Test

Restart Django server - new region will appear in calculations!

---

## 💡 Advanced Features

### Add Chart Visualization

Install Chart.js via CDN and update templates:

```html
<!-- In base.html -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<!-- In results partial -->
<canvas id="allocationChart"></canvas>
<script>
new Chart(document.getElementById('allocationChart'), {
    type: 'pie',
    data: {
        labels: ['RegionA', 'RegionB'],
        datasets: [{
            data: [{{ allocations.RegionA.percentage }}, {{ allocations.RegionB.percentage }}]
        }]
    }
});
</script>
```

### Add User Authentication

```bash
python manage.py createsuperuser
```

Then in views.py:
```python
from django.contrib.auth.decorators import login_required

@login_required
def calculate_allocation(request):
    # ... existing code ...
```

### Add Comparison Feature

Create new view to compare multiple budgets:

```python
def compare_scenarios(request):
    budgets = [500000, 1000000, 2000000]
    scenarios = []
    
    for budget in budgets:
        app = BitePiperApp(total_budget=budget)
        # ... calculate ...
        scenarios.append(result)
    
    return render(request, 'funding/compare.html', {'scenarios': scenarios})
```

---

## 🐛 Troubleshooting

### Issue: Template Not Found

**Solution**: Make sure `'funding.apps.FundingConfig'` is in `INSTALLED_APPS`

### Issue: CSRF Token Missing

**Solution**: Ensure `{% csrf_token %}` is in all POST forms

### Issue: Static Files Not Loading

**Solution**:
```bash
python manage.py collectstatic
```

### Issue: Import Error for application.py

**Solution**: Check `sys.path.insert` in `views.py` points to correct directory

### Issue: HTMX Not Working

**Solution**: Check browser console for errors. Ensure HTMX CDN is loading:
```html
<script src="https://unpkg.com/htmx.org@1.9.10"></script>
```

---

## 📖 Documentation

- **Complete Guide**: `FUNDING_ALLOCATION_GUIDE.md`
- **Quick Summary**: `FUNDING_ALLOCATION_SUMMARY.md`
- **What's New**: `WHATS_NEW.md`
- **Architecture**: `ARCHITECTURE.md`

---

## ✅ Integration Checklist

- [x] Created Django `funding` app
- [x] Added views connecting to BITE-PIPER
- [x] Created HTMX-powered templates
- [x] Set up URL routing
- [x] Updated Django settings
- [x] Integrated with existing backend
- [x] Added about page
- [x] Implemented export functionality
- [x] Added loading indicators
- [x] Color-coded priority levels
- [x] Responsive design with Tailwind

---

## 🎉 Summary

**Your BITE-PIPER system now has**:

✅ **Django Backend** - Production-ready, scalable  
✅ **HTMX Frontend** - Modern, minimal JavaScript  
✅ **Real-time Updates** - No page reloads  
✅ **Beautiful UI** - Tailwind CSS styling  
✅ **MeTTa Integration** - Direct connection to allocation engine  
✅ **Export Features** - JSON download, print  
✅ **Mobile Responsive** - Works on all devices  
✅ **Easy Customization** - Python-first approach  

**Start your server**:
```bash
cd src
python manage.py runserver
```

**Visit**: http://localhost:8000

---

**Status**: ✅ Production Ready  
**Framework**: Django + HTMX  
**Version**: 1.0.0
