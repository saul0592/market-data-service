from datetime import datetime, timedelta
import logging


def is_data_fresh(price_obj, max_age_hours: int = 24) -> bool:

    """
        Verify the data is recent(less than the x hours)

        args:
            price_objs: object price of the data base
            max_age_hours: max of the hous to consider fresh data

        returns:
            Bool:
                True -> if is fresh 
                False -> Data is old

    """


    if not price_obj:
        return price_obj

    data_age = datetime.utcnow() - price_obj.timestamp.replace(tzinfo= None)

    if data_age < timedelta(hours= max_age_hours):
        return True 
    else: 
        logging.info(f"Old data {price_obj.symbol}: {data_age.total_seconds()/3600:.1f} horas")
        return False
        
