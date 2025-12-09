import streamlit as st
import os
from PIL import Image
import pandas as pd

# Initialize session state
if "frameidx" not in st.session_state:
    st.session_state.frameidx = 0
if "df" not in st.session_state:
    # Load existing CSV if exists, else create empty
    if os.path.exists("evalOutput.csv"):
        st.session_state.df = pd.read_csv("evalOutput.csv")
    else:
        st.session_state.df = pd.DataFrame(columns=["name","falsePositive","truePositive"])

# Directory containing frames
directory = "frames"
image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif")

# Get all image file paths
image_paths = sorted([os.path.join(directory, f) for f in os.listdir(directory)
                      if f.lower().endswith(image_extensions) and os.path.isfile(os.path.join(directory, f))])

# Ensure frameidx is within bounds
st.session_state.frameidx = max(0, min(st.session_state.frameidx, len(image_paths)-1))
image_path = image_paths[st.session_state.frameidx]
image_name = os.path.basename(image_path)

# Display current frame
st.image(image_path, caption=f"{image_name} ({st.session_state.frameidx+1}/{len(image_paths)})", use_container_width=True)

# Function to add/update label for the current frame only
def label_frame(false_pos, true_pos):
    # Drop only the row with the same frame name
    st.session_state.df = st.session_state.df[st.session_state.df["name"] != image_name]
    # Add new label
    st.session_state.df.loc[len(st.session_state.df)] = [image_name, false_pos, true_pos]
    # Save CSV
    st.session_state.df.to_csv("evalOutput.csv", index=False)

# Navigation buttons
nav_col1, nav_col2, nav_col3 = st.columns([1,6,1])
with nav_col1:
    if st.button("⬅ Prev") and st.session_state.frameidx > 0:
        st.session_state.frameidx -= 1
with nav_col3:
    if st.button("Next ➡") and st.session_state.frameidx < len(image_paths)-1:
        st.session_state.frameidx += 1

# Label buttons
label_col1, label_col2, label_col3 = st.columns([1,1,1])
with label_col1:
    if st.button("False Positive ❌"):
        label_frame(True, False)
        # auto next frame
        if st.session_state.frameidx < len(image_paths)-1:
            st.session_state.frameidx += 1
with label_col3:
    if st.button("True Positive ✅"):
        label_frame(False, True)
        # auto next frame
        if st.session_state.frameidx < len(image_paths)-1:
            st.session_state.frameidx += 1

# Show labeled DataFrame
st.write(st.session_state.df)
