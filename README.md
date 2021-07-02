# Planetside Rainmeter

![](/misc/inaction.gif)

## Features

#### Status for a single server
#### States of continents
Supported states are Locked, Unstable, Stable, Alert and Unstable Alert. You can easily customize the icons for each state. Current icons were extracted from the game files.

![](/misc/states.png)

#### Alert counшdown
The alert countdown updates in real time. Every update cycle, the conuter syncs with the remaining time from the API. 

![](/misc/feature_alert.png)

#### Population distribution
Pop distibution is requested from [Fisu.pw](https://ps2.fisu.pw/) API

![](/misc/feature_pop.png)

####Customizable refresh rate (Default: 60s)
Please, keep in mind that there are 2 requests to the APIs on every update cycle. Setting a higher refresh rate **DOES NOT** help with the performance of the widget. My advice is to keep it between 1 and 5 minutes.

## Requirements

* [Rainmeter](https://github.com/rainmeter/rainmeter)
* [Json Parser plugin for Rainmeter](https://github.com/e2e8/rainmeter-jsonparser)
* [Python 3.6+](https://www.python.org/downloads/)
* API key from [DBG Census API](http://census.daybreakgames.com/#devSignup)

