var OAuth = {
	"web": {
		"client_id": "239631765696-037srjr0o8linju7o55ca1f7mcf33use.apps.googleusercontent.com",
		"project_id": "aware-170816",
		"auth_uri": "https://accounts.google.com/o/oauth2/auth",
		"token_uri": "https://accounts.google.com/o/oauth2/token",
		"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
		"client_secret": "WT-wLU2ZdWK1raIbS0Dgunfp",
		"javascript_origins": [window.location.origin]
	}
}
var R33ID = 'utexas.edu_lp55dg3h0fp4c3r2custiqkhdg@group.calendar.google.com';
var CLIENT_ID = '239631765696-037srjr0o8linju7o55ca1f7mcf33use.apps.googleusercontent.com';
// Array of API discovery doc URLs for APIs used by the quickstart
var DISCOVERY_DOCS = ["https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest"];
// Authorization scopes required by the API; multiple scopes can be
// included, separated by spaces.
var SCOPES = "https://www.googleapis.com/auth/calendar.readonly";
var authorizeButton = document.getElementById('authorize-button');
var signoutButton = document.getElementById('signout-button');
/**
 *  On load, called to load the auth2 library and API client library.
 */
function handleClientLoad() {
	gapi.load('client:auth2', initClient);
}
/**
 *  Initializes the API client library and sets up sign-in state
 *  listeners.
 */
function initClient() {
	gapi.client.init({
		discoveryDocs: DISCOVERY_DOCS,
		clientId: CLIENT_ID,
		scope: SCOPES
	}).then(function() {
		// Listen for sign-in state changes.
		gapi.auth2.getAuthInstance().isSignedIn.listen(updateSigninStatus);

		// Handle the initial sign-in state.
		updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());
		authorizeButton.onclick = handleAuthClick;
		signoutButton.onclick = handleSignoutClick;
	});
}
/**
 *  Called when the signed in status changes, to update the UI
 *  appropriately. After a sign-in, the API is called.
 */
function updateSigninStatus(isSignedIn) {
	if (isSignedIn) {
		authorizeButton.style.display = 'none';
		signoutButton.style.display = 'block';
		listUpcomingEvents();
	} else {
		$('#myModal').modal('show')
		authorizeButton.style.display = 'block';
		signoutButton.style.display = 'none';
	}
}

/**
 *  Sign in the user upon button click.
 */
function handleAuthClick(event) {
	gapi.auth2.getAuthInstance().signIn();
}

/**
 *  Sign out the user upon button click.
 */
function handleSignoutClick(event) {
	gapi.auth2.getAuthInstance().signOut();
}

/**
 * Append a pre element to the body containing the given message
 * as its text node. Used to display the results of the API call.
 *
 * @param {string} message Text to be placed in pre element.
 */
function appendPre(message) {
	var pre = document.getElementById('content');
	var textContent = document.createTextNode(message + '\n');
	pre.appendChild(textContent);
}

/**
 * Print the summary and start datetime/date of the next ten events in
 * the authorized user's calendar. If no events are found an
 * appropriate message is printed.
 */
var gcalList;
function listUpcomingEvents() {
	gapi.client.calendar.events.list({
		'calendarId': R33ID,
		'timeMin': (new Date()).toISOString(),
		//'showDeleted': false,
		'singleEvents': true,
		//'maxResults': 10,
		'orderBy': 'startTime'
	}).then(function (resp) {
		gcalResp = resp
		console.log(resp)
		gcalList = [];
		var successArgs;
		var successRes;
		if (resp.result.error) {
			reportError('Google Calendar API: ' + data.error.message, data.error.errors);
		} else if (resp.result.items) {
			$.each(resp.result.items, function (i, entry) {
				var url = entry.htmlLink;
				gcalList.push({
					id: entry.id,
					title: entry.summary,
					start: entry.start.dateTime || entry.start.date, // try timed. will fall back to all-day
					end: entry.end.dateTime || entry.end.date, // same
					location: entry.location,
					description: entry.description
				});
			});
			// call the success handler(s) and allow it to return a new events array
			console.log(gcalList)
			successArgs = [gcalList].concat(Array.prototype.slice.call(arguments, 1)); // forward other jq args
			successRes = $.fullCalendar.applyAll(true, this, successArgs);
			if ($.isArray(successRes)) {
				return successRes;
			}
		}
		if (gcalList.length > 0) {
			// Here create your calendar but the events options is :
			//fullcalendar.events: gcalList (Still looking for a methode that remove current event and fill with those news event without recreating the calendar.
		}
		return gcalList;
	}, function (reason) {
		console.log('Error: ' + reason.result.error.message);
		});
}
var appendPre;