import pandas as pd
import emoji
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter

extractor = URLExtract()


def fetch(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    urls = df['message'].apply(lambda x: extractor.find_urls(x))
    urls = [x for x in urls if x != []]

    num_msg = df.shape[0]
    words = []
    for msg in df['message']:
        words.extend(msg.split())
    media = df[df['message'] == '<Media omitted>\n'].shape[0]

    return num_msg, len(words), media, len(urls)


def fetch_busy_user(df):
    busy_user = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return busy_user.index, busy_user.values, new_df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    img_wc = wc.generate(df['message'].str.cat(sep=" "))
    return img_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    rm_grp_ntf = df[df['user'] != 'Group_Notification']
    rm_grp_ntf = df[df['message'] != '<Media omitted>\n']

    file = open('stop_words_hinglish.txt', 'r')
    stop_words = file.read()
    file.close()

    words = []
    for msg in rm_grp_ntf['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(20))


def fetch_emoji(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_name', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_time = df.groupby(['full_date']).count()['message'].reset_index()
    return daily_time


def week_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.groupby(['day_name']).count()['message'].reset_index()


def month_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.groupby(['month_name']).count()['message'].reset_index()


def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    pvt = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return pvt
