# Dynatrace DB Queries Extension Bulk Migrator

Tool to help with creating Extensions 2.0 declarative SQL extensions off of Extensions 1.0 Custom DB Queries extension configurations.

## API Authentication

For commands that interact with the Dynatrace API you need to provide an API URL and Access token. These can be provided on the command line but it is recommended to use environment variables:

- DT_URL (e.g. https://xxx.live.dynatrace.com)
- DT_TOKEN
  - permissions:
    - ReadConfig
    - WriteConfig
    - extensions.read
    - extensions.write
    - metrics.read

## Commands

Use `--help` with any command to view unique options.

```
 Usage: dbqm pull [OPTIONS]

 Pull EF1 db queries configurations into a spreadsheet.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --dt-url             TEXT  [env var: DT_URL] [default: None] [required]                                                                                                                                                                                         │
│ *  --dt-token           TEXT  [env var: DT_TOKEN] [default: None] [required]                                                                                                                                                                                       │
│    --output-file        TEXT  [default: custom.remote.python.dbquery-export.xlsx]                                                                                                                                                                                  │
│    --help                     Show this message and exit.  
```

### dbqm pull

Used to pull all EF1 Custom DB Queries configurations and export them to an Excel sheet for manual review and as an input to later steps.

### dbqm build

Used to build extensions from a previously exported configuration excel workbook.

#### Certificate and key

Before building you need to create a developer key and certificate. These will be used to sign the extension packages. Refer to the steps [here](https://docs.dynatrace.com/docs/shortlink/sign-extension#cert) for creating the certificate and key file(s). The `developer.pem` file will be used in the build command.

#### Required options

- `--cert-file-path` path to developer.pem
- `--private-key-path` path to developer.pem
- `--input-file` path to the previously exported configuration exce;
- `--merge-endpoints` tells the tool to merge endpoints based on a matching host or jdbc string (to avoid hitting limits if it were one extension per EF1 DB queries endpoint)
- `--credential-vault-id` a credential vault ID to be used in the created monitoring configurations
- `--directory` path to where the migrated extensions will be stored locally
- `--upload` upload and activate extensions after build
- `--create-config` create an initial monitoring configuration based on the db queries configuration (in a disabled state)
- `--pre-cron` set this if you are waiting to update AG to 1.301, by default it will set the cron schedule in the new extension but this is only available in AG 1.301+
- `--scope` sets the AG group any created configs will be assigned. If not prefixed with 'ag_group-' this will be added automatically (default: 'ag_group-default)
- `--log-directory` the directory where the log file/report will be generated
- `--include-disabled` by default, disabled EF1 endpoints will be disabled. Use this option to include them.


Example:

```
dbqm build --cert-file-path=developer.pem --private-key-path=developer.pem  --input-file=custom.remote.python.dbquery-export.xlsx --merge-endpoints --directory=C:\workspaces\migrated_extensions
```

After running in the directory (default: migrated_extensions) you will see a directory per new extension which will contain a src directory and a signed zip of the new extension.

In addtion to just building the extensions you can both have them uploaded to the environment, activated, and have an initial monitoring configuration created with what was avaialble in the original DB queries configurations.

To build the extension, activate it, and have a configuration created run:

```
dbqm build --cert-file-path=developer.pem --private-key-path=developer.pem  --input-file=custom.remote.python.dbquery-export.xlsx --merge-endpoints --directory=C:\workspaces\migrated_extensions --upload --create-config --scope=myActiveGateGroup
```

This will generate a report like `\.db-queries-build-2024-11-08_18-16.txt` with a summary of how the build/activation process went. After building, you should review this file for any potential issues that may need to be addressed.

Each time the build occurs it will check the environment and increment the extension version if needed.

Sample output:

```
Processing input file 'C:\workspaces\projects\db-queries-bulk-migrator\db-queries-bulk-migrator\custom.remote.python.dbquery-export.xlsx'.

###### localhost_xe ######

Built/signed extension zip: 'migrated_extensions\custom_db.query.localhost-xe\custom_db.query.localhost-xe-1.0.3.zip'.
Validating...
Extension validated: custom:db.query.localhost-xe (1.0.3)
Extension uploaded: custom:db.query.localhost-xe (1.0.3)
Link to monitoring configuration: https://<environment>.com/ui/hub/ext/listing/registered/custom:db.query.localhost-xe/06314501-c065-33e2-a099-577e13fd8286/edit

###### localhost_DYNA ######

Built/signed extension zip: 'migrated_extensions\custom_db.query.localhost-dyna\custom_db.query.localhost-dyna-1.0.3.zip'.
Validating...
Extension validated: custom:db.query.localhost-dyna (1.0.3)
Extension uploaded: custom:db.query.localhost-dyna (1.0.3)
Link to monitoring configuration: https://<environment>.com/ui/hub/ext/listing/registered/custom:db.query.localhost-dyna/620943f0-763b-3ccc-88ab-f40d586dd506/edit

###### jdbc:mysql://<host>:3307/information_schema?useUnicode=true&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=UTC ######

Error building extension from migrated_extensions\custom_db.query.localhost-dyna\src\extension.yaml: MySQL datasource does not currently support connection strings.
```

### dbqm delete

**This command is primarily for use during the migration process for when mistakes are made or changes are required. It allows you to completely delete the created extensions. There are a number of prompts/checks to help you avoid mistakes but use caution with this command as it can be used to delete all traces of any 2.0 extension.**

#### Required options

- `--pattern` a pattern using 'contains' logic that will match 2.0 extension names for deletion. It will not allow an empty value and if a pattern that doesn't use `db.query` is used it will warn/prompt you if you want to continue.

```
dbqm delete --pattern custom:db.query
```

Example output/confirmation:
```
custom:db.query.abc
custom:db.query.def
custom:db.query.ghi
The above listed 3 extensions will be deleted along with any configurations. Are you sure? [y/N]: y
...
```