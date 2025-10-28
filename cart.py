import streamlit as st

st.set_page_config(page_title="Cart", page_icon="🧺", layout="wide")

# You can keep a mirror of products here (or load from a shared module/json)
PRODUCTS = {
    "p1": {"title": "Wireless Headphones", "price": 49.99, "icon": "🎧"},
    "p2": {"title": "Smart Watch",         "price": 79.00, "icon": "⌚"},
    "p3": {"title": "Mechanical Keyboard", "price": 59.50, "icon": "⌨️"},
    "p4": {"title": "USB-C Charger 65W",   "price": 29.99, "icon": "🔌"},
    "p5": {"title": "Portable SSD 1TB",    "price": 89.99, "icon": "💾"},
}

if "cart" not in st.session_state:
    st.session_state.cart = {}

def inc(pid):
    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1

def dec(pid):
    if pid in st.session_state.cart:
        st.session_state.cart[pid] -= 1
        if st.session_state.cart[pid] <= 0:
            del st.session_state.cart[pid]

def remove(pid):
    st.session_state.cart.pop(pid, None)

def clear_cart():
    st.session_state.cart = {}

# ---------- Header ----------
left, right = st.columns([3, 1])
with left:
    st.title("Your Cart")
with right:
    try:
        if st.button("← Back to Products", use_container_width=True):
            st.switch_page("../app.py")
    except Exception:
        st.caption("Open the **Mini Store** page from the sidebar.")

st.divider()

# ---------- Body ----------
cart = st.session_state.cart
if not cart:
    st.info("Your cart is empty. Add items from the **Mini Store** page.", icon="ℹ️")
else:
    subtotal = 0.0
    for pid, qty in cart.items():
        p = PRODUCTS[pid]
        line = p["price"] * qty
        subtotal += line

        with st.container(border=True):
            cols = st.columns([6, 2, 2, 2])
            cols[0].markdown(f"### {p['icon']} {p['title']}\n${p['price']:.2f} each")
            with cols[1]:
                st.markdown("**Quantity**")
                qcols = st.columns([1, 1, 1])
                if qcols[0].button("−", key=f"dec_{pid}"):
                    dec(pid)
                    st.rerun()
                qcols[1].markdown(f"<div style='text-align:center;padding-top:6px'>{qty}</div>", unsafe_allow_html=True)
                if qcols[2].button("+", key=f"inc_{pid}"):
                    inc(pid)
                    st.rerun()
            cols[2].markdown(f"**Line total**\n\n${line:.2f}")
            with cols[3]:
                if st.button("Remove", key=f"rm_{pid}"):
                    remove(pid)
                    st.rerun()

    st.divider()
    t1, t2 = st.columns([3, 1])
    with t1:
        st.subheader(f"Subtotal: ${subtotal:.2f}")
    with t2:
        if st.button("Clear Cart", type="secondary", use_container_width=True):
            clear_cart()
            st.rerun()

    st.success("Demo checkout not implemented — this is a UI sample.", icon="✅")
