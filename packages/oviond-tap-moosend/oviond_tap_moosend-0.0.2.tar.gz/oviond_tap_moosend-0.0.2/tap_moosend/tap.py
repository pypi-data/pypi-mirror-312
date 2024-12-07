"""Moosend tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_moosend import streams


class TapMoosend(Tap):
    """Moosend tap class."""

    name = "tap-moosend"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            title="API Token",
            description="The token to authenticate against the API service",
        )
    ).to_dict()

    def discover_streams(self) -> list[streams.MoosendStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.CampaignsStream(self),
        ]


if __name__ == "__main__":
    TapMoosend.cli()
