from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .helper import checkLogin,createNewToken,addNewUserToken,registerUser,getUsernameToken,getUserByUsername

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

@csrf_exempt
def newChat(request):
    username = request.POST['username']
    token = request.POST['token']
    if getUsernameToken(token):
        user = getUserByUsername(username)
        if user != None:
            return JsonResponse({'statusCode': 200, 'fullName': user.name},safe=False)
        return JsonResponse({'statusCode': 400, 'error': 'User Not Exist'},safe=False)
    return JsonResponse({'statusCode': 401, 'error': 'Invalid Token'},safe=False)