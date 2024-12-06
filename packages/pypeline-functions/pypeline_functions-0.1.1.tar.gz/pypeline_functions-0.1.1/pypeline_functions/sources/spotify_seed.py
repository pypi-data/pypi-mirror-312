import json
from collections.abc import Iterable, Sequence

import dlt
from dlt.sources import DltResource

from ..models.spotify import FollowData, Identifier, Library, Marquee, SearchQueries, StreamingHistory, UserData
from ..parsers.json_parser import Spotify
from ..utils.google_cloud_storage import GoogleCloudStorage


@dlt.source
def spotify_seed(bucket_name:str) -> Sequence[DltResource]:
    """
    Extract data from the Spotify seed located in Google Cloud Storage.

    Parameters
    ----------
    bucket_name : str
        The name of the bucket that the seed is located in.
    """
    ACCOUNT_DATA_PATH = "spotify/account_data/"  # noqa: N806
    STREAMING_HISTORY_PATH = "spotify/streaming_history" #noqa: N806
    DATETIME_FORMAT = "%Y%m%dT%H%M%S"  # noqa: N806
    gcs = GoogleCloudStorage()
    spotify = Spotify()


    @dlt.resource(
        name="follow_data",
        write_disposition="replace",
        columns=FollowData
    )
    def follow_data() -> Iterable[FollowData]:
        """Extract the latest follow data."""
        latest_seeds = gcs.get_latest_seeds(bucket_name, ACCOUNT_DATA_PATH, "Follow.json", DATETIME_FORMAT)
        for seed in latest_seeds:
            content = seed.download_as_string().decode("utf-8", "replace")
            data = json.loads(content)
            data = spotify.follow_data_parser(data)
            yield data

    @dlt.resource(
        name="identifier",
        write_disposition="replace",
        columns=Identifier
    )
    def identifier() -> Iterable[Identifier]:
        """Extract the latest identifier data."""
        latest_seeds = gcs.get_latest_seeds(bucket_name, ACCOUNT_DATA_PATH, "Identifiers.json", DATETIME_FORMAT)
        for seed in latest_seeds:
            content = seed.download_as_string().decode("utf-8", "replace")
            data = json.loads(content)
            data = spotify.identifier_parser(data)
            yield data

    @dlt.resource(
        name="marquee",
        write_disposition="replace",
        columns=Marquee
    )
    def marquee() -> Iterable[Marquee]:
        """Extract the latest marquee data."""
        latest_seeds = gcs.get_latest_seeds(bucket_name, ACCOUNT_DATA_PATH, "Marquee.json", DATETIME_FORMAT)
        for seed in latest_seeds:
            content = seed.download_as_string().decode("utf-8", "replace")
            data = json.loads(content)
            data = [spotify.marquee_parser(datum) for datum in data]
            yield data

    @dlt.resource(
        name="search_queries",
        write_disposition="merge",
        primary_key=("search_query", "search_time"),
        columns=SearchQueries
    )
    def search_query() -> Iterable[SearchQueries]:
        """Extract the latest search query data."""
        latest_seeds = gcs.get_latest_seeds(bucket_name, ACCOUNT_DATA_PATH, "SearchQueries.json", DATETIME_FORMAT)
        for seed in latest_seeds:
            content = seed.download_as_string().decode("utf-8", "replace")
            data = json.loads(content)
            data = [spotify.search_query_parser(datum) for datum in data]
            yield data

    @dlt.resource(
        name="user_data",
        write_disposition="replace",
        columns=UserData
    )
    def user_data() -> Iterable[UserData]:
        """Extract the latest user data."""
        latest_seeds = gcs.get_latest_seeds(bucket_name, ACCOUNT_DATA_PATH, "Userdata.json", DATETIME_FORMAT)
        for seed in latest_seeds:
            content = seed.download_as_string().decode("utf-8", "replace")
            data = json.loads(content)
            data = spotify.user_data_parser(data)
            yield data

    @dlt.resource(
        name="library",
        write_disposition="replace",
        columns=Library
    )
    def library() -> Iterable[Library]:
        """Extract the latest library data."""
        latest_seeds = gcs.get_latest_seeds(bucket_name, ACCOUNT_DATA_PATH, "YourLibrary.json", DATETIME_FORMAT)
        for seed in latest_seeds:
            content = seed.download_as_string().decode("utf-8", "replace")
            data = json.loads(content)
            data = spotify.library_parser(data)
            yield data

    @dlt.resource(
        name="audio_streaming_history",
        write_disposition="merge",
        primary_key="ts",
        columns=StreamingHistory
    )
    def audio_streaming_history() -> Iterable[StreamingHistory]:
        """Extract the latest audio streaming history data."""
        blobs = gcs.list_blobs_with_prefix(bucket_name=bucket_name, prefix=STREAMING_HISTORY_PATH)
        streaming_history_files = [blob for blob in blobs if blob.name.endswith(".json") and "Audio" in blob.name]
        for f in streaming_history_files:
            content = f.download_as_string().decode("utf-8", "replace")
            data = json.loads(content)
            data = [spotify.streaming_history_parser(datum) for datum in data]
            yield data


    return follow_data, identifier, marquee, user_data, library, search_query, audio_streaming_history
