function addToCart(item_id) {
    let key = `item_id_${item_id}`;
    storage = window.localStorage
    var item_quantity = storage.getItem(key);
    item_quantity = item_quantity * 1 + 1;
    storage.setItem(key, item_quantity);

    updateNumberInCartLabel(item_id);
    updateCartButton();
}

function itemsInCartCount(item_id) {
    let key = `item_id_${item_id}`;
    let item_quantity = window.localStorage.getItem(key);
    return item_quantity;
}

// updates label of the item with number of already added items to cart
function updateNumberInCartLabel(item_id) {
    id = `number_in_cart_${item_id}`
    label = document.getElementById(id);
    label.innerHTML = 'Already in cart - ' + itemsInCartCount(item_id);
    label.type = '';
}

function hideNumberInCartLabel(item_id) {
    label = document.getElementById('number_in_cart_')
    label.type = 'hidden'
}

function getNumberOfItemsInCart() {
    storage = window.localStorage;
    number_of_items_in_cart = 0;
    for (var i = 0; i < storage.length; i++) {
        let key = storage.key(i);
        if (key.startsWith('item_id_')) {;
            value = storage.getItem(key)
            number_of_items_in_cart += Number.parseInt(value);
        }
    }
    return number_of_items_in_cart;
}

function updateCartButton() {
    button = document.getElementById('cart_button')
    console.log('getNumberOfItemsInCart', getNumberOfItemsInCart())
    button.innerHTML = `( ${getNumberOfItemsInCart()} )`
}