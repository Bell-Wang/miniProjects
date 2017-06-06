# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import datetime

with open("/Users/bella/Downloads/twitter_classifier_training_data.json") as file:
    my_json= file.readlines()

dict_list_tw =[json.loads(i) for i in my_json]
target_list_tw = [i for i in dict_list_tw if i.get('label')==1]


with open("/Users/bella/Downloads/instagram_classifier_training_data.json") as file2:
    my_json2= file2.readlines()

dict_list_in =[json.loads(i) for i in my_json2]
target_list_in = [i for i in dict_list_in if i.get('label')==1]

'''
target_list
target_list_in
in_l = [i.get('_id') for i in target_list_in0]
tw_l = [i.get('_id') for i in target_list0]

in_ll=[i['$oid'] for i in in_l]
tw_ll=[i['$oid'] for i in tw_l]

intersect = [i for i in tw_ll if i in in_ll]
'''

def tweet():
    my_event_tweet = list()
    
    for i in target_list_tw:
        oid = i.get('_id')
        oid = oid.get('$oid')
        
        tweet = i.get('tweets')
        tweet_cnt = len(tweet)
        tweet_ent = [s.get('entities') for s in tweet]
        
        hashtag_list = list()
        mention_list = list()
        for ss in tweet_ent:
            if len(ss.get('hashtags')) != 0:
                for sss in ss.get('hashtags'):
                    hashtag_list.append(sss.get('text'))
            if len(ss.get('user_mentions')) != 0:
                for sss in ss.get('user_mentions'):
                    mention_list.append(sss.get('name'))
                    
        favor_cnt = sum([s.get('favorite_count') for s in tweet])
        favor_t_cnt = sum([1 for s in tweet if s.get('favorited') == True])
        retweet_cnt = sum([s.get('retweet_count') for s in tweet])
        retweet_t_cnt = sum([1 for s in tweet if s.get('retweeted') == True])
    
        tw_list = list()
        for t in tweet:
            tw_list.append(t.get('text'))
    
    	i_dict = {
        'oid' : oid,
        'tweet_cnt' : tweet_cnt,
        'tweets' : tw_list,
        'hashtags' : hashtag_list,
        'user_mentions' : mention_list,
        'favor_cnt' : favor_cnt,
        'favor_t_cnt' : favor_t_cnt,
        'retweet_cnt' : retweet_cnt,
        'retweet_t_cnt' : retweet_t_cnt
    	}
        #[{i_dict0},{i_dict1}...]
        my_event_tweet.insert(len(my_event_tweet), i_dict)
    return my_event_tweet


def instagram():
    my_event_inst = list()
    
    for i in target_list_in:
        oid = i.get('_id')
        oid = oid.get('$oid')
        
        insta = i.get('photos')
        inst_cnt = len(insta)
        
        inst_list = list()
        comment_list = list()
        tag_list = list()
        comment_cnt = 0
        like_cnt = 0

        for t in insta:
            tmp_comment_list = list()
            
            try:               
                tt_capt =  t.get('caption')
                inst_list.append(tt_capt.get('text'))
            
                tt_comment =  t.get('comments')
                comment_cnt += tt_comment.get('count')
            
                if tt_comment.get('count') != 0:
                    for ss in tt_comment.get('data'):
                        tmp_comment_list.append(ss.get('text'))           
                        comment_list.extend(tmp_comment_list)
            
                tt_like = t.get('likes')
                like_cnt += tt_like.get('count')
                tag_list.extend(t.get('tags'))
            except:
                pass
        
        i_dict = {
        'oid' : oid,
        'inst_cnt' : inst_cnt,
        'inst' : inst_list,
        'comment_cnt' : comment_cnt,
        'comment' : comment_list,
        'like_cnt' : like_cnt,
        'tag' : tag_list
                }         
        my_event_inst.insert(len(my_event_inst), i_dict)
    return my_event_inst
            
def inst_viz():
    my_event_inst_viz = list()
    
    for i in target_list_in:
        oid = i.get('_id')
        oid = oid.get('$oid')
        
        insta = i.get('photos')
        
        for t in insta:            
            try:
                tt_capt = t.get('caption')
                text = tt_capt.get('text')
                
            except:
                text = 'image post'
                
            oid = oid
            mid_lat = t.get('mid_lat')
            mid_lng = t.get('mid_lng')
            post_time = datetime.datetime.fromtimestamp(float(t.get('created_time'))).strftime("%Y-%m-%d %H:%M:%S")         
          
            i_dict = {
                        'oid' : oid,
                        'mid_lat' : mid_lat,
                        'mid_lng' : mid_lng,
                        'created_time' : post_time,
                        'text' : text
                     }     
            my_event_inst_viz.insert(len(my_event_inst_viz), i_dict)
          
    return my_event_inst_viz
            


