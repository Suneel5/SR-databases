import pandas as pd

df1=pd.read_csv('posts_url/links.csv')
df2=pd.read_csv('posts_url/links_.csv')

df= pd.concat([df1, df2], ignore_index=True)

#remove duplicates post id
final_df = df.drop_duplicates(subset='postid')
final_df.to_csv('posts_url/links.csv', index=False)