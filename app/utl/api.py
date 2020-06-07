from googleapiclient.discovery import build
import datetime

# Calendar API =================================================================
def get_calendar(credentials, courses):
    calendar = build('calendar', 'v3', credentials = credentials)
    dict = {}

    for course in courses:
        arr = []
        events = calendar.events().list(calendarId = course[1]).execute()
        for event in events['items']:
            # Dict mappings: https://developers.google.com/calendar/v3/reference/events#resource
            summary = event['summary']
            if "dateTime" in event['start']:
                due_date = str(event['start']['dateTime'])
                due_day = due_date[:10]
                due_time = due_date[11:16]
                arr.append({
                    "summary": summary,
                    "due_day": due_day,
                    "due_time": due_time
                })

            dict[course[0]] = arr

    return dict
# ==============================================================================
class Work:
    def __init__(self, id, title, description, creationTime, updateTime, dueDate, dueTime, creatorUserID, sortTime):
        self.id = id
        self.title = title
        self.description = description
        self.creationTime = creationTime
        self.updateTime = updateTime
        self.dueDate = dueDate
        self.dueTime = dueTime
        self.creatorUserID = creatorUserID
        self.sortTime = sortTime

class Announcement:
    def __init__(self, id, text, creationTime, updateTime, creatorUserID, sortTime):
        self.id = id
        self.text = text
        self.creationTime = creationTime
        self.updateTime = updateTime
        self.creatorUserID = creatorUserID
        self.sortTime = sortTime

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

def get_user_info(credentials, userid):
    gclass = build('classroom', 'v1', credentials = credentials)
    results = gclass.userProfiles().get(userId = userid).execute()

    dict = {}
    dict['name'] = results['name']['fullName']

    return dict

def get_courses(credentials):
    gclass = build('classroom', 'v1', credentials = credentials)

    results = gclass.courses().list().execute()
    courses = results.get('courses', [])

    return courses

def get_course(credentials, courseid):
    gclass = build('classroom', 'v1', credentials = credentials)

    results = gclass.courses().get(id = courseid).execute()

    return results

def get_posts(credentials, courseid):
    gclass = build('classroom', 'v1', credentials = credentials)
    posts = []

    resultsWork = gclass.courses().courseWork().list(courseId = courseid).execute()
    courseWork = resultsWork.get('courseWork', [])
    for work in courseWork:
        description = ""
        if 'description' in work:
            description = work['description']
        creationTime = str(work['creationTime'][:10]) + " " + str(work['creationTime'][11:19])
        updateTime = str(work['updateTime'][:10]) + " " + str(work['updateTime'][11:19])
        dueDate = ""
        dueTime = ""
        if 'dueDate' in work:
            dueDate = str(work['dueDate']['year']) + '-' + str(work['dueDate']['month']) + '-' + str(work['dueDate']['day'])
        if 'dueTime' in work:
            if 'minutes' in work['dueTime']:
                dueTime = str(work['dueTime']['hours']) + ':' + str(work['dueTime']['minutes'])
            else:
                dueTime = str(work['dueTime']['hours']) + ':00'

        posts.append(Work(
            id = work['id'],
            title = work['title'],
            description = description,
            creationTime = creationTime,
            updateTime = updateTime,
            dueDate = dueDate,
            dueTime = dueTime,
            creatorUserID = work['creatorUserId'],
            sortTime = work['updateTime']
        ))

    resultsAnnounce = gclass.courses().announcements().list(courseId = courseid).execute()
    announcements = resultsAnnounce.get('announcements')
    for announcement in announcements:
        creationTime = str(announcement['creationTime'][:10]) + " " + str(announcement['creationTime'][11:19])
        updateTime = str(announcement['updateTime'][:10]) + " " + str(announcement['updateTime'][11:19])

        posts.append(Announcement(
            id = announcement['id'],
            text = announcement['text'],
            creationTime = creationTime,
            updateTime = updateTime,
            creatorUserID = announcement['creatorUserId'],
            sortTime = announcement['updateTime']
        ))

    posts.sort(key = lambda x: x.sortTime, reverse = True)

    return posts
