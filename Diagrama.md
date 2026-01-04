                    +-------------------------+
                    |     User / Client       |
                    +------------+------------+
                                 |
                                 v
                     GET /mock/prices/latest?...
                     POST /send-price {symbol, price}
                                 |
                      +----------v----------+
                      |      FastAPI        |
                      |    (app.main)       |
                      +----------+----------+
                                 |
                     Publish to Kafka Topic: test-topic
                                 |
                      +----------v----------+
                      |       Kafka         |
                      +----------+----------+
                                 |
               Consumer reads   |
                                 v
           +-----------------------------+
           | Kafka Consumer (Python)     |
           | - Processes messages        |
           | - Writes to PostgreSQL      |
           +--------------+--------------+
                          |
                          v
               +---------------------+
               |     PostgreSQL      |
               |  - Prices Table     |
               |  - Optional Stats   |
               +---------------------+
