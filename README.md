# Rireki [![Github Actions Status](https://github.com/noeldemartin/rireki/workflows/Testing/badge.svg)](https://github.com/noeldemartin/rireki/actions)

CLI backup tool.

## Installation

Install the rireki cli running the following command:

```sh
pip install rireki
```

You need to call `rireki backup` in order for backups to be performed. For example, you could use the following crontab configuration to perform backup checks every hour (remember to create the `/var/log/rireki` directory as well):

```sh
0 * * * * rireki backup >> /var/log/rireki/cron.log 2>> /var/log/rireki/cron-error.log
```

## Usage

Get detailed information running `rireki --help`.

There are three core concepts on how rireki manages backups:

- **Projects:** A project is something you want to back up. For example a website database or a collection of files.

- **Drivers:** A driver is the program used to create the backup files. For example zipping up a folder or dumping a database.

- **Stores:** A store is the program used to save the backup files created with a driver. For example copying them to a local folder or uploading them to a 3rd party service.

In order to install a new project to backup, a configuration file can be added to `~/.rireki/projects/{project-name}.conf`. This will be a [toml](https://github.com/toml-lang/toml) configuration file. It can either be created manually or calling `rireki add {project-name}`.

### Drivers

#### Files

This driver creates an archive with files copied from the local filesystem. The archive will be a zip file if possible or a tar file.

It needs the following configuration:

| property      | type          | description  |
| ------------- |---------------| -------------|
| name          | `"files"`     | The name of the driver. |
| frequency     | `integer`     | The frequency in seconds at which new backups should be made. |
| paths         | `string[]`    | Folders or files that will be included in the archive. |

#### Custom

This driver can be used if backing up a project is not supported by any of the other drivers. It consists of a custom script that will be called to generate the backup artifacts. The backup files should be placed on a path indicated by the `RIREKI_BACKUP_PATH` env variable.

Once the script has completed, a file named `logs.json` will also be placed on the path with the standard output and standard error printed by the script.

It needs the following configuration:

| property      | type          | description  |
| ------------- |---------------| -------------|
| name          | `"custom"`    | The name of the driver. |
| frequency     | `integer`     | The frequency in seconds at which new backups should be made. |
| command       | `string`      | Command to call in order to perform backups. |
| timeout       | `integer`     | Number of seconds where the command will be timed out and the backup will fail. |

### Stores

#### Local

This store copies the backups to a folder in the same filesystem.

It needs the following configuration:

| property      | type          | description  |
| ------------- |---------------| -------------|
| name          | `"local"`     | The name of the store. |
| path          | `string`      | The path of the folder where the backups will be copied. |

#### Amazon Web Services

This store uploads the backups to an AWS S3 instance.

It needs the following configuration:

| property      | type          | description  |
| ------------- |---------------| -------------|
| name          | `"aws"`     | The name of the store. |
| region        | `string`      | The region where the S3 instance is located. |
| access_key    | `string`      | The access key ID. |
| access_secret | `string`      | The secret access key. |
| bucket        | `string`      | The name of the bucket where the files will be uploaded. |
| path          | `string`      | The path within the bucket where the files will be placed. |

#### Digital Ocean

This store uploads the backups to a Digital Ocean Spaces instance.

It uses the same configuration as the AWS store, with the only exception that the name is `"digital-ocean"` instead.

### An example config file

For example, to backup a project named "Foobar" using the `files` driver and the `local` store we would create the following file at `~/.rireki/projects/foobar.conf`:

```toml
name="foobar"

[driver]
name="files"
paths=["/path/to/data/folder"]
frequency=1440

[store]
name="local"
path="/path/to/backups/folder"
```

As mentioned before, you could call `rireki add foobar` to create this file.

## Development

Run tests with `pytest` and lint your code with `flake8` (see the [Github Actions configuration](.github/workflows/testing.yml) for more details).
