async function loadProducts() {
    const res = await fetch('/products/');
    const data = await res.json();

    const container = document.getElementById('products');
    container.innerHTML = "";

    data.forEach(p => {
        container.innerHTML += `
            <div class="card">
                <h3>${p.name}</h3>
                <p>₹${p.price}</p>
                <p>Stock: ${p.stock}</p>
                <button onclick="buyProduct(${p.id})">Buy</button>
            </div>
        `;
    });
}

async function addProduct() {
    const name = document.getElementById('name').value;
    const price = parseFloat(document.getElementById('price').value);
    const stock = parseInt(document.getElementById('stock').value);

    await fetch('/products/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, price, stock })
    });

    loadProducts();
}

async function buyProduct(id) {
    alert("Purchase feature coming soon!");
}

loadProducts();