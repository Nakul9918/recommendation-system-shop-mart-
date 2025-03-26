const recommendations = {
    "Premia Tea Masala": { products: ["Sugar Cubes", "Elaichi", "Ginger Powder", "Honey", "Milk Powder"], prices: [50, 100, 75, 120, 80] },
    "Laptop": { products: ["Mouse", "Keyboard", "Cooling Pad"], prices: [500, 800, 1000] }
};

let selectedItems = [];
let trendingProducts = { "Sugar Cubes": 10, "Elaichi": 20, "Laptop": 15, "Mouse": 12, "Cooling Pad": 18 };

// Function to Load Recommendations
function loadRecommendations() {
    const product = document.getElementById("product").value;
    const recommendationList = document.getElementById("recommendation-list");
    recommendationList.innerHTML = recommendations[product] 
        ? recommendations[product].products.map((item, index) => createRecommendationHTML(item, recommendations[product].prices[index])).join("")
        : "<p>No recommendations available.</p>";
}

// Helper function to create recommendation HTML
function createRecommendationHTML(item, price) {
    return `
        <div class="recommend-item">
            <span>${item} - ₹${price}</span>
            <button class="add-btn" onclick="addToCart('${item}', ${price})">Add</button>
        </div>`;
}

// Function to Add Selected Product
function addToCart(item, price) {
    let existingItem = selectedItems.find(i => i.name === item);
    existingItem ? existingItem.quantity++ : selectedItems.push({ name: item, price, quantity: 1 });

    trendingProducts[item] = (trendingProducts[item] || 0) + 1;
    updateCartUI();
    updateTrendingChart();
}

// Function to Remove Selected Product
function removeFromCart(itemName) {
    selectedItems = selectedItems.filter(i => i.name !== itemName);
    updateCartUI();
}

// Function to Update Cart UI
function updateCartUI() {
    const cartList = document.getElementById("cart-items");
    cartList.innerHTML = selectedItems.length
        ? selectedItems.map(item => createCartItemHTML(item)).join("")
        : "<p>Your cart is empty.</p>";

    document.getElementById("total-price").textContent = `₹${selectedItems.reduce((sum, item) => sum + item.price * item.quantity, 0)}`;
}

// Helper function to create cart item HTML
function createCartItemHTML(item) {
    return `
        <li>
            ${item.name} - ₹${item.price} x 
            <input type="number" value="${item.quantity}" min="1" class="quantity-input" onchange="updateQuantity('${item.name}', this.value)">
            <button class="remove-btn" onclick="removeFromCart('${item.name}')">Remove</button>
        </li>`;
}

// Function to Update Quantity in Cart
function updateQuantity(itemName, newQuantity) {
    let item = selectedItems.find(i => i.name === itemName);
    if (item) {
        item.quantity = Math.max(1, parseInt(newQuantity) || 1);
        updateCartUI();
    }
}

// Function to Update Trending Products Chart
function updateTrendingChart() {
    trendingChart.data.labels = Object.keys(trendingProducts);
    trendingChart.data.datasets[0].data = Object.values(trendingProducts);
    trendingChart.update();
}

// Initialize Chart.js Bar Chart
const ctx = document.getElementById("trendingChart").getContext("2d");
const trendingChart = new Chart(ctx, {
    type: "bar",
    data: {
        labels: Object.keys(trendingProducts),
        datasets: [{
            label: "Trending Products",
            data: Object.values(trendingProducts),
            backgroundColor: "rgba(75, 192, 192, 0.6)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: (context) => `Sold: ${trendingProducts[context.label] || 0} times`
                }
            }
        },
        scales: { y: { beginAtZero: true } }
    }
});
