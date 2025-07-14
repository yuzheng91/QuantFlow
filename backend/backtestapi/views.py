from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import os, importlib, json
from strategies.run_strategy_metrics import run_strategy_metrics
from run_backtest import backtest

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
        data["entry_category"], data["entry_name"],
        data["exit_category"],  data["exit_name"],
        data.get("entry_params", {}),
        data.get("exit_params", {})
    )
    return JsonResponse(result, safe=False)
