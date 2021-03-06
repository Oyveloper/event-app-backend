from flask_app.flask_app.app import app, event_storage
from flask import jsonify, request
from event import Event, EventFilter, FilterOperator
from datetime import datetime


@app.route('/get_events')
def get_events():
    """
    Returns a list of all events from all datasources
    
    It is possible to filter the request with the following flags
    - name: str – name containing the given string 
    - class_year: str – study program containing given string
    - host: str – Name of the host
    - study_program: str – name of the study programs allowed
    - start: str (timestamp) – The earliest starting time of the events
    - Soon: dateRange: str – two timestamps separated with - as 'start-stop'.
    Gives all events in the interval
    - 
    """

    # Handle the filters
    filter_keys = [
        "name",
        "host",
        "class_year",
        "study_program",
        "start",
        "end",
        "type"
    ]

    filters = []

    for key in filter_keys:
        value = request.args.get(key, "")

        values = []

        if value != "":
            filter_operator = ""
            if key == "start":
                filter_operator = FilterOperator.GREATER_THAN
                value = datetime.strptime(value, "%Y-%m-%d")
                values = [value]
            elif key == "end":
                filter_operator = FilterOperator.LESS_THAN
                value = datetime.strptime(value, "%Y-%m-%d")
                values = [value]
            else:
                filter_operator = FilterOperator.LIKE
                values = [f"%{val}%" for val in value.split(",")]

            filters.append(EventFilter(key, values, filter_operator))

            


    events = []
    if len(filters) == 0:
        events = event_storage.get_all_events()
    else:  
        events = event_storage.get_filtered_events(filters)

    events = [e.__dict__ for e in events]

    
    return jsonify(events)


@app.route('/search')
def search():
    """
    Search the event database for the given query 
    """
    query = request.args.get('query')

    # Execute the query
    events = [e.__dict__ for e in event_storage.search(query)]

    return jsonify(events)


@app.route('/suggestions')
def suggestions():
    """
    Returns a list of suggestions for what the user might want to
    search for, based on the query url parameter
    """
    query = request.args.get('query')
    if not query is None:
        return jsonify(event_storage.getSuggestions(query))

    
@app.route('/get_hosts')
def get_hosts():
    """
    Returns a list of all hosts with events in the database
    """
    hosts = event_storage.get_all_hosts()
    return jsonify(hosts)


@app.route('/get_types')
def get_types():
    """
    Returns a list of all types of events in the db
    """
    return jsonify(event_storage.get_all_types())


@app.route("/get_study_programs")
def get_study_programs():
    """
    Returns a list of all study programs mensioned in events in the db
    """
    return jsonify(event_storage.get_all_study_programs())

