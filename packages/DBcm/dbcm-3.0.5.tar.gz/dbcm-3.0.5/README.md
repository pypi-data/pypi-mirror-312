
## Release 3 of DBcm

The DBcm.UseDatabase context manager for working with MySQL/MariaDB and SQLite3.

The 1.x release of this module was based on code created for the second edition 
of Head First Python. See chapters 7, 8, 9, and 11 of the that book for information
on how this module was originally created. The 2.x and 3.x releases were updated 
during the writing of the third edition of the book.

### Installation Notes

To install the second edition release of DBcm, please use: 

    pip install --upgrade DBcm==1.7.4

To install DBcm for use with a MySQL server (for example, on PythonAnywhere), please use: 

    pip install --upgrade DBcm==2.1

Note: on the PythonAnywhere command-line, prefix the above "pip" command with "python3 -m ".

The 3.x release (the default install target) specifically works with the MariaDB server (for 
compatibility reasons).

### The Latest (and Greatest) DBcm

For the third edition of Head First Python, DBcm moved to release 2. The option to use 
SQLite3 is now supported in this new release.  Release 3 of DBcm removes the dependancy
on mysql.connector and replaces it with (the more up-to-date) mariadb library (but do 
consider the Installation Notes, above).

### Using DBcm

Simple example usage (for a MySQL/MariaDB backend):

    from DBcm import UseDatabase, SQLError

    config = { "host": "127.0.0.1",
               "user": "myUserid",
               "password": "myPassword",
               "database": "myDB" }

    with UseDatabase(config) as cursor:
        try:
            _SQL = "select * from log"
            cursor.execute(_SQL)
            data = cursor.fetchall()
        except SQLError as err:
            print("Your query caused an issue:", str(err))

If a filename (string) is used in place of a config dictionary when using 
DBcm.UseDatabase, the data is assumed to reside in a local SQLite file (which
gets created if it doesn't previously exist).
 
