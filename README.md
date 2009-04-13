# Ai Stager

## Overview

**Ai Stager** is a Django powered staging platform for displaying design compositions to clients in a structured manner using an outlined view with project resources.

## Installation

1. Clone the repository from GitHub.

        git clone git://github.com/aiaio/ai-stager

2. Create a ``settings.py`` file from the ``settings.py.template`` file.

4. Setup your database and add the criteria to ``settings.py``. Works with Django >= 1.0.

3. Run ``python manage.py syncdb`` and create an admin user.

# Using Ai Stager

## Creating Users 

1. From the ``/admin`` homepage, click add user.
2. Enter username and password.
3. Check the "active" box.
4. If the user is a client, omit permissions.
5. Click "save".

## Creating Clients

1. From the ``/admin`` homepage, click add client.
2. Enter the client's name.
3. Name the client url fragment (yoururl.com/clientname).
4. Upload a logo (Width = 200, Height = 55).
5. Check the "active" box.
6. Choose a user. This designates what login info will be assigned to the client url.
7. Create projects (ie. "Alexander Interactive" or "AI2883 Alexander Interactive").
8. Designate urls for each project (yoururl.com/clientname/projectname).

NOTE: Don't add contacts under this section, as you cannot add multiple contacts here. You can do this under the "contacts" section.

## Creating Contacts

1. From the ``/admin`` homepage, click add contact.
2. Add contact info.
3. Check "active".
4. If an employee, check "staff". If not, the system will assume the contact is a client.
5. Add the project to which you'd like to add this contact, and click "save."
6. On the front end, project view, contacts will appear on the right side of the page.

## Creating Categories

1. From the ``/admin`` homepage, click projects.
2. Select a project, now you are in "project" view.
3. Name categories. These will be the tabs across the top of a project page, such as "design," "ia," or "account".
4. Number the categories under "ordering." The first should be labeled "0," the second should be "1", and so forth.
5. Check a default category. The default will automatically display that tab when you hit the project url.
6. Click "save and continue editing" to register the categories. When the page refreshes, there will be links to edit categories above the category names.

## Creating External Links

1. From the ``/admin`` homepage, click projects.
2. Select a project, now you are in "project" view.
3. Filling out the link section at the bottom of the page will place links or files on the upper right hand side of a project page, under "project resources."
4. Click "save and continue editing".

## Creating Sections

1. From the ``/admin`` homepage, click projects
2. Select a project, now you are in "project" view.
3. Fill out the name of section, assign a category, and select a date. A section is a large break in any of the categories.
4. Click save and continue editing, then a link to edit that section will appear above the section name. click into that link, now you are in "section" view.
5. Add descriptions and subsections. Click "save and continue editing." If you've added a subsection, a link will appear above the subsection name.

## Adding comps

1. From the ``/admin`` homepage, click projects, select project, click into the appropriate section.
2. Under "comps", add comp names and ordering, click "save and continue editing".
3. Click the link above the comp name you'd like to change. Now you are in "comp" view.
4. If you want to add a single file, add 1 file here.
5. If you want to create a clickthrough, add multiple files here, and order them. 
6. click "save."

## Creating Subsections And Adding Comps:

1. From the ``/admin`` homepage, click projects, select project, click into the appropriate section.
2. Under "subsections," add name and description, check "active," then click "save and continue editing".
3. Click into the newly created subsection link
4. Under "comps", add the name of the comps and ordering, then click "save and continue editing".
5. Click the link above the comp name you'd like to change. Now you are in "comp" view.
6. If you want to add 1 comp for viewing, add it here, then click save and continue editing.
7. If you want to create a click through, add multiple files here, and order them.
8. Click "save"

# Congratulations! You have staged!

# Development and contributions

This is an initial release. Expect regular improvements.

We welcome any improvements or suggestions to Ai Stager.  Please contact us through our github account.

# Author & License

Ai Stager was originally developed for Ai's Internal use by Loren Davie and later re-factored by David Napolitan.  The initial HTML integration was done by Tom Rosario.  Ai Stager is now maintained by Sean Auriti and Nick Angiolillo with project management by Amanda McCroskery. Favicon by Skottey Forden. Repo magic by Joshua Rusch. QA by David Kamm, Robert Gurdian and Alex Schmelkin. Used by all Ai PMS. Final word by Josh Levine.

Ai Stager is licensed under a modified MIT licence. See LICENCE.txt.

Copyright 2009 Alexander Interactive, Inc.

