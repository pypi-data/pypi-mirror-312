# Happy Migrations: Hopefully no tears. (WIP)
Architecture:

- up
- up-all
- up-to

Require Access to DB
- down
- down-to
- down-all

TODO:
1. Display nice error messages for lacking happy.ini or its data


Flow:
1. create - Create mig file.
2. up:
   1. check which should be applied
   2. parse mig
   3. apply mig
   4. add to the status
3. down:
   1. check which should be rolled back
   2. parse mig
   3. rollback mig
   4. remove from the status



Test:
- Coverage
- Commands
- Data classes


CLI:
- Print notifications like:
  - Warning: No migration to apply
  - Success: Migration has being applied

Docs:
- Create docs with MkDocs


Commands:
- up
- up-all
- up-to
- down
- down-to
- down-all
- status
- create
- fixture
