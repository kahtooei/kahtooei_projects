from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .helper import checkLogin,createNewToken,addNewUserToken,registerUser

# Create your views here.

@csrf_exempt
def checkConnect(request):
    return JsonResponse({'status':'OK'},safe=False)

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    result = checkLogin(username,password)
    if result['status']:
        token = createNewToken()
        r=addNewUserToken(result['user'],token)
        if r:
            return JsonResponse({'statusCode': 200, 'fullName': result['user'].name, 'token': token},safe=False)
        else:
            return JsonResponse({'statusCode': 400, 'error': 'Token Error'},safe=False)
    else:
        return JsonResponse({'statusCode': 400, 'error': 'Invalid Username Or Password'},safe=False)

@csrf_exempt
def register(request):
    username = request.POST['username']
    password = request.POST['password']
    fullName = request.POST['fullName']
    result = registerUser(fullName,username,password)
    if result['status']:
        token = createNewToken()
        r=addNewUserToken(result['user'],token)
        if r:
            return JsonResponse({'statusCode': 200, 'token': token},safe=False)
        else:
            return JsonResponse({'statusCode': 400, 'error': 'Token Error'},safe=False)
    else:
        return JsonResponse({'statusCode': 400, 'error': result['error']},safe=False)