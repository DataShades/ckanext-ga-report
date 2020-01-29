from __future__ import print_function, absolute_import

import datetime
import logging
import os

import ckan.plugins.toolkit as tk
import click


log = logging.getLogger(__name__)


def get_commands():
    return [ga_report]


@click.group("ga-report")
def ga_report():
    """GA Report management commands
    """


@ga_report.command()
def init():
    """Initialise the extension's database tables
    """

    from . import ga_model

    ga_model.init_tables()
    click.secho("DB tables are setup", fg="green")


@ga_report.command()
def fix():
    """
    Fixes the 'All' records for GA_Urls

    It is possible that older urls that haven't recently been visited
    do not have All records.  This command will traverse through those
    records and generate valid All records for them.
    """
    from .ga_model import post_update_url_stats

    click.echo("Updating 'All' records for old URLs")
    post_update_url_stats()
    click.secho("Processing complete", fg="green")


@ga_report.command()
@click.argument("time_period", default="latest")
@click.option(
    "-d",
    "--delete-first",
    is_flag=True,
    help="Delete data for the period first",
)
@click.option(
    "-s",
    "--skip_url_stats",
    is_flag=True,
    help="Skip the download of URL data - just do site-wide stats",
)
def load(time_period, delete_first, skip_url_stats):

    """Get data from Google Analytics API and save it
    in the ga_model

    Usage: paster loadanalytics <time-period>

    Where <time-period> is:
        all         - data for all time
        latest      - (default) just the 'latest' data
        YYYY-MM     - just data for the specific month
    """

    token = ""

    from .download_analytics import DownloadAnalytics
    from .ga_auth import init_service, get_profile_id

    ga_token_filepath = os.path.expanduser(
        tk.config.get("googleanalytics.token.filepath", "")
    )
    if not ga_token_filepath:
        tk.error_shout(
            "ERROR: In the CKAN config you need to specify the filepath of the "
            "Google Analytics token file under key: googleanalytics.token.filepath"
        )
        raise click.Abort()

    try:
        token, svc = init_service(ga_token_filepath)
    except TypeError as e:
        tk.error_shout(
            "Have you correctly run the getauthtoken task and "
            "specified the correct token file in the CKAN config under "
            '"googleanalytics.token.filepath"?'
        )
        raise click.Abort()

    downloader = DownloadAnalytics(
        svc,
        token,
        profile_id=get_profile_id(svc),
        delete_first=delete_first,
        skip_url_stats=skip_url_stats,
    )

    if time_period == "all":
        downloader.all_()
    elif time_period == "latest":
        downloader.latest()
    else:
        # The month to use
        for_date = datetime.datetime.strptime(time_period, "%Y-%m")
        downloader.specific_month(for_date)
