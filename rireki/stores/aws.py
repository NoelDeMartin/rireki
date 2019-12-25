import boto3
import click
import os
import re

from functools import reduce
from rireki.core.store import Store
from rireki.utils.file_helpers import file_get_name


class AmazonWebServices(Store):
    NAME = 'aws'

    def __init__(self):
        Store.__init__(self)

        self.region = None
        self.access_key = None
        self.access_secret = None
        self.bucket = None
        self.path = None

    def ask_config(self):
        Store.ask_config(self)

        click.echo('Please, introduce credentials for %s.' % self._get_service_name())

        self.region = self.__ask_region()
        self.access_key = self.__ask_access_key()
        self.access_secret = self.__ask_access_secret()
        self.bucket = self.__ask_bucket()
        self.path = self.__ask_path()

    def load_config(self, config):
        Store.load_config(self, config)

        self.region = config['region']
        self.access_key = config['access_key']
        self.access_secret = config['access_secret']
        self.bucket = config['bucket']
        self.path = config['path']

    def get_config(self):
        config = Store.get_config(self)

        config['region'] = self.region
        config['access_key'] = self.access_key
        config['access_secret'] = self.access_secret
        config['bucket'] = self.bucket
        config['path'] = self.path

        return config

    def _get_backup_names(self):
        client = self.__create_s3_client()
        paginator = client.get_paginator('list_objects')
        page_iterator = paginator.paginate(Bucket=self.bucket, Prefix=self.path)

        files = reduce(
            sum,
            [self.__parse_page_files(self.path, page) for page in page_iterator],
        )

        return sorted([file_get_name(file) for file in files], reverse=True)

    def _upload_file(self, source, destination):
        client = self.__create_s3_client()

        client.upload_file(
            source,
            self.bucket,
            os.path.join(self.path, destination),
        )

    def _get_service_name(self):
        return 'Amazon Web Services'

    def _get_endpoint_url(self):
        return 'https://s3.%s.amazonaws.com' % self.region

    def __ask_region(self):
        return click.prompt('Region')

    def __ask_access_key(self):
        return click.prompt('Access Key')

    def __ask_access_secret(self):
        return click.prompt('Access Secret (hidden)', hide_input=True)

    def __ask_bucket(self):
        return click.prompt('Bucket')

    def __ask_path(self):
        return click.prompt('Path')

    def __create_s3_client(self):
        return boto3.client(
            's3',
            region_name=self.region,
            endpoint_url=self._get_endpoint_url(),
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.access_secret,
        )

    def __parse_page_files(self, path, page):
        backup_names = []

        if 'Contents' not in page:
            return backup_names

        if not path.endswith('/'):
            path += '/'

        regex = '%s([^\\/]+)\\/?$' % path.replace('/', '\\/')

        for item in page['Contents']:
            match = re.match(regex, item['Key'])

            if match:
                backup_names.append(match.group(1))

        return backup_names
