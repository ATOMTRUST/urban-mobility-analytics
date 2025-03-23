# Urban Mobility Analytics - Data Models

This document defines the core data models used throughout the Urban Mobility Analytics platform.

## Transit Vehicle Data

### Schema: `transit_vehicle`
| Field            | Type      | Description                                        |
|------------------|-----------|---------------------------------------------------|
| vehicle_id       | string    | Unique identifier for the vehicle                  |
| vehicle_type     | string    | Type of vehicle (bus, train, etc.)                 |
| route_id         | string    | Identifier for the route being serviced            |
| timestamp        | timestamp | Time of the position update                        |
| latitude         | float     | Current latitude                                   |
| longitude        | float     | Current longitude                                  |
| speed            | float     | Current speed in km/h                              |
| bearing          | float     | Direction of travel in degrees (0-359)             |
| occupancy_status | int       | Occupancy level (0-4, empty to full)               |
| status           | string    | Operational status (in_service, out_of_service)    |
| next_stop        | string    | ID of the next scheduled stop                      |
| delay            | int       | Seconds behind or ahead of schedule (negative=ahead)|

## Passenger Events

### Schema: `passenger_event`
| Field            | Type      | Description                                        |
|------------------|-----------|---------------------------------------------------|
| event_id         | string    | Unique identifier for the event                    |
| event_type       | string    | Type of event (check_in, check_out, transfer)      |
| timestamp        | timestamp | Time of the event                                  |
| passenger_id     | string    | Anonymized passenger identifier                    |
| station_id       | string    | Station/stop where event occurred                  |
| vehicle_id       | string    | Vehicle involved (if applicable)                   |
| route_id         | string    | Route identifier                                   |
| fare_amount      | float     | Amount charged for the trip                        |
| payment_method   | string    | Method of payment                                  |

## Weather Data

### Schema: `weather`
| Field            | Type      | Description                                        |
|------------------|-----------|---------------------------------------------------|
| weather_id       | string    | Unique identifier for the weather record           |
| timestamp        | timestamp | Time of the weather observation                    |
| location_id      | string    | Area identifier                                    |
| temperature      | float     | Temperature in Celsius                             |
| precipitation    | float     | Precipitation amount in mm                         |
| wind_speed       | float     | Wind speed in km/h                                 |
| wind_direction   | int       | Wind direction in degrees                          |
| weather_condition| string    | Weather condition (clear, rain, snow, etc.)        |
| visibility       | float     | Visibility in km                                   |

## Incidents

### Schema: `incident`
| Field            | Type      | Description                                        |
|------------------|-----------|---------------------------------------------------|
| incident_id      | string    | Unique identifier for the incident                 |
| incident_type    | string    | Type of incident (accident, maintenance, etc.)     |
| timestamp_start  | timestamp | Start time of the incident                         |
| timestamp_end    | timestamp | End time of the incident (null if ongoing)         |
| latitude         | float     | Latitude of incident                               |
| longitude        | float     | Longitude of incident                              |
| route_ids        | array     | Routes affected by the incident                    |
| severity         | int       | Severity level (1-5, 5 being most severe)          |
| description      | string    | Description of the incident                        |
| status           | string    | Current status (active, resolved, etc.)            |

## Routes and Stops

### Schema: `route`
| Field            | Type      | Description                                        |
|------------------|-----------|---------------------------------------------------|
| route_id         | string    | Unique identifier for the route                    |
| route_name       | string    | Human-readable name                                |
| route_type       | string    | Type of transportation (bus, subway, etc.)         |
| start_stop_id    | string    | First stop on the route                            |
| end_stop_id      | string    | Last stop on the route                             |
| frequency        | int       | Service frequency in minutes                       |
| active           | boolean   | Whether route is currently active                  |

### Schema: `stop`
| Field            | Type      | Description                                        |
|------------------|-----------|---------------------------------------------------|
| stop_id          | string    | Unique identifier for the stop                     |
| stop_name        | string    | Human-readable name                                |
| latitude         | float     | Latitude coordinate                                |
| longitude        | float     | Longitude coordinate                               |
| routes           | array     | Routes serving this stop                           |
| amenities        | array     | Available amenities at the stop                    |
| wheelchair_access| boolean   | Whether stop has wheelchair accessibility          |

## Data Relationships

- A **vehicle** operates on a **route** and makes **stops**
- **Passengers** generate **events** at **stops** or on **vehicles**
- **Incidents** and **weather** can affect **routes** and **vehicles**
- **Routes** connect multiple **stops** in a specific sequence