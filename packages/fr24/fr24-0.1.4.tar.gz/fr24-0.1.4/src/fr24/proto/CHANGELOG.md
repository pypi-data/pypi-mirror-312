# Changelog

All known changes of the gRPC messages are documented here.

Client versions are usually updated every 5 days, most frequently on Mon/Tue 10am. This list is not exhaustive.

## `24.333.0902` (2024-11-28)

- add field: `Flight.position_buffer`
- add message: `RecentPosition`, `PositionBuffer`
- add field: `FlightStage::DIVERSION`

## `24.288.0818` (2024-10-14)
- rename fields: `FlightStage::ASCENDING`, `FlightStage::DESCENDING`

## `24.200.1841` (2024-07-18)
- add field: `FlightProgress.progress_pct`
- add message: `HistoricTrailRequest`

## `24.184.2001` (2024-07-02)
- add field: `FlightProgress.delay_status`

## `24.171.1153` (2024-06-19)
- update message: `FlightProgress`
- update message: `FollowFlightRequest.restriction_mode`

## `24.169.0808` (2024-06-17)

- rename fields: `RestrictionVisibility`
- add message: `Duration`, `Tick`
- add message: `RadarHistoryRecord`
- add message: `FetchSearchIndexRequest`, `FetchSearchIndexResponse`
- add message: `ImageInfo`, `AircraftInfo`, `Point`, `Coordinate`, `Fix`, `AltArrival`, `FlightPlan`, `ScheduleInfo`, `FlightStage`, `FlightProgress`, `ExtendedFlightInfo`, `TrailPoint`
- add message: `LiveTrailRequest`, `LiveTrailResponse`
- add message: `FollowedFlight`, `TopFlightsRequest`, `TopFlightsResponse`

___

# `23.108.1135` (2023-04-18)

- gRPC endpoint introduced.

