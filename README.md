- [Introduction and motivation](#introduction-and-motivation)
- [Supreme Shop Bot](#supreme-shop-bot)
- [Limitations](#limitations)
- [Sofware Requirements](#sofware-requirements)

# Introduction and motivation
Supreme is one of the most famous streetfashion brand in the world. Their marketing strategy is based on weekly drops of rare clothes editions collaborating with another well known brands such as Nothface, Nike, etc ... so much so that they have created a "Drop culture" with a huge community of fans and an active resell market. 

This active reselling market has attracted some buyers who are just interested in making money in the resell market, closing to the fans the opportunity to buy this products. We can see it every week during the drops, where some products turn sold out in just a few seconds, that is due to the huge amount of bots performing purchases to resell the products for two of three times their price.

It is not a problem if every one has the opportunity to use a bot, but it fact, not every one has the technical skills to develop their own bot, so, this is the origin of this project: the democratization of the bots to make the market more fair.

# Supreme Shop Bot
Here you will find a bot implemented to perform purchases on supreme official page based on the droplists published by supremecommunity.com. The implementation is based on Selenium library (Python) and it has a GUI to interact with the bot without need to code anything. I intend to develop GUI to be user friendly with a complete guide which describes the installation and how to use it.

# Limitations
There are some limitations that you have to keep in mind if you are planning to use this bot:

1. The product list which is included as a purchase option is the latest drop list published in https://www.supremecommunity.com, so, you should visit the page and check the latest droplist to ensure what are you going to buy with the bot. I thought that has no sense to automate a purchase for a product released weeks ago, you can do it by yourself.

2. The Supreme shop usually crashes during the drops and, even though the bot is prepared for that and he will restart the process if the servers are busy, it could result in a failed purchase.

3. The speed of the bot depends directly of your internet speed, it has been developed with a connection of 500 mb/s with good results (he can arrive to the payment stage in less than 4 seconds), but the performance can be slower due to the connection speed, so, you should try to have the best connection as possible during the purchases.

4. The bot is implemented to pay only with a Paypal account, the reason is because the usual banks have a double step verification which forces you to wait a sms to verify the purchase and it can take a few minutes, so definetly, a log in in Paypal is faster than credit card verifications.

5. The Supreme shop has an antibot service (reCAPTCHA v3 by Google) which is very difficult to bypass if you do not have a proper VPN service working (the usual VPN services probably will fail to hid you because between the huge number of bots there may be a lot of them which are using these VPN). So, as a simple solution, I have included a Chrome extension https://anti-captcha.com/mainpage which works fine avoiding the bot detector, it solves the challenges in less than a minute (usually in a few seconds) and he can bypass recaptcha v3 too. Definetly, I recommend you to use this service during the purchases but it is not mandatory and the bot works without this service, but I can not ensure a succesful purchase without this service yet. 

NOTE: I am working in a VPN solution for this problem.

# Sofware Requirements
