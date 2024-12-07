"""Stream type classes for tap-moosend."""

from __future__ import annotations

import typing as t
from importlib import resources
from singer_sdk import typing as th
from tap_moosend.client import MoosendStream


class CampaignsStream(MoosendStream):
    """Define custom stream."""

    name = "moosend_campaigns"
    path = "/campaigns.json"
    primary_keys = ["ID"]
    replication_key = None
    records_jsonpath = "$.Context.Campaigns[*]"
    schema = th.PropertiesList(
        th.Property(
            "ID", th.StringType, description="Unique identifier for the campaign"
        ),
        th.Property("Name", th.StringType, description="Name of the campaign"),
        th.Property(
            "Subject", th.StringType, description="Subject line of the campaign"
        ),
        th.Property(
            "SiteName",
            th.StringType,
            description="Site name associated with the campaign",
        ),
        th.Property(
            "ConfirmationTo", th.StringType, description="Confirmation email address"
        ),
        th.Property(
            "CreatedOn",
            th.StringType,
            description="Timestamp when the campaign was created (epoch format with timezone offset)",
        ),
        th.Property(
            "ABHoursToTest",
            th.IntegerType,
            nullable=True,
            description="AB testing hours",
        ),
        th.Property(
            "ABCampaignType",
            th.IntegerType,
            nullable=True,
            description="Type of AB campaign if applicable",
        ),
        th.Property(
            "ABWinner",
            th.IntegerType,
            nullable=True,
            description="Winner of the AB test if applicable",
        ),
        th.Property(
            "ABWinnerSelectionType",
            th.IntegerType,
            nullable=True,
            description="Selection type for the AB test winner",
        ),
        th.Property(
            "Status",
            th.IntegerType,
            description="Status of the campaign (e.g., Draft, Sent, etc.)",
        ),
        th.Property(
            "DeliveredOn",
            th.StringType,
            description="Timestamp when the campaign was delivered (epoch format with timezone offset)",
            nullable=True,
        ),
        th.Property(
            "ScheduledFor",
            th.StringType,
            nullable=True,
            description="Scheduled time for the campaign",
        ),
        th.Property(
            "ScheduledForTimezone",
            th.StringType,
            description="Timezone for the scheduled campaign",
        ),
        th.Property(
            "TotalSent", th.IntegerType, description="Total number of emails sent"
        ),
        th.Property(
            "TotalOpens", th.IntegerType, description="Total number of email opens"
        ),
        th.Property(
            "UniqueOpens", th.IntegerType, description="Number of unique email opens"
        ),
        th.Property(
            "TotalBounces", th.IntegerType, description="Total number of email bounces"
        ),
        th.Property(
            "TotalForwards",
            th.IntegerType,
            description="Total number of email forwards",
        ),
        th.Property(
            "UniqueForwards",
            th.IntegerType,
            description="Number of unique email forwards",
        ),
        th.Property(
            "TotalLinkClicks", th.IntegerType, description="Total number of link clicks"
        ),
        th.Property(
            "UniqueLinkClicks",
            th.IntegerType,
            description="Number of unique link clicks",
        ),
        th.Property(
            "RecipientsCount", th.IntegerType, description="Total number of recipients"
        ),
        th.Property(
            "IsTransactional",
            th.BooleanType,
            description="Indicates whether the campaign is transactional",
        ),
        th.Property(
            "TotalComplaints", th.IntegerType, description="Total number of complaints"
        ),
        th.Property(
            "TotalUnsubscribes",
            th.IntegerType,
            description="Total number of unsubscribes",
        ),
        th.Property(
            "CampaignSource",
            th.StringType,
            nullable=True,
            description="Source of the campaign if applicable",
        ),
        th.Property(
            "CampaignType",
            th.StringType,
            description="Type of the campaign (e.g., Digest)",
        ),
        th.Property(
            "profile_id",
            th.StringType,
        ),
    ).to_dict()
