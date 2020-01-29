import logging
import operator

import ckan.lib.helpers as h
import ckan.plugins.toolkit as tk


import ckan.model as model

from ckanext.ga_report.ga_model import GA_Url, GA_Publisher
from ckanext.ga_report.views import _get_publishers


log = logging.getLogger(__name__)


def get_helpers():

    return {
        "ga_report_installed": lambda: True,
        "popular_datasets": popular_datasets,
        "most_popular_datasets": most_popular_datasets,
        "single_popular_dataset": single_popular_dataset,
        "month_option_title": month_option_title,
        "gravatar": custom_gravatar,
        "join_x": join_x,
        "join_y": join_y,
        "get_tracking_enabled": get_tracking_enabled,
        "get_key_helper": get_key_helper,
    }


def custom_gravatar(*pargs, **kargs):
    gravatar = h.gravatar(*pargs, **kargs)
    pos = gravatar.find("/>")
    gravatar = (
        gravatar[:pos]
        + tk.literal(' alt="User\'s profile gravatar" ')
        + gravatar[pos:]
    )
    return gravatar


def popular_datasets(count=10):
    import random

    publisher = None
    publishers = _get_publishers(30)
    total = len(publishers)
    while not publisher or not datasets:
        rand = random.randrange(0, total)
        publisher = publishers[rand][0]
        if not publisher.state == "active":
            publisher = None
            continue
        datasets = _datasets_for_publisher(publisher, 10)[:count]

    ctx = {"datasets": datasets, "publisher": publisher}
    return tk.render_snippet("ga_report/ga_popular_datasets.html", **ctx)


def single_popular_dataset(top=100):
    """Returns a random dataset from the most popular ones.

    :param top: the number of top datasets to select from
    """
    import random

    top_datasets = (
        model.Session.query(GA_Url)
        .filter(GA_Url.url.like("%/dataset/%"))
        .order_by("ga_url.pageviews::int desc")
    )
    num_top_datasets = top_datasets.count()

    dataset = None
    if num_top_datasets:
        count = 0
        while not dataset:
            rand = random.randrange(0, min(top, num_top_datasets))
            ga_url = top_datasets[rand]
            # TODO: [extract SA]
            dataset = model.Package.get(ga_url.url[len("/data/dataset/") :])
            if dataset and not dataset.state == "active":
                dataset = None
            # When testing, it is possible that top datasets are not available
            # so only go round this loop a few times before falling back on
            # a random dataset.
            count += 1
            if count > 10:
                break
    if not dataset:
        # fallback
        dataset = (
            model.Session.query(model.Package)
            .filter_by(state="active")
            .first()
        )
        if not dataset:
            return None
    dataset_dict = tk.get_action("package_show")(
        {"model": model, "session": model.Session, "validate": False},
        {"id": dataset.id},
    )
    return dataset_dict


def single_popular_dataset_html(top=100):
    dataset_dict = single_popular_dataset(top)
    groups = package.get("groups", [])
    publishers = [g for g in groups if g.get("type") == "organization"]
    publisher = publishers[0] if publishers else {"name": "", "title": ""}
    context = {"dataset": dataset_dict, "publisher": publisher_dict}
    return tk.render_snippet("ga_report/ga_popular_single.html", **context)


def most_popular_datasets(publisher, count=100, preview_image=None):

    if not publisher:
        log.error("No valid publisher passed to 'most_popular_datasets'")
        return ""

    results = _datasets_for_publisher(publisher, count)

    ctx = {
        "dataset_count": len(results),
        "datasets": results,
        "publisher": publisher,
        "preview_image": preview_image,
    }

    return tk.render_snippet("ga_report/publisher/popular.html", **ctx)


def _datasets_for_publisher(publisher, count):
    datasets = {}
    entries = (
        model.Session.query(GA_Url)
        .filter(GA_Url.department_id == publisher.name)
        .filter(GA_Url.url.like("%/dataset/%"))
        .order_by("ga_url.pageviews::int desc")
        .all()
    )
    for entry in entries:
        if len(datasets) < count:
            # TODO: [extract SA]
            p = model.Package.get(entry.url[len("/data/dataset/") :])

            if not p:
                log.warning(
                    "Could not find Package for {url}".format(url=entry.url)
                )
                continue

            if not p.state == "active":
                log.warning(
                    "Package {0} is not active, it is {1}".format(
                        p.name, p.state
                    )
                )
                continue

            if not p.private == False:
                log.warning(
                    "Package {0} is private {1}".format(p.name, p.state)
                )
                continue

            if not p in datasets:
                datasets[p] = {"views": 0, "visits": 0}

            datasets[p]["views"] = datasets[p]["views"] + int(entry.pageviews)
            datasets[p]["visits"] = datasets[p]["visits"] + int(entry.visits)

    results = []
    for k, v in datasets.items():
        results.append((k, v["views"], v["visits"]))

    return sorted(results, key=operator.itemgetter(1), reverse=True)


def month_option_title(month_iso, months, day):
    month_isos = [iso_code for (iso_code, name) in months]
    try:
        index = month_isos.index(month_iso)
    except ValueError:
        log.error('Month "%s" not found in list of months.' % month_iso)
        return month_iso
    month_name = months[index][1]
    if index == 0:
        return month_name + (" (up to %s)" % day)
    return month_name


def join_x(graph):
    return ",".join([x for x, y in graph])


def join_y(graph):
    return ",".join([y for x, y in graph])


def get_tracking_enabled():
    return tk.asbool(tk.config.get("ckan.tracking_enabled", "false"))


def get_key_helper(d, key):
    return d.get(key)
