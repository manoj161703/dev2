import streamlit as st
from data import PRODUCT_MAP

# NOTE: Avoid set_page_config here for max compatibility across versions.

if "cart" not in st.session_state:
    st.session_state.cart = {}

def inc(pid: str):
    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1

def dec(pid: str):
    if pid in st.session_state.cart:
        st.session_state.cart[pid] -= 1
        if st.session_state.cart[pid] <= 0:
            del st.session_state.cart[pid]

def remove(pid: str):
    st.session_state.cart.pop(pid, None)

st.title("Your Cart")
st.caption("Adjust quantities or remove items. Use the sidebar to return to the products page.")

st.markdown("---")

cart = st.session_state.cart
if not cart:
    st.info("Your cart is empty. Open the **Mini Store** page from the sidebar and add items.", icon="ℹ️")
else:
    subtotal = 0.0
    for pid, qty in cart.items():
        p = PRODUCT_MAP.get(pid)
        if not p:
            continue
        line = p["price"] * qty
        subtotal += line

        # simple row without border=True for compatibility
        c1, c2, c3, c4 = st.columns([6, 2, 2, 2])
        with c1:
            st.markdown(f"### {p['icon']} {p['title']}")
            st.caption(f"${p['price']:.2f} each")
        with c2:
            st.markdown("**Quantity**")
            cc1, cc2, cc3 = st.columns([1, 1, 1])
            if cc1.button("−", key=f"dec_{pid}"):
                dec(pid)
                st.rerun()
            cc2.markdown(f"<div style='text-align:center;padding-top:6px'>{qty}</div>", unsafe_allow_html=True)
            if cc3.button("+", key=f"inc_{pid}"):
                inc(pid)
                st.rerun()
        with c3:
            st.markdown(f"**Line total**\n\n${line:.2f}")
        with c4:
            if st.button("Remove", key=f"rm_{pid}"):
                remove(pid)
                st.rerun()

    st.markdown("---")
    st.subheader(f"Subtotal: ${subtotal:.2f}")
    if st.button("Clear Cart"):
        st.session_state.cart = {}
        st.rerun()
