                    +-------------------------+
                    |     User / Client       |
                    +------------+------------+
                                 |
                                 v
                     GET /prices/latest?...
                                 |
                      +----------v----------+
                      |      FastAPI        |
                      |    (app.main)       |
                      +----------+----------+
                                 |
                     Publish to Kafka Topic: price-events
                                 |
                      +----------v----------+
                      |       Kafka         |
                      +----------+----------+
                                 |
               Consumer reads   |
                                 v
           +-----------------------------+
           | Kafka Consumer (Python)     |
           | - Calculates Moving Average |
           | - Writes to PostgreSQL      |
           +--------------+--------------+
                          |
                          v
               +---------------------+
               |     PostgreSQL      |
               |  - Prices Table     |
               |  - Averages Table   |
               +---------------------+
