from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import os, importlib, json
from strategies.run_strategy_metrics import run_strategy_metrics
from run_backtest import backtest
from django.views.decorators.http import require_GET

@require_http_methods(["GET"])
def fixed_strategy(request):
    result = run_strategy_metrics()
    return JsonResponse(result, safe=False)


def scan(root):
    ans = {}
    for category in os.listdir(root):
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
        entry_indicators=data.get("entry_indicators", []),
        exit_indicators=data.get("exit_indicators", []),
        entry_mode=data.get("entry_mode", "and"),
        exit_mode=data.get("exit_mode", "or"),
    )
    return JsonResponse(result, safe=False)
