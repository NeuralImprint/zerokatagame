import streamlit as st
st.set_page_config(page_title="Zero-Kata", layout="centered")

import numpy as np
import random
from sklearn.tree import DecisionTreeClassifier

@st.cache_data
def train():
    X, y = [], []
    for _ in range(1000):
        b = [0]*9
        mv = list(range(9))
        p = 1
        for _ in range(9):
            if not mv: break
            m = random.choice(mv)
            b[m] = p
            mv.remove(m)
            X.append(b.copy())
            y.append(m)
            p *= -1
    clf = DecisionTreeClassifier()
    clf.fit(np.array(X), np.array(y))
    return clf

clf = train()
wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
sym = {1: 'X', -1: 'O', 0: ' '}

def check(b):
    for a, b_, c in wins:
        if b[a] == b[b_] == b[c] != 0:
            return b[a]
    if 0 not in b: return 0
    return None

def block(b):
    for a, b_, c in wins:
        line = [b[a], b[b_], b[c]]
        if line.count(-1) == 2 and line.count(0) == 1:
            if b[a] == 0: return a
            if b[b_] == 0: return b_
            if b[c] == 0: return c
    return None

def ai(b):
    for a, b_, c in wins:
        line = [b[a], b[b_], b[c]]
        if line.count(1) == 2 and line.count(0) == 1:
            if b[a] == 0: return a
            if b[b_] == 0: return b_
            if b[c] == 0: return c
    bl = block(b)
    if bl is not None: return bl
    pred = clf.predict([b])[0]
    if b[pred] == 0: return pred
    avail = [i for i, v in enumerate(b) if v == 0]
    return random.choice(avail)

st.title("Tic-Tac-Toe")
st.markdown("""
### Welcome to the Tic-Tac-Toe (जीरो काटा) game
You play with 0 and the machine plays with X.
""")


if "b" not in st.session_state:
    st.session_state.b = [0]*9
    st.session_state.over = False
    st.session_state.msg = "lets goooo!"

def reset():
    st.session_state.b = [0]*9
    st.session_state.over = False
    st.session_state.msg = "lets goooo!"

def move(p):
    if st.session_state.over or st.session_state.b[p] != 0: return
    st.session_state.b[p] = -1
    w = check(st.session_state.b)
    if w is not None:
        st.session_state.over = True
        st.session_state.msg = "You Won" if w == -1 else ("Bad luck, you lost" if w == 1 else "Its a draw")
        return
    bot = ai(st.session_state.b)
    st.session_state.b[bot] = 1
    w = check(st.session_state.b)
    if w is not None:
        st.session_state.over = True
        st.session_state.msg = "You Won" if w == -1 else ("Bad luck, you lost" if w == 1 else "Its a draw")
    else:
        st.session_state.msg = "lets goooo!"

cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        if st.button(sym[st.session_state.b[i]], key=f"c_{i}", use_container_width=True):
            if not st.session_state.over and st.session_state.b[i] == 0:
                move(i)

st.markdown(f"### {st.session_state.msg}")
st.divider()
st.button("Restart", on_click=reset)
