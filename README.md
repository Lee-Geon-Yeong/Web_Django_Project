# 애주가를 위한 주류 전용 Website

## 1. Subject

### Drunken-tiger-mall 온라인 주류 거래 사이트

## 2. Team members
- 이건영 https://github.com/Lee-Geon-Yeong
- 권혜주 https://github.com/hyejoo-kwon
- 한지훈 https://github.com/codenamenadja

## 3. Usage
- Purchase
```
1. naver혹은 일반유저로 가입을 진행해야합니다.
2. 로그인이 되어있다면 원하는 상품을 디테일하게 확인할 수 있으며,
   상품을 구매할 수 있습니다.
3. 원하는 상품을 filter를 사용하여 검색한 뒤, 상세페이지로 이동해주세요.
4. Quantity를 선택한 후, add to cart 해주세요.
5. Mypage에 접근하시면 본인의 cart를 확인할 수 있으며,
6. 해당목록에 대해서 구매를 원하면 Payment 버튼을 클릭해야합니다.
7. Payment가 지불되기 전까지 새로운 Payment를 생성할 수 없습니다.
```
- like products
```
1. naver혹은 일반유저로 가입을 진행해야합니다.
2. 로그인이 되어있다면 원하는 상품을 디테일하게 확인할 수 있으며,
   상품을 좋아요 마크할 수 있습니다.
3. 제품을 like하고 싶다면 제품 리스트에 보이는 Like버튼을 클릭해주세요.
4. 같은 주소에서 like를 disable 하는 버튼을 통해 취소 할 수 있습니다.
```

## 4. Features
- 추천수에 따른 제품 추천
- 상세 검색 필터링을 사용한 검색기능
- 소셜 로그인 기능
- 제품 장바구니 및 구매신청 기능
- 호스팅서비스플랫폼 활용-ttps적용

## 5. Prototype Views
- 초기 메인 화면<br>
![image](https://user-images.githubusercontent.com/59759468/105464277-a1a99600-5cd4-11eb-92c1-eacd05d06ca8.png)
- 필터링 기능 화면<br>
![image](https://user-images.githubusercontent.com/59759468/105464280-a40bf000-5cd4-11eb-831d-9da00e21d941.png)
- 카트 목록 화면<br>
![image](https://user-images.githubusercontent.com/59759468/105464289-a8380d80-5cd4-11eb-8825-a94449655530.png)

## 6. Database Model
- Drinks & Brand<br>
![image](https://user-images.githubusercontent.com/59759468/105464356-d0277100-5cd4-11eb-8626-dc8eb5f3da62.png)
drinks 는 category로서 필터링 역할을 해줄 brand 를 참조합니다. 그 외에도 추천하는 음식과 좋아요, price등으로 검색이 가능하도록 구성되었습니다. drinks 에서만 검색하는 것 뿐 아니라, brand 에 속하는 drinks 를 검색할 수 있습니다.

- Cart & Payment<br>
![image](https://user-images.githubusercontent.com/59759468/105464362-d3226180-5cd4-11eb-9e21-953917058a04.png)
accounts 는 cutomized usermodel입니다. 기존 builtin usermodel과 유사하지만 BaseUser를 Overide하되, 소셜 로그인을 위해 email을 user-identity로 사용하며, Annoymous user혹은 staff는 cart를 부여받지 않기 때문에 장바구니에 담기와 구매가 허용되지 않습니다. carts에 저장된 목록이 payments로 전환되면 이전에 payments가 처리되기 전까지 새로운 payemnt를 만들 수 없습니다.
- Likes & account<br>
![image](https://user-images.githubusercontent.com/59759468/105464368-d61d5200-5cd4-11eb-9b1a-c355bd0a09bc.png)
한 유저는 모든 drinks 에 대한 1개의 like row 를 생성할 수 있습니다. 간단한 처리이며, 자신의 likes를 확보하고, likes를 ordering으로 활용하기 위한 용도로 구현하였습니다. 현재는 list_view 에서 로그인이 되어있는 상태라면 간단하게 button으로 toggle가능하도록 처리하고 있습니다.

## 7. Code sample
프로젝트의 대부분의 url 에 매치되는 view 는 함수로 구현되었습니다. 프로젝트 규모 작을때 코드재활용에 대한 필요성이 적어지는 것과 직관적이라는 점, 그리고 규모가 작을 경우 최적화문제는 IO 에서 가장 두드러지기 떄문에 SQL Query 에 조금 더 신경쓸 수 있도록 하였습니다.
```
@require_GET
def main_view(request):
    objects = Drinks.objects.all().order_by('-likes')[:16]
    return render(request,template_name='drinks/index.html',context={"objects":objects})

@require_http_methods(["GET", "POST"])
def list_filter_view(request):
    if request.method == "POST":
        return toggle_like(request)
    PAGE_SIZE = 1
    objects = Drinks.objects.select_related('brand')
    f = DrinkFilter(request.GET, queryset=objects) # 1.49ms
    paginator = Paginator(f.qs, PAGE_SIZE)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    return render(request,template_name='drinks/list.html',context={'filter':f, 'objects':response})

@login_required
def like_create_destroy_view(request):
    pk = request.POST.get('drink_like')
    drink = Drinks.objects.get(id=pk)
    likes = Likes.objects.filter(user=request.user, drink=drink)
    if likes:
        likes.delete()
    else:
        likes = Likes.objects.create(drink=drink, user=request.user)
    return HttpResponseRedirect(redirect_to=request.path_info)

@require_GET
def brand_detail_view(request, brand_name):
    objects = Brand.objects.prefetch_related(Prefetch('drinks')).get(name=brand_name)
    return render(request,template_name='drinks/brand.html', context={'object':objects})

@login_required
@require_http_methods(['GET', 'POST'])
def drink_detail_view(request, pk):
    if request.method == 'POST':
        amount = request.POST.get('quantity')
        form = CartItemCreateForm(request.POST)
        if form.is_valid():
            user_cart = get_cart_and_items(request)
            created = create_cart_item(pk, form.cleaned_data['quantity'], user_cart)
        return HttpResponseRedirect(reverse_lazy('mypage:index'))
    form = CartItemCreateForm()
    return render(request, template_name="drinks/detail.html", context={'object':Drinks.objects.get(id=pk), 'form':form})
```

## 8. Complements
![image](https://user-images.githubusercontent.com/59759468/105464849-85f2bf80-5cd5-11eb-9698-1b94804944e1.png)
