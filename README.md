# Capstone Project: Sustainable Travel in Europe
This repository contains the capstone project for the spring term 2026 course "Practical Data Science: Tools for Social Good". It is an interactive Streamlit app to compare rail and air travel on more than 40 routes across Europe, enabling analysis of the competitiveness of trains based on different assumptions.

## Idea behind the project
Transport accounts for roughly a fifth of global carbon dioxide emissions (1). Many environmentally conscious people therefore want to travel by train rather than take the airplane, especially for intra-continental trips. However, trains often appear quite slow and expensive compared to cheap airline offerings. Consequently, on an individual level, air travel sometimes wins, even if it is the environmentally worse choice.
Yet, how often do we not take into account the additional time spent at the airport when flying somewhere? And the remote location of many airports? Does this change the calculation of which means of transport is more practical?
And even further, what if we take into account the price we pay for the carbon emissions? Not the cost to compensate a flight via a compensation provider, but the price we pay as society for the future damages caused by climate change (social cost of carbon)?
These considerations gave rise to the idea to simulate different scenarios in an interactive app, to analyse in what distances rail travel is competitive, and how much carbon dioxide emissions could be saved.

## Practical use cases
One could play around with parameters when planning a trip to compare time and price differences.
But more importantly, the analysis illustrates clearly that, even if train is the environmentally better choice, trains are still slower AND more expensive at the same time compared to planes. This highlights the urgency for policymakers to actually make trains the more practical option for travellers. It also helps to find best practices. 

## Data Sources
This dataset was manually collected from Rome2Rio following a standardised rule. City pairs were chosen arbitrarily according to personal interest. Air distances were retrieved from distance.to.org.

- All fares for 14 July 2026 (as if booking a trip 3 months in advance)
- Cheapest direct connection. Consider only high-speed rail.
- All travel times must be between 6am and 10pm
- If only price span was available, look price up on train operator's website, else use the average of the price span.

- Standard value for social cost of carbon was retrieved from: *A new way to price carbon: Understanding the social cost of carbon by Christoph Hambel Ton van den Bremer Frederick van der Ploeg, 2024, CEPR*
- Standard emissions per kilometer for air and rail travel were retrieved from: *“Data Page: Carbon footprint of travel per kilometer”. Our World in Data (2026). Data adapted from UK Government, Department for Energy Security and Net Zero. Retrieved from https://archive.ourworldindata.org/20260304-094028/grapher/carbon-footprint-travel-mode.html [online resource] (archived on March 4, 2026).*

## Making of the project
1. Data Collection
2. Data Cleaning and Exploration
3. Creation of Visuals and a Model to find a Threshold
4. Import and transform main elements to create Streamlit App

## Features of the interactive app
- Interactive sliders for assumptions
- Route-level comparisons
- Distance-level comparisons
- Price vs. Time differences across routes
- Threshold model for when rail becomes better
- Emission saving potential for routes where air wins by slim margin
  
## Limitations
1. The underlying dataset represents one point in time and a limited number of routes. The same analysis could be expanded on a larger data collection, fetched for example through an API. For the current project, this option was not available, since the respective APIs (for example by Rome2Rio) are a paid service.
2. Several simplifications had to be made during data collection: Only air distance was used for distance calculations, so actual rail distance detours due to geography were not considered. Only the main airport was considered even if several airports were available in one location. 
3. In practice, travellers have more discretion than represented in the model where only one train journey was compared with one plane journey for a given route. For example, one may be much more flexible to pay more for a faster route, or travel at a more unconventional time or accept a number of stops. At the same time, the "cheapest" route found may not always be feasible for the traveler.
   
## References
(1) Hannah Ritchie (2020) - “Cars, planes, trains: where do CO₂ emissions from transport come from?” Published online at OurWorldinData.org. Retrieved from: 'https://archive.ourworldindata.org/20251125-173858/co2-emissions-from-transport.html' [Online Resource] (archived on November 25, 2025).
