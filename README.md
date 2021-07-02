<div align="center">
	<br>
	<br>
	<a href="https://sindresorhus.com/caprine">
		<img src="/misc/inaction.gif" width="320">
	</a>
	<h1>Planetside Rainmeter</h1>
	<p>
		<b>A collection of rainmeter widgets to monitor your favorite game</b>
	</p>
	<br>
	<br>
	<br>
</div>

## Features

### Status for a single server
I felt that the support for multiple servers defies the role of this small widge. If you need to, you can set up two instances by duplicating the ServerStatus folder with a different name.

### States of continents
Supported states are Locked, Unstable, Stable, Alert and Unstable Alert. You can easily customize the icons for each state. Current icons were extracted from the game files.

![](/misc/states.png)

### Alert countdown
The alert countdown updates in real time. Every update cycle, the counter syncs with the remaining time from the API. 

![](/misc/feature_alert.png)

### Population distribution
Pop distibution is requested from [Fisu.pw](https://ps2.fisu.pw/) API. Last value is total players online.

![](/misc/feature_pop.png)

### Customizable refresh rate
Default refresh rate is 60 seconds. Please, keep in mind that there are 2 requests to the APIs on every update cycle. Setting a higher refresh rate **DOES NOT** help with the performance of the widget. My advice is to keep it between 1 and 5 minutes. You can see the last refresh time at the bottom.

## Requirements

* [Rainmeter](https://github.com/rainmeter/rainmeter)
* [Json Parser plugin for Rainmeter](https://github.com/e2e8/rainmeter-jsonparser)
* [Python 3.6+](https://www.python.org/downloads/)
* API key from [DBG Census API](http://census.daybreakgames.com/#devSignup)

