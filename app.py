import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
st.sidebar.title("Whatsapp Chat Analyzer")

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error("⚠️ File size too large! Please upload a file smaller than 5MB.")
    elif not uploaded_file.name.endswith(".txt"):  # Check file extension
        st.error("⚠️ Invalid file type. Please upload a .txt file.")
    else:
        try:
            bytes_data = uploaded_file.getvalue()
            data = bytes_data.decode("utf-8")
            # st.text(data) # for showing data into string format
            df = preprocessor.preprocess(data)
            
            if df is not None:  # If file is valid
                st.success("✅ File uploaded and processed successfully!")
                    
                users = df['User'].unique().tolist() # stored the unique users into list 
                users.sort() # Sort the user according to ascending order
                users.insert(0, "Overall") 
                selected_user = st.sidebar.selectbox("Select User", users) 

                if st.sidebar.button("SHOW MAGIC"):

                    html_code = "<u><h1 style='color:white;text-align:center;'>Whatsapp Chat Analyzer</h1></u>"  # Adding a style for header
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    st.header("Original data", divider="gray")
                    st.dataframe(df) # for showing data into dataframe(table) format
                
                    # Statistical part
                    col1, col2, col3, col4 = st.columns(4)

                    total_msg, total_word, total_media_file, total_link = helper.show_stat(selected_user, df)

                    with col1:
                        st.header("Total message", divider="gray")
                        st.title(total_msg)
                    with col2:
                        st.header("Total word", divider="gray")
                        st.title(total_word)
                    with col3:
                        st.header("Media shared", divider="gray")
                        st.title(total_media_file)
                    with col4:
                        st.header("Total link", divider="gray")
                        st.title(total_link)

                    # Finding the most busy user from group
                    if selected_user == 'Overall':
                        col1, col2 = st.columns(2)
                        x1, x2 = helper.show_busy_user(df)

                        # show top 5 users 
                        with col1:
                            fig1, ax1 = plt.subplots(figsize=(8, 6))  # Set figure size
                            name = x1.index
                            count = x1.values
                            st.title("Most Busy Users")
                            # Bar graph
                            ax1.bar(name, count, color='skyblue')
                            ax1.set_xlabel("Users", fontsize=15)
                            ax1.tick_params(axis='x', rotation=90)
                            ax1.set_ylabel("Activity Count", fontsize=15)
                            st.pyplot(fig1)
                        # show all the users in percentage
                        with col2:
                            fig2, ax2 = plt.subplots(figsize=(8, 6))  # Set figure size
                            name = x2.index
                            count = x2.values
                            st.title("All Users Activity")
                            # Bar graph with percentages
                            ax2.bar(name, count, color='skyblue')
                            ax2.set_xlabel("Users", fontsize=15)
                            ax2.tick_params(axis='x', rotation=90)
                            ax2.set_ylabel("Percentage (%)", fontsize=15)
                            ax2.set_ylim(0, 100)
                            st.pyplot(fig2)
                    
                    # Show month wise TIMELINE analysis 
                    month_timeline = helper.show_month_timeline(selected_user, df)
                    st.title("Month Timeline")
                    fig, ax = plt.subplots(figsize=(8, 6))  # Set figure size
                    # Bar graph
                    ax.plot(month_timeline['Time'], month_timeline['Message'])
                    ax.tick_params(axis='x', rotation=90)
                    st.pyplot(fig)

                    # Show day wise TIMELINE analysis 
                    day_timeline = helper.show_day_timeline(selected_user, df)
                    st.title("Day Timeline")
                    fig, ax = plt.subplots(figsize=(8, 6))  # Set figure size
                    # Bar graph
                    ax.plot(day_timeline['Full_date'], day_timeline['Message'])
                    ax.tick_params(axis='x', rotation=90)
                    st.pyplot(fig)

                    # Show Most busy day and month wise analysis
                    html_code = "<u><h1 style='color:white;text-align:center;'>Activity Map</h1></u>"  # Adding a style for header
                    st.markdown(html_code, unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    with col1:
                        day_name_timeline = helper.show_day_name_ana(selected_user, df)
                        st.title("Most Busy Day")
                        fig, ax = plt.subplots(figsize=(8, 6))  # Set figure size
                        # Bar graph
                        ax.bar(day_name_timeline.index, day_name_timeline.values)
                        ax.tick_params(axis='x', rotation=90)
                        st.pyplot(fig)
                    with col2:
                        month_name_timeline = helper.show_month_name_ana(selected_user, df)
                        st.title("Most Busy Month")
                        fig, ax = plt.subplots(figsize=(8, 6))  # Set figure size
                        # Bar graph
                        ax.bar(month_name_timeline.index, month_name_timeline.values)
                        ax.tick_params(axis='x', rotation=90)
                        st.pyplot(fig)

                    # Show the time wise activity analysis
                    time_wise_act = helper.time_wise_active(selected_user, df)
                    st.title("Weekly Activity Map")
                    fig, ax = plt.subplots(figsize=(10, 8))  # Set figure size
                    ax = sns.heatmap(time_wise_act)
                    st.pyplot(fig)

                    # Show word cloud
                    df_wc = helper.show_word_cloud(selected_user, df)
                    if df_wc:  # Ensure word cloud is generated before displaying
                        with col1:
                            st.title("Word Cloud")
                            fig, ax = plt.subplots(figsize=(8, 6))  # Set figure size
                            ax.imshow(df_wc, interpolation='bilinear')  # Corrected function call
                            ax.axis("off")  # Hide axes
                            st.pyplot(fig)
                    else:
                        st.warning("😭 No words available to generate Word Cloud.")

                    # Show most common 20 words
                    df_most_word = helper.show_most_com_word(selected_user, df)
                    if not df_most_word.empty:  # Ensure DataFrame is not empty
                        with col2:
                            st.title("Most Common Words")
                            fig, ax = plt.subplots(figsize=(8, 6))
                            ax.barh(df_most_word["Word"], df_most_word["Count"])  # Use named columns
                            ax.set_xlabel("Count")
                            ax.set_ylabel("Words")
                            st.pyplot(fig)
                    else:
                        st.warning("😭 No common words found.")

                    # Show emoji analysis
                    df_emj = helper.show_emoji_ana(selected_user, df)
                    df_emj.rename(columns={'0': 'Emojis', '1': 'Count'}, inplace=True)
                    col1, col2 = st.columns(2)
                    if not df_emj.empty and df_emj.shape[1] >= 2:  # Ensure df_emj has at least 2 columns
                        with col1:
                            st.title("Emoji Analysis")
                            st.dataframe(df_emj, width=700, height=500) # All the emoji will display
                        with col2:
                            st.title("Top 5 Emoji Analysis")
                            fig, ax = plt.subplots(figsize=(8, 6))  # Set figure size
                            ax.pie(df_emj.iloc[:, 1].head(), labels=df_emj.iloc[:, 0].head(), autopct="%0.2f") # Top 5 emoji will display
                            st.pyplot(fig)
                    else:
                        st.warning("😭 No emoji data available for analysis.")
        except Exception as e:
            st.error(f"⚠️ Unable to read the file. Possible corruption. Error: {str(e)}")
