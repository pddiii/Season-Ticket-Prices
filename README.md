# Season-Ticket-Prices

This repository utilizes the SeatGeek API interface to scrape tickets and ticket statistics for the home team of MLB games.

## Ticket Prices file

[Ticket Prices](ticket_prices.py) is a file which contains a function `get_tickets`

`get_tickets` arguments:

- `home_team_name: str`
  - The home team
  - e.g. 'philadelphia-phillies'
- `start_date: str`
  - e.g. '2024-03-31'
- `end_date: str`
  - e.g. '2024-09-15'

When the script is run, the file by default is set to scrape ticket prices for the Philadelphia Phillies because I'm interested in their home game ticket prices.

When the script runs it does not output a dataframe, but creates a csv file containing the scraped ticket information for the home team.

## CSV file Variables

| Variable                        | Description                                                           | Type  |
|---------------------------------|-----------------------------------------------------------------------|-------|
| datetime_utc                    | Date and Time of the Game                                             | str   |
| sg_url                          | SeatGeek URL to the game tickets                                      | str   |
| sg_score                        | Average SeatGeek Deal score for available tickets                     | float |
| type                            | Type of Event "mlb" by default of the function endpoints              | str   |
| home_team                       | Home MLB team                                                         | str   |
| away_team                       | Away MLB team                                                         | str   |
| slug                            | ID for SeatGeek ('philadelphia-phillies')                             | str   |
| short_name                      | Team short name ('phillies')                                          | str   |
| listing_count                   | Number of Tickets listings                                            | int   |
| average_price                   | Average price of ticket listings                                      | float |
| lowest_price_good_deals         | Lowest price for deals considered "good"                              | float |
| lowest_price                    | Lowest price for any tickets                                          | float |
| highest_price                   | Highest price for any tickets                                         | float |
| visible_listing_count           | Visible ticket listings                                               | int   |
| median_price                    | Median price for any tickets                                          | float |
| lowest_sg_base_price            | Lowest SeatGeek ticket base price                                     | float |
| lowest_sg_base_price_good_deals | Lowest SeatGeek ticket base prices for deals considered "good"        | float |
| ticket_count                    | Number of Tickets available                                           | int   |
| headline                        | Promotion headline/title                                              | str   |
| additional_info                 | Additional details concerning the Promotion                           | str   |