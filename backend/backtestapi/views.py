from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import os, importlib, json
from strategies.run_strategy_metrics import run_strategy_metrics
from run_backtest import backtest
from django.views.decorators.http import require_GET
from django.conf import settings

@require_http_methods(["GET"])
def fixed_strategy(request):
    result = run_strategy_metrics()
    print(result)
    return JsonResponse(result, safe=False)


def scan(root):
    ans = {}
    for category in os.listdir(root):
        if category == "__pycache__":
            continue
        cat_path = os.path.join(root, category)
        if not os.path.isdir(cat_path):
            continue
        ans[category] = [
            f[:-3] for f in os.listdir(cat_path)
            if f.endswith(".py") and not f.startswith("__")
        ]
    return ans


@require_http_methods(["GET"])
def available_indicators(request):
    return JsonResponse({
        "entry": scan("indicators/entry"),
        "exit": scan("indicators/exit")
    })


@require_http_methods(["GET"])
def indicator_schema(request):
    group = request.GET.get("group")
    category = request.GET.get("category")
    name = request.GET.get("name")
    mod = importlib.import_module(f"indicators.{group}.{category}.{name}")
    schema = getattr(mod, "param_schema", lambda: {})()
    return JsonResponse(schema)


@csrf_exempt
@require_http_methods(["POST"])
def custom_strategy(request):
    data = json.loads(request.body)
    result = backtest(
        symbol=data.get("symbol", "MSFT"),
        start_date=data.get("start_date", "2012-01-03"),
        end_date=data.get("end_date", "2024-12-26",),
        entry_indicators=data.get("entry_indicators", []),
        exit_indicators=data.get("exit_indicators", []),
        entry_mode=data.get("entry_mode", "and"),
        exit_mode=data.get("exit_mode", "or"),
    )
    return JsonResponse(result, safe=False)

@require_GET
def list_symbols(request):
    data_path = os.path.join(settings.BASE_DIR, 'data')
    files = [
        f[:-4] for f in os.listdir(data_path)
        if f.endswith('.csv')
    ]
    return JsonResponse({'symbols': files})
