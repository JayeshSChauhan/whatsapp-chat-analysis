from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

# Function will show the statistic part of data
def show_stat(selected_user, df):
    if selected_user != 'Overall':
        df = df[selected_user == df['User']]

    # 1. show the total number of message(chat) done into group/individual
    total_msg = df.shape[0]

    # 2. show the total number of words by group/individual
    total_word_list = []
    for msg in df['Message']:
        total_word_list.extend(msg.split()) # stored words into total_word list
    total_word = len(total_word_list)

    # 3. show the total number of media omitted file(video/image file)
    total_media_file = df[df['Message'] == '<Media omitted>'].shape[0]

    # 4. Show the total number of links
    link_list = []
    extractor = URLExtract()
    for msg in df['Message']:
        link_list.extend(extractor.find_urls(msg))
    link = len(link_list)

    return total_msg, total_word, total_media_file, link

# Function will show the most busy user
def show_busy_user(df):
    x1 = df['User'].value_counts().head() # show top 5 users 
    x2 = (df['User'].value_counts()/df.shape[0])*100 # show all the users in percentage
    return x1, x2.round(2)

# Function will show word cloud
def show_word_cloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[selected_user == df['User']]

    temp_df = df[df['User'] != 'Group_notification'] # will not count Group_notification's words as word cloud
    temp_df = temp_df[temp_df['Message'] != '<Media omitted>'] # will not count <Media omitted> message as word cloud
    # below words are also not count as word cloud
    f = open('stop_hinglish.txt')
    stop_word = f.read()

    def remove_stop_word(msg):
        word_cloud_list = []
        for wd in msg.lower().split():
            if wd not in stop_word:
                word_cloud_list.append(wd)
        return " ".join(word_cloud_list)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    
    temp_df['Message'] = temp_df['Message'].apply(remove_stop_word)
    df_wc = wc.generate(temp_df['Message'].str.cat(sep = " "))
    return df_wc

# Function will show msot common word
def show_most_com_word(selected_user, df):
    if selected_user != 'Overall':
        df = df[selected_user == df['User']]
    
    temp_df = df[df['User'] != 'Group_notification'] # will not count Group_notification's words as most common word
    temp_df = temp_df[temp_df['Message'] != '<Media omitted>'] # will not count <Media omitted> message as most common word
    # below words are also not count as most common word
    f = open('stop_hinglish.txt')
    stop_word = f.read()

    word_list = []
    for msg in temp_df['Message']:
        for wd in msg.lower().split():
            if wd not in stop_word:
                word_list.append(wd)

    most_word = pd.DataFrame(Counter(word_list).most_common(15)) # fetch most 20 words
    return most_word

# Function will show emoji analysis
def show_emoji_ana(selected_user, df):
    if selected_user != 'Overall':
        df = df[selected_user == df['User']]

    emoji_list = []
    for msg in df['Message']:
        emoji_list.extend([c for c in msg if c in emoji.EMOJI_DATA])
    emj = pd.DataFrame(Counter(emoji_list).most_common(len(Counter(emoji_list)))) # fetch all the emoji which is used
    return emj

def show_month_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[selected_user == df['User']]

    timeline = df.groupby(['Year', 'Month_name', 'Month']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month_name'][i] + "-" + str(timeline['Year'][i]))
    timeline['Time'] = time
    return timeline

def show_day_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[selected_user == df['User']]

    timeline = df.groupby(df['Full_date']).count()['Message'].reset_index()
    return timeline

def show_day_name_ana(selected_user, df):
    if selected_user != 'Overall':
        df = df[selected_user == df['User']]

    day_timeline = df['Day_name'].value_counts()
    return day_timeline

def show_month_name_ana(selected_user, df):
    if selected_user != 'Overall':
        df = df[selected_user == df['User']]

    month_timeline = df['Month_name'].value_counts()
    return month_timeline

def time_wise_active(selected_user, df):
    if selected_user != 'Overall':
        df = df[selected_user == df['User']]
    
    active_graph = df.pivot_table(index='Day_name', columns='Period', values='Message', aggfunc='count').fillna(0)
    return active_graph