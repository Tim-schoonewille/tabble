# Tabble
Tabble will be a project where I will practice becoming a full-stack developer. Creating a restufl-api backend with Python's Flask, and a front-end interface using React. 
Currently I have the skills to create a full functioning backend, but I do not yet posses the necesasrily skills to create a frontend in JS. 

---
### About Tabble:

**Tabble** will be an app to search, save and manage Guitar Tabs. Making it easier for you to a musician to be in touch with songs you want to practice. 

---
## Todo:

#### Backend:
- Design the database
- Write down endpoints.
- Create an authentication system
- Write logic to save and edit found tabs.
- Write logic to find tabs with the API instead of manually saving them to your profile
- Create an admin/moderator portal.

#### Frontend:
- Learn CSS/JS/React
- Rough sketch/design the layout.
- Convert sketch/design to HTML/CSS
- Apply React magic
- ..
- .....
- Profit?

---
## Backend API endpoints

* /auth/
  * /auth/login
  * /auth/logout
  * /auth/register
  * /auth/<user_uuid>/confirm/<registration_uuid>
  * /auth/<user_uuid>/confirm/new
* /tabs/
  * /tabs/artist/<artist>
* /tab/
  * /tab/<tab_uuid>
  * /tab/<tab_uuid>/favourite
  * /tab/<tab_uuid>/unfavourite
  * /tab/<tab_uuid>/complete
  * /tab/<tab_uuid>/uncomplete