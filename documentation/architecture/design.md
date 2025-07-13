# Channel Monitoring Project - Data Flows 

An initial design specification for a system to monitor channel crossing through vessel activities and weather forecasting. This is to establish safer passage and accountability in case of harm is to promote safe and legal migration routes for a more open world.

## Data Sources

### Weather Forecast
The weather reporting is done daily, at the same time.
We need to establish risk related parameters. these include wave height, wind speed and direction, currents, temperature, water temperature and others.

### AIS Boat Position Reports
We collect positioning reports that include a list of boats currently in the arena. This information includes position, speed, headings, op code, and other.


## Processing

### Downsampling
Position reports needs to be downsampled for storage, where we may be receiving many position reports for each boat every minute, we only need an archive every few minutes.

### Alert handling
Based on the position reports, we try and guess when relevant activity is happening, using vectors like speed change, and position of boat, and later on based on predictive statistical model, we try and understand when situations that require out attention arise, and send alerts that would allow us to respond accordingly. 

### Crossing risk asessment
Using the weather forecast, we try and produce a prediction of the likelihood of an attempted crossing, and the risk to life posed by crossing.

### Weather forecast plotting
Using the weather forecast data, we plot information about the next day relevant weather conditions, 

### Arena plotting
When we decide we are sending out an alert, we will plot the arena, this will include bositions and names of relevant boats, classified by type if known. The plot cloud include information like sea conditions. Relevant boats should show a recent trail, speed, headings, etc.

If a relevant boat has it's AIS transimition off, we should record it with a label and a gray dot on the last known position.

## Data Storage

### Database
Position reports and daily crossing risk assesments will be stored for reference and modeling. Position reports are downsampled, and will be in a minute or several minutes granularity at most.

## Dispatch
### Forecast
A daily report composed mosly of the weather related crossing risk report and a plot is dispatched, possibly through email or a chat client, discord, or another.

### Alert
This is dispatched when the predictive system identify activities that require our attention or intervention. It includes a plot of the arena and some labels related to the conditions that triggered it, for example a rescue boat speeding, or a border force boat in an area identified as likely inteception zone.

### API
The API is a subsystem that connects this system to others. it can query the database, receive live position updates, and produces graphs and data that can be consumed by other services, such as the wordpress website. this will be done by providing REST API endpoints.

``` mermaid
flowchart LR
    AIS_EVENT(["New position report"]) --> AIS
    AIS["AIS Producer"] --> QUEUE[/"Position reports Queue"\]
    QUEUE --> PRC["Periodic Position Reports Consumer"]
    PRC --> DOWN_SAMPLER["Downsampler"]
    DOWN_SAMPLER --> DB[("Database")]
    QUEUE --> QUEUE_EVENT(["Queue Event"])
    QUEUE_EVENT --> QUEUE_EVENT_CONSUMER["Queue Event Consumer"]
    UPDATE_API["Update API"]
    ALERT_HANDLER["Alert Handler"]
    QUEUE_EVENT_CONSUMER --> ALERT_HANDLER
    QUEUE_EVENT_CONSUMER --> UPDATE_API
    DB --> ALERT_HANDLER
    UPDATE_API --> API["API"]
    DB -->API
    ALERT_HANDLER --> ALERT_SCENE_PLOTTING["Plot Arena"]
    ALERT_SCENE_PLOTTING --> ALERT(["Alert"])

    %% Weather
    SCHEDULED_FORECAST["Scheduled Forecast"]
    RISK_EVALUATION["Crossing Risk Evaluation"]
    PLOT_WEATHER["Plot Forecast data"]
    FORECAST_REPORT["Weather forecast dispatch"]

    SCHEDULED_FORECAST --> RISK_EVALUATION
    RISK_EVALUATION --> PLOT_WEATHER --> FORECAST_REPORT["Crossing risk forecast report"]
    RISK_EVALUATION --> DB
```
