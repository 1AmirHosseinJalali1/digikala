cart = {
    "3": {
        "quantity": 2,
        "price": "120",
        'totalPrice':'2000'
           # شیء کامل محصول
    },
    "5": {
        "quantity": 1,
        "price": "300",
        'totalPrice':'3000'
        
    }
}
# for key , values in cart.items:
#     print(key,values['price'])
    # cart[key]['totalprice'] = 10
# if cart :
#     print('true')
# else:
#     print('false')
# x = cart.keys()
# for i in x :

#     print(i)
# cart["3"]['product'] = 'product'
# for key in cart:
#     cart[key]['product'] = 'product'
# print(cart)

for item in cart.values():
    print(item['totalPrice'])