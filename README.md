# crwd.

A real-time source of how busy Rice Coffeehouse is.

**Visit at [bit.ly/chauscrowd](https://bit.ly/chauscrowd)**

## Team Members
- Audrey Deigaard / acd7@rice.edu
- Manaal Khan /  mk90@rice.edu
- Ryan Knightly / rek5@rice.edu
- Daphne Yang / dy27@rice.edu

## Pitch
Wouldn’t it be great to know how busy chaus (or any public place) is before showing up and realizing that the line is too long? To do this, we can build a system that monitors the crowdedness of a place (e.g. Rice Coffeehouse) and reports both its real time and predicted business in a simple frontend to the users. 

## Full Proposal
https://docs.google.com/document/d/1umKnb4pe47abechjmZ10AYvQPR0TGF1hE9PGJhB-iZY/edit?usp=sharing


# Usage

## Frontend (React App)

```bash
# Setup
cd frontend
npm install

# Run
npm run start
```

The frontend is deployed as a static web-app via Netlify. 
Visit the site here: https://chauscrowd.netlify.app/

## Backend (Flask Server)

```bash
# Setup
pip3 install -r requirements.txt

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
