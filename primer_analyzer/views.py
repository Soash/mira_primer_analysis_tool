from django.shortcuts import render
from django.http import JsonResponse
import json
from .utils import analyze_single_primer, analyze_dimer_dg

# Create your views here.

def index(request):
    return render(request, 'primer_analyzer/index.html')

def analyze_primers(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            fp = data.get('fp', '')
            rp = data.get('rp', '')

            fp_stats = analyze_single_primer(fp) if fp else None
            rp_stats = analyze_single_primer(rp) if rp else None
            
            fp_fp_dg = analyze_dimer_dg(fp, fp) if fp else 0.00
            rp_rp_dg = analyze_dimer_dg(rp, rp) if rp else 0.00
            fp_rp_dg = analyze_dimer_dg(fp, rp) if fp and rp else 0.00

            response_data = {
                'fp_stats': fp_stats,
                'rp_stats': rp_stats,
                'fp_fp_dg': round(fp_fp_dg, 2),
                'rp_rp_dg': round(rp_rp_dg, 2),
                'fp_rp_dg': round(fp_rp_dg, 2)
            }
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
