# crwd

## Team Members
- Audrey Deigaard / acd7@rice.edu
- Manaal Khan /  mk90@rice.edu
- Ryan Knightly / rek5@rice.edu
- Daphne Yang / dy27@rice.edu

## Pitch
Wouldn’t it be great to know how busy chaus (or any public place) is before showing up and realizing that the line is too long? To do this, we can build a system that monitors the crowdedness of a place (e.g. Rice Coffeehouse) and reports both its real time and predicted business in a simple frontend to the users. We can set up a WiFi-enabled Raspberry Pi in the place of interest that monitors how many WiFi devices are nearby. The Pi can upload this data to a backend, which would do some processing and then store it in a database. The frontend can then query this information and display it to users.

## Full Proposal
https://docs.google.com/document/d/1umKnb4pe47abechjmZ10AYvQPR0TGF1hE9PGJhB-iZY/edit?usp=sharing

# Usage


## Frontend (React App)

```bash
# Setup
cd frontend
npm install

# Test
npm run test

# Run
npm run start
```

## Backend (Flask Server)

```bash
# Setup
pip3 install -r requirements.txt

# Test
python3 -m unittest discover ./test

# Run
python3 app.py
```

The backend is deployed via heroku with: `git subtree push --prefix backend heroku main`


## Read IT Data (Python Script)

This script reads data from the GitLab provided by IT and updates the backend with new data.

```bash
# Setup
pip3 install -r requirements.txt

# Run
python3 read_IT_data.py
```
