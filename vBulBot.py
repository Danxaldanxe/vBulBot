import os
import sys
import random
import mechanize
import time
import string

useragents = [
 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
 "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)",
 "Googlebot/2.1 (http://www.googlebot.com/bot.html)",
 "Opera/9.20 (Windows NT 6.0; U; en)",
 "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)",
 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)",
 "Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0",
 "Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
 "Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)", # maybe not
 "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13"
 "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)",
 "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)",
 "Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)",
 "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)",
 "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8",
 "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
 "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
 "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
 "YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)"
 ]


# Mechanize browser and set user agent
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = random.choice(useragents)


def login():
	print "[+]Logging in."
	
	br.open("http://www.exampleforums.org/forums/login.php?do=login")
    
	# Select first form(login form) and set values to the credentials -
	# of the account made in advance for spamming purposes
	br.form = list(br.forms())[0]
	br["vb_login_username"] = "username"
	br["vb_login_password"] = "password"
   
	# Submit values for username and password fields
	response = br.submit()

	print "\n[+]Response:"
	print
	print response
	print 
	print "[+]Selecting random URL by page/thread ID"
	
	# Call function to start posting
	post()

	
# Function to generate a random string of digits to replace the original page/thread ID 
def digit_generator(size=5, chars=string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

	
def post():	
	try:
		while True:
			random_url = "http://www.exampleforums.org/forums/operating-systems/linux-1" + digit_generator(5, "0987654321") + ".html"
			print
			print "[+]Selected URL:" 
			print
			print random_url

			br.open(random_url)

			# Select 'vbform' which is the name of the quick reply form - 
			# if not present we've either been banned or are otherwise - 
			# unable to post in this thread
			try:
				br.select_form("vbform")
			except:
				print "\n[!]Could not find quick reply form. Unable to post on page"
				print "\n[+]Consider inspecting selected URL manually in your browser"
		
				choice = raw_input("Retry? Y/n: ")
		
				if "y" in choice:
					print "\nRetrying"
					login()
				elif "n" in choice:
					print "\nQuitting"
					break
				else:
					print "\nUnhandled option, quitting"
					break
	
			print "\nPosting message"
	
			# Message to spam
			br["message"] = "Spam goes here"
	
			# Set values for checkbox control where needed
			try:
				br[quickreply] = 1
				br[forcepost] = 1
			except:
				pass
	
			response = br.submit()
	
			print "\n[+]Response: "
			print
			print response
			print
			print "[+]Message was posted succesfully"
		
	# Handle CTRL+C
	except KeyboardInterrupt:
		print "[!]CTRL+C Caught, quitting"
		sys.exit(0)
						
login()
