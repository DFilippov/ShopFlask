function addToCart(item_id) {
    let cartExists = localStorage.getItem('cart') != null;
    if (cartExists == false) {
        localStorage.setItem('cart', null);
    }

    updateCart(item_id);
    updateNumberInCartLabel(item_id);
    updateCartButton();
}

// updates data in 'cart'-object of localStorage (in the cart the key is item's id)
function updateCart(item_id) {
    let cart = localStorage.getItem('cart');
    let cartObject = JSON.parse(cart);
    if (cartObject == null) {
        cartObject = {}
    }
    let key = item_id;
    if (cartObject[key] != null) {
        let newValue = cartObject[key] * 1 + 1
        cartObject[key] = newValue
    } else {
        cartObject[key] = 1
    }

    updated = JSON.stringify(cartObject)
    localStorage.setItem('cart', updated)
}

// will get number of the particular item in the cart (in 'cart'-object of localStorage)
// (in the cart the key is item's id)
function numberOfItemInCart(item_id) {
    let key = item_id;
    let cart = window.localStorage.getItem('cart');
    let cartObject = JSON.parse(cart);
    let item_quantity = cartObject[key];
    return item_quantity;
}


// updates label of the item with number of already added items to cart
function updateNumberInCartLabel(item_id) {
    id = `number_in_cart_${item_id}`
    label = document.getElementById(id);
    label.innerHTML = 'Already in cart - ' + numberOfItemInCart(item_id);
    label.type = '';
}

function getNumberOfAllItemsInCart() {
    let cart = localStorage.getItem('cart');
    let cartObject = JSON.parse(cart);
    values = Object.values(cartObject);
    total_value = values.reduce( function(sum, value) {
            return sum + value
        }, 0
    );
    return total_value;
}

function updateCartButton() {
    button = document.getElementById('cart_button_label');
    button.innerHTML = `( ${getNumberOfAllItemsInCart()} )`;
}

function getDataFromLocalStorage() {
    let data = localStorage.getItem('cart');
    return data;
}

function updateCartDataElement() {
    data = getDataFromLocalStorage();
    cartDataElement = document.getElementById('cart_data');
    cartDataElement.value = data
}
