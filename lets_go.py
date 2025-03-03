import streamlit as st

def main():
    # User information
    user_info = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "profile_pic": "https://via.placeholder.com/150"
    }

    # Sidebar
    st.sidebar.image(user_info["profile_pic"], width=150)
    st.sidebar.write(f"**Name:** {user_info['name']}")
    st.sidebar.write(f"**Email:** {user_info['email']}")

    # Main content
    st.write("Welcome to the main content area!")

if __name__ == "__main__":
    main()