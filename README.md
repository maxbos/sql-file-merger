# sql-file-merger
Provides an architecture for structuring your SQL project using a dependency mechanism

# What does it do?
Ever had the problem of designing a SQL database and you don't want to have everything in one .sql file but work organized instead? Then this handy tool may help you out. This tool lets you require other .sql files, so you can write your database schema over an arbitrary number of .sql files while maintaining the import structure of your schema. Then, when you are done working on your database version you simply run `python ./main.py` inside the `sql-file-merger` folder to merge all your .sql files into one correctly ordered version file.

An example:
You have a table `profile` that references to the table `user`, and you want to have 2 separate .sql files for these tables. With this tool you can create 2 files: `table_user.sql` and `table_profile.sql`, and require the `user` table by adding `-- requires: table_user` at the top of your `table_profile.sql` file.

This tool expects the following folder structure:
- `v.*.*.*`: any number of version folders, for example v0.0.0 or v1.0.2. This folder will contain your .sql files.
- `db-versions`: this folder will contain the final merged .sql version files, for example v0.0.0.sql and current.sql.
- `sql-file-merger`: needs to contain the `sql-file-merger/main.py` from this repository.
