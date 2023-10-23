import json
from flask import Flask,render_template,request,redirect,flash,url_for


MAXIMUM_BOOKING_PER_CLUB = 12


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def add_places_booked_field_to_competition(competitions, clubs):
    """Add 'places_booked' field in competitions to
    keep track of clubs booking history
    """
    for competition in competitions:
        if not competition.get('places_booked', None):
            competition['places_booked'] = {
                club['name']: 0 for club in clubs
            }


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
add_places_booked_field_to_competition(competitions, clubs)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except IndexError:
        error = "Sorry, that email was not found."
        if not request.form['email']:
            error = "Please, enter an email adress to continue"
        return render_template('index.html', error=error), 400
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        ), 400
    places_booked = foundCompetition['places_booked'][foundClub['name']]
    if foundClub and foundCompetition:
        return render_template(
            'booking.html',
            club=foundClub,
            competition=foundCompetition,
            max_booking_per_club=MAXIMUM_BOOKING_PER_CLUB,
            places_booked=places_booked,
            maximum_booking=min(
                int(foundClub['points']),
                int(foundCompetition['numberOfPlaces']),
                MAXIMUM_BOOKING_PER_CLUB - places_booked
            )
        )


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    error = None
    places_booked = competition['places_booked'][club['name']]
    if not request.form['places'] or int(request.form['places']) <= 0:
        error = 'You must enter a positive number of places to book them.'
    else:
        placesRequired = int(request.form['places'])
        if placesRequired > int(club['points']):
            error = 'You do not have enough points.'
        elif placesRequired > MAXIMUM_BOOKING_PER_CLUB:
            error = (
                f'You can not book more than {MAXIMUM_BOOKING_PER_CLUB}'
                ' places per competition.'
            )
        elif places_booked == MAXIMUM_BOOKING_PER_CLUB:
            error = (
                'You have already reached the maximum'
                ' number of places for this competition'
            )
        elif int(competition['numberOfPlaces']) == 0:
            error = 'This competition is full'
        elif placesRequired > int(competition['numberOfPlaces']):
            error = (
                f'You try to purchase {placesRequired} places but there '
                f'are only {competition["numberOfPlaces"]} left for '
                'this competition.'
            )
        elif (places_booked + placesRequired) > MAXIMUM_BOOKING_PER_CLUB:
            error = (
                'You can purchases no more than '
                f'{MAXIMUM_BOOKING_PER_CLUB - places_booked} places'
                ' as your club has already purchased'
                f' {places_booked} of them'
            )

    if error:
        return render_template(
            'booking.html',
            club=club,
            competition=competition,
            error=error,
            max_booking_per_club=MAXIMUM_BOOKING_PER_CLUB,
            places_booked=places_booked,
            maximum_booking=min(
                int(club['points']),
                int(competition['numberOfPlaces']),
                MAXIMUM_BOOKING_PER_CLUB - places_booked,
            )
        ), 400
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points']) - placesRequired
    competition['places_booked'][club['name']] += placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))