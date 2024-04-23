
import sqlite3

# Initialize connection to SQLite database
def init_db():
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    # Create inventory table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                (ID TEXT PRIMARY KEY NOT NULL,
                Name TEXT NOT NULL,
                Quantity INTEGER NOT NULL,
                Orders INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

# Function to add an item or update if exists
def add_or_update_item(id, name, quantity):
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute('''INSERT INTO inventory (ID, Name, Quantity, Orders) 
                 VALUES (?, ?, ?, 0)
                 ON CONFLICT(ID) DO UPDATE SET Name=excluded.Name, Quantity=excluded.Quantity''',
              (id, name, quantity))
    conn.commit()
    conn.close()

# Function to delete an item
def delete_item(item_id):
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute('DELETE FROM inventory WHERE ID = ?', (item_id,))
    conn.commit()
    conn.close()

# Function to place an order
def place_order(item_id, quantity):
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    message = "Not enough stock to fulfill the order or item not found"
    c.execute('SELECT Quantity FROM inventory WHERE ID = ?', (item_id,))
    row = c.fetchone()
    if row and row[0] >= quantity:
        c.execute('UPDATE inventory SET Quantity = Quantity - ?, Orders = Orders + ? WHERE ID = ?',
                  (quantity, quantity, item_id))
        conn.commit()
        message = f"Order placed for {quantity} of item {item_id}"
    conn.close()
    return message

# Function to fetch inventory for display
def fetch_inventory():
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute('SELECT ID, Name, Quantity FROM inventory')
    inventory = c.fetchall()
    conn.close()
    return inventory

# Function to fetch orders for display
def fetch_orders():
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute('SELECT ID, Name, Orders FROM inventory WHERE Orders > 0')
    orders = c.fetchall()
    conn.close()
    return orders
