# The Running API

The Running API is a python library intended to provide functionality for organizing and understanding data from various running activities. Funcitons and classes for both trainig runs and races are included as well as helpers for implementing functions from the Strava API.

## Strava Client
The Running API comes with classes that automate the interaction with the Strava REST API. This allows The Running API to quickly grab runs that have been posted to Strava profiles and clubs assuming the user has an available application registered with Strava.

Let's see an example of how to instance a Strava activities client to pull data from a series of runs.

>**Note**: You will need to set up a Strava application first and get the Client ID and Client Secret at well as the authorization token and other information related to the athlete profile. Strava has instructions on how to set this up [here](https://developers.strava.com/docs/getting-started/).

```python
from running_api.utils.strava_utils import StravaActivitiesClient
from running_api.schemas.schemas import AthleteStravaAccessToken, StravaClientConfig

# set up some pre-requisites
# you will need to substitue your own values
athlete_token = AthleteStravaAccessToken(
    athlete_name = "Test Athlete",
    token_type = "Bearer",
    access_token = "Test Token",
    expires_at = 100000,
    expires_in = 100000,
    refresh_token = "Test Refresh Token",
)

client_config = StravaClientConfig(
    client_id = 10000,
    client_secret = "Test Secret",
)

# initialize the client
client = StravaActivitiesClient(
    athlete_token,
    client_config
)

# now let's grab some activity data!
single_activity = client.get_individual_activity_stats(
    "Test Activity ID"
)

# we can also grab a series of runs in a time range
many_activities = client.get_activities_in_time_range(
    start = "2023-10-10T00:00:00",
    end = "2023-10-15T00:00:00",
)
```

Note that all of the data returned from these functions are in json format. This can be occasionally cumbersome to work with, so *The Running API* has provided the user with some custom workout datatypes to load these activities into.

>**Note:** A particular quirk in how authentication is handled with the Strava API requires that the access token be refreshed after 6 hours. The `StravaActivitiesClient` handles this automatically, but the new values for the `access_token`, `refresh_token`, and the expiration timeout values will need to be stored somewhere for the next use otherwise the user will need to generate a fresh set of tokens as outlined in the Strava API documentation. It is suggested that these updated values are continuously saved into a file and loaded any time a new set of activities is pulled. Simply pull the up-to-date access token information by getting the `StravaActivitiesClient.athlete_token` attribute and then save to a file. 

## Loading Workout Activities
As mentioned above, if one would like a simple interface to organize and load many workouts into a list of custom datatypes, we have a specialized function to do just that.

```python
from running_api.utils.training_utils import get_training_runs

# reuse the client created in the previous section
# initialize the client
client = StravaActivitiesClient(
    athlete_token,
    client_config
)

training_runs = get_training_runs(
    client, 
    start = "2023-10-10T00:00:00",
    end = "2023-10-15T00:00:00",
)
```

The `training_runs` object is a list storing each activity as a `TrainingRun` class. This hopefully will be a little easier to manage than the dict\json object. In addition, functions such as `convert_training_runs_to_df` are provided to convert lists of `TrainingRun` objects into dataframes for even more flexibility.

## Racing Tools
There are also some niffty ways to organize and ***track*** racing data. Let's suppose we want to note down what an athlete has done for a particular race. We can use a real-life example from the 2024 US Olympic Trials.

```python
from running_api.utils.race_utils import Race, RaceType
from running_api.utils.data_utils import save_races

# let's log a track race
individual_race = Race(
    athlete = "Grant Fisher",
    race_name = "U.S. Olympic Trials",
    date = "2024-06-21T22:27:00",
    tot_time = 1669.47, #s
    tot_distance = 10000, #m
    location = "Eugine, OR",
    race_type = RaceType.OUTDOOR_TRACK,
)

# let's add the first 400m as a split
individual_race.add_split(
    time = 64.43,
    start_loc = 0.0,
    end_loc = 400.0,
)

# now we can can save this race to a json file for later analysis
race_collection = [individual_race] # this can be a list of many races

save_races(race_collection, "races.json")

```

## Analysis
There are a few ways that these training and racing activities can be processed. One of the first ways that one can evaluate a set of training runs would be to find the total volume of a collection of workouts.

Currently, *The Running API* calculates volume by $V = mileage*intensity$. Practically, over a collection of runs, this is computed using $V=\sum_{i=0}^{N} m(i)pe(i)$ where $m(i)$ is the total miles for run $i$ and $pe(i)$ is the percieved effort, usually expressed as a range from 1-10. There are certainly many other ways to compute volume, but this appears simple enough to be useful to a broad range of users.

Let's take a collection of training runs over the course of a week `runs`, collected using the `get_training_runs` function, and calculate the volume using the above fomula assuming percieved effort values are included.

```python
from running_api.analysis.metrics import collection_volume

weekly_volume = collection_volume(runs)
```

The user can also set flags based on volume to evaluate if some volume or mileage limit has been reached.

```python
from running_api.analysis.flags import is_high_volume_collection, is_high_mileage_collection

high_volume = is_high_volume_collection(
    runs, 
    volume_limit = 500, 
    distance_units = "km", # set distance to km
)
high_mileage = is_high_mileage_collection(
    runs, 
    mileage_limit = 40, 
    distance_units = "mi", # distance in miles
)
```

## Getting Weekly Statistics
Let's say that a user is interested in understanding how weekly mileage and pace has changed over a given build phase of marathon preparation. If the user has been bulding through the last 12 weeks, then they can use the `get_previous_weekly_metrics` function provided.

```python
from running_api.utils.strava_utils import StravaActivitiesClient
from running_api.schemas.schemas import AthleteStravaAccessToken, StravaClientConfig
from running_api.analysis.macro_analysis import get_previous_weekly_metrics

athlete_token = AthleteStravaAccessToken(
    athlete_name = "Test Athlete",
    token_type = "Bearer",
    access_token = "Test Token",
    expires_at = 100000,
    expires_in = 100000,
    refresh_token = "Test Refresh Token",
)

client_config = StravaClientConfig(
    client_id = 10000,
    client_secret = "Test Secret",
)

# initialize the client
client = StravaActivitiesClient(
    athlete_token,
    client_config
)


weekly_df, runs_df = get_previous_weekly_metrics(client, previous_weeks = 12)
```
