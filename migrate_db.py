from playhouse.migrate import *

import models

my_db = models.psql_db
migrator = PostgresqlMigrator(my_db)


