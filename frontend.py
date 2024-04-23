
import streamlit as st
from backend import add_or_update_item, delete_item, place_order, fetch_inventory, fetch_orders, init_db
import pandas as pd
import matplotlib.pyplot as plt

# Initialize the database
init_db()

def main():
    st.sidebar.title("Role Selection")
    role = st.sidebar.radio("", ["Admin", "Customer"])

    if role == "Admin":
        admin_page()
    elif role == "Customer":
        customer_page()

def admin_page():
    st.title("👑 Admin Dashboard")

    # Add or Update Item
    with st.form("add_item"):
        st.subheader("Add or Update an Item")
        id = st.text_input("Item ID", "")
        name = st.text_input("Item Name", "")
        quantity = st.number_input("Quantity", 0)
        submit_button = st.form_submit_button(label="Submit")
        if submit_button:
            add_or_update_item(id, name, quantity)
            st.success(f"Item {name} added/updated successfully!")

    # Delete Item
    with st.form("delete_item"):
        st.subheader("Delete an Item")
        del_id = st.text_input("Item ID to Delete", key="del")
        delete_button = st.form_submit_button(label="Delete Item")
        if delete_button:
            delete_item(del_id)
            st.success(f"Item {del_id} deleted successfully!")

    # Display Inventory
    st.subheader("Inventory")
    inventory = fetch_inventory()
    st.dataframe(pd.DataFrame(inventory, columns=['ID', 'Name', 'Quantity']))

    # Display Orders
    st.subheader("Received Orders")
    orders = fetch_orders()
    st.dataframe(pd.DataFrame(orders, columns=['ID', 'Name', 'Orders']))

def customer_page():
    st.title("🛍️ Customer Dashboard")
    
    # Display Items
    st.subheader("Available Items")
    inventory = fetch_inventory()
    st.dataframe(pd.DataFrame(inventory, columns=['ID', 'Name', 'Quantity']))

    # Place an Order
    with st.form("place_order"):
        st.subheader("Place an Order")
        order_id = st.text_input("Item ID", key="order_id")
        order_quantity = st.number_input("Order Quantity", min_value=1, value=1, key="order_quantity")
        order_button = st.form_submit_button("Place Order")
        if order_button:
            message = place_order(order_id, order_quantity)
            st.success(message)

if __name__ == "__main__":
    main()
