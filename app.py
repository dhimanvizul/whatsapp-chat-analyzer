import streamlit as st
import preprocessor, fetch_stats
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('Group_Notification')
    user_list.sort(reverse=True)
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox('User List', user_list)

    if st.sidebar.button('Show Analysis'):
        st.title('Top Statistics')
        num_msg, words_cnt, media, urls = fetch_stats.fetch(selected_user, df)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.header('Total Messages')
            st.title(num_msg)
        with c2:
            st.header('Total Words')
            st.title(words_cnt)
        with c3:
            st.header('Total Media')
            st.title(media)
        with c4:
            st.header('Total Links shared')
            st.title(urls)

        # monthly timeline
        st.header('Monthly Timeline')
        timeline = fetch_stats.monthly_timeline(selected_user, df)
        fig, axes = plt.subplots()
        sns.pointplot(data=timeline, x='time', y='message', color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.header('Daily Timeline')
        daily_time = fetch_stats.daily_timeline(selected_user, df)
        fig, axes = plt.subplots()
        sns.pointplot(data=daily_time, x='full_date', y='message', color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        c9, c10 = st.columns(2)
        with c9:
            st.header('Week Activity')
            week_activity = fetch_stats.week_activity(selected_user, df)
            fig, axes = plt.subplots()
            sns.barplot(data=week_activity, x='day_name', y='message', color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with c10:
            st.header('Month Activity')
            month_activity = fetch_stats.month_activity(selected_user, df)
            fig, axes = plt.subplots()
            sns.barplot(data=month_activity, x='month_name', y='message', color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            msg, busy_user, new_df = fetch_stats.fetch_busy_user(df)
            fig, axes = plt.subplots()

            c5, c6 = st.columns(2)
            with c5:
                sns.barplot(x=msg, y=busy_user)
                # axes.bar(msg, busy_user)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with c6:
                st.dataframe(new_df)

        st.title('Most Common Words')
        wc_img = fetch_stats.create_wordcloud(selected_user, df)
        fig, axes = plt.subplots()
        axes.imshow(wc_img)
        st.pyplot(fig)

        most_common_word_df = fetch_stats.most_common_words(selected_user, df)
        fig, axes = plt.subplots()
        sns.barplot(data=most_common_word_df, x=most_common_word_df[0], y=most_common_word_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # st.dataframe(most_common_word_df)

        emoji_df = fetch_stats.fetch_emoji(selected_user, df)
        st.title('Emoji Analysis')
        fig, axes = plt.subplots()
        col7, col8 = st.columns(2)
        with col7:
            st.dataframe(emoji_df)
        with col8:
            if emoji_df.shape[0] == 0:
                plt.pie(x=[100], colors='white')
                st.pyplot(fig)
            else:
                # color = sns.color_palette('pastel')
                plt.pie(x=emoji_df[1], labels=emoji_df[0], autopct='%0.2f')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

        # user heatmap
        st.title('User Heatmap')
        heatmap = fetch_stats.activity_heatmap(selected_user, df)
        plt.figure(figsize=(11, 4))
        sns.heatmap(heatmap)
        plt.xticks(rotation='vertical')
        st.pyplot(plt)
