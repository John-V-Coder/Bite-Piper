"""
Django views for BITE-PIPER Funding Allocation with HTMX
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from application import BitePiperApp
from advanced_scoring import calculate_advanced_priority_score, explain_priority_decision
from .agent_client import get_agent_client


def home(request):
    """The main home page with shortcuts."""
    return render(request, 'funding/home.html', {
        'title': 'Welcome to BITE-PIPER'
    })


def index(request):
    """Main dashboard view"""
    return render(request, 'funding/index.html', {
        'title': 'BITE-PIPER Funding Allocation',
        'default_budget': 1000000,
        'use_advanced_scoring': True  # Enable advanced logical scoring
    })


@require_http_methods(["POST"])
def calculate_allocation(request):
    """
    Calculate funding allocation based on budget (HTMX endpoint)
    Returns HTML partial for HTMX to inject
    """
    try:
        # Get budget from POST data
        budget = int(request.POST.get('budget', 1000000))
        
        if budget <= 0:
            return render(request, 'funding/partials/error.html', {
                'error_message': 'Budget must be a positive number'
            })
        
        # Create BitePiperApp and calculate
        app = BitePiperApp(total_budget=budget)
        
        # Check if advanced scoring is requested
        use_advanced = request.POST.get('use_advanced', 'true').lower() == 'true'
        
        # Calculate priorities for all regions
        region_priorities = []
        for region in app.regions:
            if use_advanced:
                # Use advanced scoring with sophisticated logic
                priority_data = app.calculate_priority_score(region)
                
                # Extract indicators for advanced analysis
                indicators = priority_data.get('indicators', {})
                if indicators:
                    # Apply advanced scoring logic
                    advanced_result = calculate_advanced_priority_score(indicators)
                    
                    # Merge advanced results with basic data
                    priority_data['score'] = advanced_result['display_score']
                    priority_data['priority'] = advanced_result['priority_level']
                    priority_data['explanation'] = advanced_result['explanation']
                    priority_data['indicator_breakdown'] = advanced_result['indicator_breakdown']
                    priority_data['warnings'] = advanced_result.get('warnings', [])
                    priority_data['urgency'] = advanced_result['urgency']
                    priority_data['methodology'] = 'Advanced Multi-Indicator Assessment'
            else:
                # Use basic scoring
                priority_data = app.calculate_priority_score(region)
            
            region_priorities.append(priority_data)
        
        # Allocate funding
        allocations = app.allocate_funding(region_priorities)
        
        # Calculate totals
        total_allocated = sum(details['amount'] for details in allocations.values())
        budget_utilization = (total_allocated / budget) * 100
        
        # Prepare context for editable template
        context = {
            'budget': budget,
            'total_allocated': total_allocated,
            'budget_utilization': budget_utilization,
            'priorities': region_priorities,
            'allocations': allocations,
            'regions_analyzed': len(region_priorities),
            'is_custom': False
        }
        
        return render(request, 'funding/partials/editable_results.html', context)
    
    except Exception as e:
        return render(request, 'funding/partials/error.html', {
            'error_message': f'Error calculating allocation: {str(e)}'
        })


@require_http_methods(["POST"])
def recalculate_custom(request):
    """
    Recalculate allocation with custom priority scores (HTMX endpoint)
    Allows users to manually adjust scores
    """
    try:
        # Get budget
        budget = float(request.POST.get('budget', 1000000))
        
        if budget <= 0:
            return render(request, 'funding/partials/error.html', {
                'error_message': 'Budget must be a positive number'
            })
        
        # Create app to get region list
        app = BitePiperApp(total_budget=budget)
        
        # Collect custom scores from form
        custom_priorities = []
        for region in app.regions:
            region_name = str(region)
            score_key = f'score_{region_name}'
            
            # Get custom score from form
            custom_score = float(request.POST.get(score_key, 0.0))
            
            # Validate score range
            if custom_score < 0.0 or custom_score > 1.0:
                return render(request, 'funding/partials/error.html', {
                    'error_message': f'Score for {region_name} must be between 0.0 and 1.0'
                })
            
            # Determine priority level based on custom score
            if custom_score >= 0.70:
                priority = 'CRITICAL'
            elif custom_score >= 0.50:
                priority = 'HIGH'
            elif custom_score >= 0.30:
                priority = 'MEDIUM'
            else:
                priority = 'LOW'
            
            # Get original calculated data for reference
            original_data = app.calculate_priority_score(region)
            
            custom_priorities.append({
                'region': region_name,
                'score': custom_score,
                'priority': priority,
                'explanation': f"Custom score: {custom_score:.3f} (Original: {original_data['score']:.3f})",
                'indicators': original_data.get('indicators', {})
            })
        
        # Allocate funding based on custom scores
        allocations = app.allocate_funding(custom_priorities)
        
        # Calculate totals
        total_allocated = sum(details['amount'] for details in allocations.values())
        budget_utilization = (total_allocated / budget) * 100
        
        # Prepare context
        context = {
            'allocations': allocations,
            'total_allocated': total_allocated,
            'budget_utilization': budget_utilization,
            'is_custom': True
        }
        
        return render(request, 'funding/partials/allocation_display.html', context)
    
    except ValueError as e:
        return render(request, 'funding/partials/error.html', {
            'error_message': f'Invalid input: {str(e)}'
        })
    except Exception as e:
        return render(request, 'funding/partials/error.html', {
            'error_message': f'Error recalculating: {str(e)}'
        })


@require_http_methods(["POST"])
def calculate_priority(request, region_name):
    """
    Calculate priority for a specific region (HTMX endpoint)
    """
    try:
        from metta_atoms import Symbol
        
        app = BitePiperApp()
        region_symbol = Symbol(region_name)
        
        # Check if region exists
        if region_symbol not in app.regions:
            return render(request, 'funding/partials/error.html', {
                'error_message': f'Region {region_name} not found'
            })
        
        priority_data = app.calculate_priority_score(region_symbol)
        
        return render(request, 'funding/partials/priority_card.html', {
            'priority': priority_data
        })
    
    except Exception as e:
        return render(request, 'funding/partials/error.html', {
            'error_message': str(e)
        })


@require_http_methods(["GET"])
def api_health(request):
    """API health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'BITE-PIPER Funding Allocation',
        'version': '1.0.0',
        'backend': 'Django + HTMX'
    })


@require_http_methods(["GET"])
def get_regions(request):
    """Get list of available regions"""
    try:
        app = BitePiperApp()
        regions = [str(region) for region in app.regions]
        
        return JsonResponse({
            'regions': regions,
            'count': len(regions)
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


def about(request):
    """About page explaining the system"""
    return render(request, 'funding/about.html', {
        'title': 'About BITE-PIPER'
    })


# ============================================================================
# AGENT INTEGRATION VIEWS
# ============================================================================

@require_http_methods(["GET"])
async def agent_health(request):
    """Check agent health status (API endpoint)"""
    client = get_agent_client()
    health_data = await client.health_check()
    
    return JsonResponse(health_data)


@require_http_methods(["POST"])
async def agent_analyze_allocation(request):
    """
    Send allocation decision to agent for analysis (HTMX endpoint)
    Returns HTML partial with agent insights
    """
    try:
        # Get allocation data from POST
        budget = float(request.POST.get('budget', 1000000))
        
        # Recalculate to get allocation data
        app = BitePiperApp(total_budget=budget)
        use_advanced = request.POST.get('use_advanced', 'true').lower() == 'true'
        
        # Calculate priorities
        region_priorities = []
        for region in app.regions:
            if use_advanced:
                priority_data = app.calculate_priority_score(region)
                indicators = priority_data.get('indicators', {})
                if indicators:
                    advanced_result = calculate_advanced_priority_score(indicators)
                    priority_data['score'] = advanced_result['display_score']
                    priority_data['priority'] = advanced_result['priority_level']
                    priority_data['explanation'] = advanced_result['explanation']
                    priority_data['indicator_breakdown'] = advanced_result['indicator_breakdown']
                    priority_data['warnings'] = advanced_result.get('warnings', [])
                    priority_data['urgency'] = advanced_result['urgency']
            else:
                priority_data = app.calculate_priority_score(region)
            
            region_priorities.append(priority_data)
        
        # Allocate funding
        allocations = app.allocate_funding(region_priorities)
        
        # Send to agent for analysis
        client = get_agent_client()
        agent_results = await client.batch_analyze_allocations(allocations, region_priorities, budget)
        
        # Prepare context with agent insights
        context = {
            'agent_results': agent_results,
            'agent_results_json': json.dumps(agent_results),
            'allocations': allocations,
            'priorities': region_priorities,
            'budget': budget
        }
        
        return render(request, 'funding/partials/agent_analysis.html', context)
    
    except Exception as e:
        return render(request, 'funding/partials/error.html', {
            'error_message': f'Agent analysis error: {str(e)}'
        })


@require_http_methods(["POST"])
async def agent_analyze_single(request, region_name):
    """
    Analyze a single region allocation with agent (API endpoint)
    """
    try:
        # Get allocation details from POST
        amount = float(request.POST.get('amount', 0))
        budget = float(request.POST.get('budget', 1000000))
        priority_score = float(request.POST.get('priority_score', 0))
        
        # Build decision data
        decision_data = {
            "decision_type": "funding_allocation",
            "region": region_name,
            "amount": amount,
            "budget": budget,
            "priority_score": priority_score,
            "percentage": (amount / budget) * 100,
            "stakeholders": ["Local government", "Community organizations", "Social services"]
        }
        
        # Send to agent
        client = get_agent_client()
        result = await client.analyze_decision(decision_data)
        
        return JsonResponse(result)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
async def agent_dashboard(request):
    """
    Agent status dashboard page
    Shows agent capabilities and status
    """
    client = get_agent_client()
    health_data = await client.health_check()
    
    return render(request, 'funding/agent_dashboard.html', {
        'title': 'AI Agent Dashboard',
        'health': health_data
    })
