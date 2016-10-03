import os
import sys
import random
import mechanize
import time
import string


# Mechanize browser and set user agent
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('user-agent', '  Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3'),
('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]


def login():
	print "[+]Logging in."
	
	try:
		br.open("http://www.exampleforums.org/forums/login.php?do=login")
    	except Exception as e:
    		print "\nCould not open target URL, please reference the error message below: "
    		print 
    		print e
    		
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
	while True:
		try:
			random_url = "http://www.exampleforums.org/forums/operating-systems/linux-1" + digit_generator(5, "0987654321") + ".html"
			print
			print "[+]Selected URL:" 
			print
			print random_url

			br.open(random_url)
			
			# Reset 'random_url' value to null
			random_url = ""
			
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
		print "\n[!]CTRL+C Caught, quitting"
		break
		time.sleep(2)
		sys.exit(0)
		

						
login()
