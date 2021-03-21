function checkCartExists() {
    let cart = getDataFromLocalStorage();
    let cartExists = 'cart' in localStorage;
    if (cartExists == false) {
        saveCartInLocalStorage({});
    }
}

function addToCart(item_id) {
    updateCart(item_id);
    updateNumberInCartLabel(item_id);
    updateCartButton();
}

// updates data in 'cart'-object of localStorage (in the cart the key is item's id)
function updateCart(item_id) {
    let cartObject = getCartDataObject();
    if (cartObject == null) {
        cartObject = {};
    }
    let key = item_id;
    if (cartObject[key] != null) {
        let newValue = cartObject[key] * 1 + 1;
        cartObject[key] = newValue;
    } else {
        cartObject[key] = 1;
    }

    saveCartInLocalStorage(cartObject);
}

// will get number of the particular item in the cart (in 'cart'-object of localStorage)
// (in the cart the key is item's id)
function numberOfItemInCart(item_id) {
    let key = item_id;
    let cartObject = getCartDataObject();
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
    let cartObject = getCartDataObject();
    if (cartObject == null) {
        return 0;
    }
    values = Object.values(cartObject);
    total_value = values.reduce( function(sum, value) {
            return sum + parseInt(value)
        }, 0
    );
    return total_value;
}

function updateCartButton() {
    button = document.getElementById('cart_button_label');
    button.innerHTML = `( ${getNumberOfAllItemsInCart()} )`;
}

function getDataFromLocalStorage() {
    let data = window.localStorage.getItem('cart');
    return data;
}

function updateCartDataElement() {
    let data = getDataFromLocalStorage();
    cartDataElement = document.getElementById('cart_data');
    cartDataElement.value = data;
}

function changeCartItemQuantity(itemId, value) {
    let cartObject = getCartDataObject();

    const newValue = parseInt(value);
    if (newValue < 1 || newValue == null || value == '') {
        removeItemFromCart(itemId);
    } else {
        cartObject[itemId] = newValue;
        saveCartInLocalStorage(cartObject);
    }

    updateCartEndpointParams();
}

function getCartDataObject() {
    let cart = window.localStorage.getItem('cart');
    const cartObject = JSON.parse(cart);
    return cartObject;
}

function saveCartInLocalStorage(cartObject) {
   let json = JSON.stringify(cartObject);
   window.localStorage.setItem('cart', json);
}

// updates /cart endpoint with fresh cart_data (for case if the /cart page will be reloaded/refreshed)
function updateCartEndpointParams() {
    let json = getDataFromLocalStorage();
    endpointParams = '/cart?cart_data=' + json;
    history.pushState('', '', endpointParams);
}

// removes item from cart and saves changes to localStorage
function removeItemFromCart(itemId) {
    let cartObject = getCartDataObject();
    delete cartObject[itemId];
    saveCartInLocalStorage(cartObject);
}