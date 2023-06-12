import datetime
import json
from uuid import uuid4

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from bbsh_api.models import Basket, History, Menu, MyUser, OrderList


def error_handler(func):
    def wrapper(*args, **kwargs) -> JsonResponse:
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            return JsonResponse(str(type(e)) + str(e.args), status=400, safe=False)

    return wrapper


@error_handler
def validate_user(request, user_id, only_staff) -> JsonResponse | None:
    if isinstance(request.user, AnonymousUser):
        return JsonResponse("not authorised", status=401, safe=False)
    if request.user.id != user_id:
        return JsonResponse("wrong user", status=401, safe=False)
    if only_staff and not request.user.is_staff:
        return JsonResponse("only for staff", status=403, safe=False)
    return None


@error_handler
def count_orders(user_id) -> int:
    history_count = History.objects.filter(user=user_id).count()
    return history_count


@error_handler
@require_http_methods(["GET"])
def user_basket(request, user_id) -> JsonResponse:
    if resp := validate_user(request, user_id, False):
        return resp
    user: MyUser = request.user
    order_list = Basket.objects.filter(user=user)
    res = [order.to_dict() for order in order_list]
    return JsonResponse(res, safe=False)


@csrf_exempt
@error_handler
@require_http_methods(["POST"])
def user_login(request) -> JsonResponse:
    if not isinstance(request.user, AnonymousUser):
        return JsonResponse("already in account", safe=False)
    attrs = json.loads(request.body)
    username = attrs["username"]
    password = attrs["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse(user.id, safe=False)
    else:
        return JsonResponse("Incorrect data", status=400, safe=False)


@csrf_exempt
def user_logout(request) -> JsonResponse:
    logout(request)
    return JsonResponse(None, status=204, safe=False)


@csrf_exempt
@error_handler
@require_http_methods(["PUT"])
def user_registration(request) -> JsonResponse:
    if not isinstance(request.user, AnonymousUser):
        return JsonResponse("you are in account", safe=False)
    attrs = json.loads(request.body)
    username = attrs["username"]
    password = attrs["password"]
    phone = attrs["phone"]
    if MyUser.objects.filter(Q(username=username) | Q(phone=phone)):
        return JsonResponse("user is already exists", safe=False)
    else:
        user = MyUser(username=username, password=password, phone=phone, id=uuid4())
        user.set_password(password)
        user.save()
        login(request, user)
        return JsonResponse(user.id, status=201, safe=False)


@error_handler
@require_http_methods(["GET"])
def show_menu(request) -> JsonResponse:
    menu = Menu.objects.all()
    res = [dish.to_dict() for dish in menu]
    return JsonResponse(res, safe=False)


@error_handler
@require_http_methods(["GET"])
def user_history(request, user_id) -> JsonResponse:
    if resp := validate_user(request, user_id, False):
        return resp
    user: MyUser = request.user
    history = History.objects.filter(user=user.id)
    res = [order.to_dict() for order in history]
    return JsonResponse(res, safe=False)


@error_handler
@require_http_methods(["GET"])
def user_profile(request, user_id) -> JsonResponse:
    if resp := validate_user(request, user_id, False):
        return resp
    user: MyUser = request.user
    info = user.to_dict()
    info["total orders"] = count_orders(user.id)
    return JsonResponse(info, safe=False)


@csrf_exempt
@error_handler
@require_http_methods(["PUT"])
def menu_add(request, staff_id) -> JsonResponse:
    if resp := validate_user(request, staff_id, True):
        return resp
    attrs = json.loads(request.body)
    if Menu.objects.filter(name=attrs["name"]):
        return JsonResponse("dish is already exists", status=409, safe=False)
    new_position = Menu(
        name=attrs["name"],
        cost=attrs["cost"],
        size=attrs["size"],
        ingredients=attrs["ingredients"],
    )
    new_position.save()
    return JsonResponse(True, status=201, safe=False)


@csrf_exempt
@error_handler
@require_http_methods(["DELETE"])
def menu_delete(request, staff_id) -> JsonResponse:
    if resp := validate_user(request, staff_id, True):
        return resp
    attrs = json.loads(request.body)
    dish = Menu.objects.get(name=attrs["name"])
    dish.delete()
    return JsonResponse(True, safe=False)


@csrf_exempt
@error_handler
@require_http_methods(["PUT"])
def user_basket_add(request, user_id) -> JsonResponse:
    if resp := validate_user(request, user_id, False):
        return resp
    attrs = json.loads(request.body)
    dish_name = attrs["dish_name"]
    dop_ingredients = attrs["dop_ingredients"]
    dish = Menu.objects.get(name=dish_name)
    order = Basket(
        dish=dish, dop_ingredients=dop_ingredients, user=request.user, id=uuid4()
    )
    order.save()
    return JsonResponse(True, safe=False)


@csrf_exempt
@error_handler
@require_http_methods(["DELETE"])
def user_basket_delete(request, user_id) -> JsonResponse:
    if resp := validate_user(request, user_id, False):
        return resp
    attrs = json.loads(request.body)
    order_id = attrs["order_id"]
    Basket.objects.filter(id=order_id).delete()
    return JsonResponse(True, safe=False)


@csrf_exempt
@error_handler
@require_http_methods(["PATCH"])
def user_make_order(request, user_id) -> JsonResponse:
    if resp := validate_user(request, user_id, False):
        return resp
    if not (order := Basket.objects.filter(user=request.user)):
        return JsonResponse("empty basket", safe=False)
    last_order = OrderList.objects.order_by("-order_id").first()
    order_id = 0 if last_order is None else last_order.order_id + 1
    date_time = datetime.datetime.now().date()
    attrs = json.loads(request.body)
    for last_order in order:
        new_order = OrderList(
            dish=last_order.dish,
            dop_ingredients=last_order.dop_ingredients,
            date_time=date_time,
            user=request.user,
            order_id=order_id,
            comments=attrs["comments"],
        )
        new_order.save()
    Basket.objects.filter(user=request.user).delete()
    return JsonResponse(order_id, safe=False)


@csrf_exempt
@error_handler
@require_http_methods(["PATCH"])
def accept_order(request, staff_id) -> JsonResponse:
    if resp := validate_user(request, staff_id, True):
        return resp
    attrs = json.loads(request.body)
    order_id = attrs["order_id"]
    if not (order_list := OrderList.objects.filter(order_id=order_id)):
        return JsonResponse("Wrong order_id", status=400, safe=False)
    for temp in order_list:
        temp.accepted = True
        temp.save()
    return JsonResponse(True, safe=False)


@csrf_exempt
@error_handler
@require_http_methods(["PATCH"])
def dismiss_order(request, staff_id) -> JsonResponse:
    if resp := validate_user(request, staff_id, True):
        return resp
    attrs = json.loads(request.body)
    order_id = attrs["order_id"]
    order = OrderList.objects.get(order_id=order_id)
    if order.accepted:
        return JsonResponse("Already accepted", safe=False)
    OrderList.objects.filter(order_id=order_id).delete()
    return JsonResponse(True, safe=False)


@csrf_exempt
@error_handler
@require_http_methods(["GET"])
def show_all_orders(request, staff_id) -> JsonResponse:
    if resp := validate_user(request, staff_id, True):
        return resp
    res = [order.to_dict() for order in OrderList.objects.all()]
    return JsonResponse(res, safe=False)


@error_handler
@require_http_methods(["GET"])
def get_user_info(request, staff_id) -> JsonResponse:
    if resp := validate_user(request, staff_id, True):
        return resp
    user_id = request.GET["user_id"]
    user = MyUser.objects.get(id=user_id)
    info = user.to_dict()
    info["total_orders"] = count_orders(user.id)
    return JsonResponse(info)


@csrf_exempt
@error_handler
@require_http_methods(["DELETE"])
def user_profile_delete(request, user_id) -> JsonResponse:
    if resp := validate_user(request, user_id, False):
        return resp
    MyUser.objects.filter(id=user_id).delete()
    return JsonResponse(True, safe=False)


@csrf_exempt
@error_handler
@require_http_methods(["PATCH"])
def ready_order(request, staff_id) -> JsonResponse:
    if resp := validate_user(request, staff_id, True):
        return resp
    attrs = json.loads(request.body)
    order = OrderList.objects.filter(order_id=attrs["order_id"])
    if not order:
        return JsonResponse("wrong order_id", status=400)
    for dish in order:
        record = History(
            name=dish.dish.name,
            cost=dish.dish.cost,
            size=dish.dish.size,
            dop_ingredients=dish.dop_ingredients,
            date_time=dish.date_time,
            user=dish.user.id,
            id=uuid4(),
        )
        record.save()
    OrderList.objects.filter(order_id=attrs["order_id"]).delete()
    return JsonResponse(True, safe=False)


@csrf_exempt
@error_handler
@require_http_methods(["GET"])
def show_all_history(request, staff_id) -> JsonResponse:
    if resp := validate_user(request, staff_id, True):
        return resp
    res = [record.to_dict() for record in History.objects.all()]
    return JsonResponse(res, safe=False)


@csrf_exempt
@error_handler
@require_http_methods(["GET"])
def get_order_info(request, user_id):
    if resp := validate_user(request, user_id, False):
        return resp
    order_id = request.GET["order_id"]
    order = OrderList.objects.filter(Q(user_id=user_id) & Q(order_id=order_id))
    res = [record.to_dict() for record in order]
    return JsonResponse(res, safe=False)


def server_is_healthy(request):
    return JsonResponse("Server is healthy", safe=False)
