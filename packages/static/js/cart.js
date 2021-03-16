function addToCart(item_id) {
    let key = `item_id_${item_id}`;
    storage = window.localStorage
    var item_quantity = storage.getItem(key);
    item_quantity = item_quantity * 1 + 1;
    storage.setItem(key, item_quantity);

    console.log(`======== LOG !!!!=== ${item_id}`);
    updateNumberInCartLabel(item_id);
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

    console.log('updateNumberInCartLabel', item_id);
}

function hideNumberInCartLabel(item_id) {
    label = document.getElementById('number_in_cart_')
    label.type = 'hidden'
}
