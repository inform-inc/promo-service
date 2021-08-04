import socket
import mysql.connector

hostname = socket.gethostname()
# print(hostname)

cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='partnerMRSSfeed')

cursor = cnx.cursor()

query = ("SELECT feedURL FROM `PartnerMRSS`" 
         "WHERE `PartnerMRSS`.`trackingGroup` = 93425 AND `isActive` = 1")

cursor.execute(query)

for (feedURL) in cursor:
    rssFeedURL = feedURL # set feedURL to rssFeedURL

cursor.close()
cnx.close()

def get_posts_details(rss=None):
	
	"""
	Take link of mrss feed as argument
	"""
	if rss is not None:
		
		# import the library only when url for feed is passed
		import feedparser # type: ignore
		
		# parsing partner feed
		partner_feed = partner_feed = feedparser.parse(rss)
		
		# getting lists of partner entries via .entries
		posts = partner_feed.entries
		# print(posts)
		# dictionary for holding posts details
		# print(partner_feed.entries[0])
		posts_details = {"Partner Title" : partner_feed.feed.title,
						"Partner Feed" : partner_feed.feed.updated}
		
		post_list = []
		
		# iterating over individual posts
		for post in posts:
			temp = dict()
			
			# if any post doesn't have information then throw error.
			try:
				temp["post_title"] = post.title
				temp["post_URL"] = post.link
				temp["post_cover_image"] = post.media_thumbnail
				# temp["author"] = post.author
				# temp["time_published"] = post.published

			except:
				pass
			
			post_list.append(temp)
		
		# storing lists of posts in the dictionary
		posts_details["posts"] = post_list
		
		return posts_details # returning the details which is dictionary
	else:
		return None

if __name__ == "__main__":
    import json
    # feed_url = "https://vaibhavkumar.hashnode.dev/rss.xml"

    # feed_url = "https://rss.politico.com/energy.xml"

    # feed_url = "https://thebright.com/feed/"
    
    print("The Feed is:{} ".format(rssFeedURL))
    # print(rssFeedURL)   

    feed_url = ''.join(rssFeedURL)
    print(feed_url)
    data = get_posts_details(rss = feed_url) # return blogs data as a dictionary
        
    if data:
        # printing as a json string with indentation level = 2
        print(json.dumps(data, indent=2))
    else:
        print("None")
