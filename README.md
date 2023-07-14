This is recreation of cherrypy tutorial number 09 with use of React 18.

React part is done using simple pure JS Vite project.

Development run of Vite project will not work as there is no backend.

For this to run:

- You need to build poject.
- You need to move/copy generated \*.js file from dist assets folder of Vite project to cherrypy public/assets folder.
- Then you need to replace \*.js name in script tag of index.html (cherrypy project).

Activate cherrypy environment with 'source ./bin/activate'.

Then you can start python script with 'python tut09.py'.

Ouch!!! For this to run you will need mariadb database :)
