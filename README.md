# crwd


- Audrey Deigaard / acd7@rice.edu
- Manaal Khan /  mk90@rice.edu
- Ryan Knightly / rek5@rice.edu
- Daphne Yang / dy27@rice.edu
 
## The Catchy Name
crwd

## Proposal PDF
https://docs.google.com/document/d/1umKnb4pe47abechjmZ10AYvQPR0TGF1hE9PGJhB-iZY/edit?usp=sharing

## The Pitch
Wouldn’t it be great to know how busy chaus (or any public place) is before showing up and realizing that the line is too long? To do this, we can build a system that monitors the crowdedness of a place (e.g. Rice Coffeehouse) and reports both its real time and predicted business in a simple frontend to the users. We can set up a WiFi-enabled Raspberry Pi in the place of interest that monitors how many WiFi devices are nearby. The Pi can upload this data to a backend, which would do some processing and then store it in a database. The frontend can then query this information and display it to users.

## Background / Use case
As Houston’s most visited coffee shop, the world is often wondering: When’s the best time to visit Rice Coffeehouse? Our system would enable people to view both the real-time and predicted crowd levels at Coffeehouse. Fondren Library solves this problem with a digital sign showing the percentage of each floor that is occupied by students. Their data comes from the network and how many devices are connected to the various modems throughout the library. Another solution can be found in Google Maps’ “Popular Times” graph that appears for each location. Google Maps uses location data from people who have opted-in to share their location with Google.
 
## Potential obstacles and difficulties:
Not every WiFi device corresponds to a Rice Coffeehouse customer, and not every person in Coffeehouse is waiting in line. Detected devices may need to be filtered out based on various factors (signal strength, time since arrival) to provide a more useful sense of crowdedness.
What about the privacy issues of observing and storing MAC addresses? Maybe the data should be transformed in some way (hashed?) before being sent to the backend.

Data will need to be collected before the system can be tuned to accurately report 100% vs 50% vs 25% crowdedness.
We will be dealing with the physical world and hardware, which adds additional sources of problems to a purely-software system.
Rice Coffeehouse is one of the most popular spots on campus, not just for their coffee, but also for the fun hangout and study ambience. It can be very disappointing to make a plan to visit Coffeehouse, just to arrive and see that there are no empty spots and the line is out the door. We can use a small example to illustrate the utility of our app. Say that our friend Dan, who just got out of his last class early, would like to stop by Coffeehouse for an Americano and to finish some reading for his next class. He could take his chances and hope for the best that it would not be that busy, but that could be disappointing if there are too many people there. To avoid this, Dan could open up “crwd,” in order to see if Coffeehouse is currently busy, and if it is, when the next time it will be less busy is. The website shows that Coffeehouse isn’t that busy, so Dan can enjoy a successful Coffeehouse trip and finish his readings.

## Design / Attributes / Requirements
### High-level component diagram:






### UI Sketch:
![UI Sketch](/ui.jpeg)

- Scalability: More users/traffic can be handled by choosing appropriate cloud infrastructure. For example, serverless functions are designed to scale automatically, essentially removing this issue from our hands. In order to support more locations than just chaus, we can add another Raspberry Pi in each location we want to track. This will also require us to design the backend and frontend to be flexible and not make assumptions about having only one location source.
- Reliability: The backend can check if the Raspberry Pi is not producing readings and attempt to remotely restart it. We can also have a mechanism to alert the developers of such issues. There can also be a feedback form for users to submit issues with the website.
Performance: We can target allowing 500 people to use the website at once (which should not be an issue if we use appropriate hosting services). We can target a p99 latency of 150ms for queries to the backend to make sure the data loads quickly and the site is responsive.

## Security
- Authentication: Since people from outside of Rice also enjoy visiting Coffeehouse, we don’t believe that any extra authentication would be necessary for accessing the website
- Separation: The only data that will be broadcasted to the website is how busy Coffeehouse is, which is calculated based on averages and percentiles and displayed in the form of a cartoon progress bar, and how busy Coffeehouse is predicted to be everyday of the week.
- Threat model: An adversary to our model could be someone making a multitude of requests to the site, or a Coffeehouse patron showing up a large number of wifi-enabled devices.

## Implementation / Testing
What programming language(s) and tools will you use?
Frontend: TypeScript (React)
Server: TypeScript (web/JSON friendly) or Python (ML-friendly) ?
Raspberry Pi: Python
What coding style will you use: 
Object-Oriented programming, utilizing functional programming where appropriate (e.g. simple data transformations)
What tools are available to regularize indentation and formatting? 
VSCode project settings
What tools are available to check for unit test code coverage?
c8 for TypeScript, Coverage.py for Python
What tools are available to statically check for bugs (type checkers, common bug pattern checkers, etc.)?
VSCode extension to check TypeScript and Python types
What open-source libraries are available that you might build on?
https://github.com/schollz/howmanypeoplearearound
What cloud services (storage, compute, database, etc.) are available that you might build on?
Database: MongoDB (managed/hosted with Atlas)
Compute: Netlify Serverless functions or AWS lambda
How will you test your system? How will you validate that your bugs, when you fix them, won’t ever come back (“regressions”)?
Simple unit tests using:
Mock data from the Raspberry Pi
Mock data from the database
We can set up GitHub to trigger these tests on each commit. When we run into a bug, we can create a failing unit test that captures the bug (which will succeed when the bug is fixed), so we can make sure bugs don’t come back.
What tests can you run in a CI/CD system like Github Actions or locally in your development tools (i.e., running without any external network resources)?
The mocked dependencies enable testing without network connections.
What tests do you anticipate will need to run in a “real” network? How will you minimize this?
Only the end-to-end tests will require a “real” network. The rest of the tests can test components in isolation.
External partners / customers: The main users of the website would be Coffeehouse patrons, but this website’s data and displays could eventually be integrated with the existing Coffeehouse website. We may have to speak with the Coffeehouse managers to allow us to install a Raspberry Pi there for data collection, but other than that, interactions will be pretty limited.
Front-end deployment / targets: Currently, we are planning to create a mobile-friendly website.
If you’re interacting with users, how will you do it? Android/iOS? Web? What libraries will you use? Do you need unusual hardware?
The user will interact with a website, made with React. Regarding hardware, we will need a Raspberry Pi ($35) and a USB WiFi adapter with monitor mode ($50).
Back-end deployment / targets:
Atlas for a hosted MongoDB database.
Netlify for serving the website.
Netlify Serverless Functions or AWS Lambda for the backend services.
The free version should suffice for each of these services.

## Milestones
Rigged demo (Week 8):  Set up the MongoDB database and add mock data in the format the Raspberry Pi will output, query from the database, and display the data in some initial, simple form on a website.

MVP (Week 12): Have the Raspberry Pi collecting live data from Coffeehouse and feeding that data directly into the database (in a form that respects privacy), then using that data to display the real time business level on both the site. 

Final (Week 15): Include predictions for every hour of every week, and set up Raspberry Pis in other locations. Filter the data to estimate the number of people actually waiting in line vs. just how many people are in chaus. Integrate with the existing Coffeehouse website.




## Development Process
Gradual refinement: We start with a rigged demo that has major systems stubbed out or simplified, but that’s enough to get the ball rolling and you make incremental improvements to our system, while always having something that “works”.
React Site: Everyone 
Raspberry Pi: Ryan Knightly
Backend
Database queries: Daphne Yang
Predictions: Manaal Khan and Audrey Deigaard
To track work: Trello that we update when we complete a task (and review every Friday)
Each task on Trello will be assigned to the person(s) in charge of completing it
We plan to have a development branch on Github, make sure stuff works before moving the code to the main branch.

## Decision-Making / Governance
We will vote on important decisions.
