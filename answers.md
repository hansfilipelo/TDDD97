# Answers TDDD97

## Lab 1

**Why do we validate data before sending it to the server at client­side, as opposed to just letting
the server validate data before using it? What we get and what we lose by it?**

Speed. Validating before sending allows for shorter response times, and lesser server load in case something is wrong (for security reasons one should still validate a lot of things in the server though). 

**How secure is the system using an access token to authenticate? Is there any way to circumvent
it and get access to private data?**

In case there aren't any SQL-injection-possibilities (which there "always" are) and the token is managed to be kept secure (for example using HTTPS), the token system should be secure enough as long as the token isn't guessable. 

**What would happen if a user were to post a message containing JavaScript­code? Would the
code be executed? How can it oppose a threat to the system? What would the counter measure?**

--

**What happens when we use the back/forward buttons while working with Twidder ? Is this the expected behaviour? Why are we getting this behaviour? What would be the solution?**

We go back outside of the application since Twidder is, by specification, a single-page website. The solution for a single-page website would be to use javascript to create client routes that correspond to server routes. 

**What happens when the user refreshes the page while working with Twidder ? Is this the expected behaviour? Why are we getting this behaviour?**

The user logs out, again since Twidder is a single-page-app. 

**Is it a good idea to read views from the server instead of embedding them inside of the “client.html”? What are the advantages and disadvantages of it comparing to the current
approach?**

Embedding views in the client is faster and makes for a more "native-like" experience. Fetching views from the server means longer response time but would not have troubles with the forward/backward buttons. 

**Is it a good idea to return true or false to state if an operation has gone wrong at the server­side or not? How can it be improved?**

True and false are of a boolean data-type. It would be better to return an error code to the client. 

**Is it reliable to perform data validation at client­side? If so please explain how and if not what would be the solution to improve it?**

No it is not reliable to do validation ONLY in the client side since a client made by anyone can connect to a HTTP-server running the server app, and then send "crappy data" to the server. 

**Why isn’t it a good idea to use tablesfor layout purposes? What would be the replacement?** 

CSS flexbox is a replacement for tables. 

**How do you think Single Page Applications can contribute to the future of the web? What is their advantages and disadvantages from usage and development point of views?**

Single-page application is often used as a plattform independent way to reach many users using a single code base. I think that's their future. 

Advantages: Responsiveness and possibilities for more rich desktop-grade applications (for example using WebSockets).

Disadvantages: Non-regular browsing behaviour, large download at first page-hit and often not preferrable on slow connections. 


## Lab 2

**What security risks can storing passwords in plain text cause? How can this problem be addressed programmatically?**

In case someone gets a hold of the database, that someone has all the users passwords (which might be same for that users GMail account as an example). 

Hashing + salt is one solution, another is to user external identification for your webapp (Google, Facebook, BankID etc). 

**As http requests and responses are text­based information, they can be easily intercepted and read by a third­party on the Internet. Please explain how this problem has been solved in real­world
scenarios**

They have been solved by Diffie-Helmann key exchange through HTTPS (today HTTP over TLS). 

**How can we use Flask for implementing multi­page web applications? Please explain how Flask templates can help us on the way?**

Flask templates allows us to use a single template-style with different content. Most content management systems, blogging system and server side technologies allows for this. 

**Do you think the Telnet client is a good tool for testing server­side procedures? What are its possible shortages?**

The testing process becomes ridiculously slow. I used Postman instead which generate HTTP-requests and where I can save parameters. 


## Lab 3

**XML is also used as another widely used data exchange format. please have a comparison between the two and pinpoint the differences and similarities. Would you still use JSON over
XML or not?**

XML is a markup language, much like HTML. XML is more powerful and often used in enterprise applications (as the financial XBRL subset for example). 

JSON uses less data for meta-information and have better collection of parsers. JSON is therefore today more widely deployed. 

I would prefer JSON if implementing a Web API. 

**Is it possible to have two way communication without using WebSocket protocol? Please elaborate your answer.**

Not through a browser that I know of, unless the client is also a server - then you can use regular TCP sockets. 

**What is REST architectural style? Is our Twidder web application based on REST architecture? Please elaborate your answer.**

I'd say that Twidder is REST. It's quite simple and uses a client-server model (which is one of the models under REST) and a JSON interface. 

**What does web application deployment mean? What pieces of information do you think a web server needs to run a web application?**

A web server needs an HTTP-server to deliver a web application. There are web applications (entire CMSes) running entirely on the client using JavaScript. 

Most web apps however need an HTTP- and an App-server delivering dynamic content. 

**Please mention and explain three real world functionalities which require two way client-­server communication to be implemented. Is it possible to implement them without two way communication? how?**

1. Realtime chat application (think Facebook Messenger)
2. Realtime game (think Agar.io)
3. Realtime video chat (Google Hangouts)

The chat application could probably be implemented using client-side polling but it would be much less efficient. 
