from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def getHome(request):
    r1 = {'id': 1, 'title': 'Slow-Cooker Chicken Tikka Masala', 'description': 'Thinking about Indian food tonight? Assemble the whole pot in the morning and come home to the taste of takeout.', 'cover': 'https://food.fnr.sndimg.com/content/dam/images/food/fullset/2013/9/28/0/FNK_Buffalo-Style-Chicken-Wings_s4x3.jpg.rend.hgtvcom.616.462.suffix/1383780068425.jpeg', 'likeCount': 12}
    r2 = {'id': 2, 'title': 'Shrimp Pad Thai', 'description': 'Quick-cooking shrimp bulk up pad Thai in a hurry', 'cover': 'https://food.fnr.sndimg.com/content/dam/images/food/editorial/blog/legacy/fn-dish/2014/2/fnd_Ginger-Pork-Over-Pasta-Foodlets_s4x3_lg.jpg.rend.hgtvcom.616.462.suffix/1505017091127.jpeg', 'likeCount': 22}
    r3 = {'id': 3, 'title': 'Ginger Pork with Sugar Snap Peas', 'description': 'A quick sauce spiked with fresh garlic and ginger adds bold flavor this weeknight staple.', 'cover': 'https://food.fnr.sndimg.com/content/dam/images/food/fullset/2016/8/23/0/FNK_cast-iron-skillet-pizza_s4x3.jpg.rend.hgtvcom.616.462.suffix/1473350486403.jpeg', 'likeCount': 13}
    r4 = {'id': 4, 'title': 'Skillet Deep-Dish Pizza', 'description': 'Good news, folks: No pizza stone required here! Just break out your cast-iron skillet to get that crispy crust you crave.', 'cover': 'https://food.fnr.sndimg.com/content/dam/images/food/fullset/2012/10/2/0/FNM_110112-Beef-Pho-Recipe_s4x3.jpg.rend.hgtvcom.616.462.suffix/1382451880742.jpeg', 'likeCount': 42}
    r5 = {'id': 5, 'title': 'Beef Pho', 'description': 'Make your own broth or start with the store-bought stuff. We’ll never tell.', 'cover': 'https://food.fnr.sndimg.com/content/dam/images/food/unsized/2016/1/7/0/fnd_foodlets-cheeseburger-hand-pies.jpg', 'likeCount': 15}
    return JsonResponse({'status':200, 'recipeList': [r1,r2,r3,r4,r5]},safe=False)