def cart_item_count(request):
    cart_data = request.session.get('cart_product_data', {})
    count = len(cart_data)
    return {'cart_item_count': count}