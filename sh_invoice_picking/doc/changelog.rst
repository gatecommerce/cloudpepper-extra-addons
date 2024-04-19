17.0.1(26th Sep 2023)
-----------------------

Initial Release.

17.0.2 (29th Jan 2024)
-----------------------

- Fix Quanitty Done Field issue

17.0.3 (30th Jan 2024)
-----------------------

- [FIX] module is conflicted with other module and invoice count is wrong

17.0.4 (12th Fabruary 2024)
-----------------------

- [FIX] issue of journal entry with Anglo-Saxon Accounting

17.0.5 (12th April 2024)
-----------------------
- [Removed] Separate Invoices boolean field from Create Invoice wizard
- [Added] Code to skip cancelled picking and forcefully validate picking
- [Updated] Set picking_ids m2m field to readonly in account.move

17.0.6 (18th April 2024)
------------------------
- [Updated] Code updated to Create Invoice/Bill only for selected picking 
            and remove extra invoice lines from Invoice/Bill which are not in picking