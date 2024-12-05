import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const port = 1245;

// Create a Redis client and promisify methods
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// List of products (already defined earlier)
const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

// Function to get item by ID
function getItemById(id) {
  return listProducts.find(product => product.id === id);
}

// Route to list all products
app.get('/list_products', (req, res) => {
  const products = listProducts.map(product => ({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
  }));
  res.json(products);
});

// Route to get product details and current available stock
app.get('/list_products/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const product = getItemById(Number(itemId));

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const reservedStock = await getAsync(`item.${itemId}`) || 0;
  const availableQuantity = product.stock - reservedStock;

  res.json({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity: availableQuantity,
  });
});

// Function to reserve stock for an item
async function reserveStockById(itemId, stock) {
  const currentReservedStock = await getAsync(`item.${itemId}`) || 0;
  const newReservedStock = parseInt(currentReservedStock) + stock;
  await setAsync(`item.${itemId}`, newReservedStock);
}

// Route to reserve a product
app.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const product = getItemById(Number(itemId));

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const reservedStock = await getAsync(`item.${itemId}`) || 0;
  const availableQuantity = product.stock - reservedStock;

  if (availableQuantity <= 0) {
    return res.status(400).json({
      status: 'Not enough stock available',
      itemId: product.id,
    });
  }

  await reserveStockById(itemId, 1); // Reserve one item
  res.json({ status: 'Reservation confirmed', itemId: product.id });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});

