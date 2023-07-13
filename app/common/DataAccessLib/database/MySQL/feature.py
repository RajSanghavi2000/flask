from DataAccessLib.database.models import (FeatureMinimumPlanMapping, Feature, Plan)


def get_feature_minimum_plan_mapping_data(conn):
    """
    SQLAlchemy query to fetch <-> Minimum plan mapping data from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object

    :return: Dialog <-> Feature mapping data
   """
    return conn.query(FeatureMinimumPlanMapping).with_entities(
        FeatureMinimumPlanMapping.minimum_plan_id.label("plan_id"),
        FeatureMinimumPlanMapping.feature_id.label("feature_id"),
        Plan.name.label('plan_name'),
        Plan.stripe_plan_id.label('stripe_plan_id'),
        Feature.key.label('feature_key')
    ).join(
        Feature, FeatureMinimumPlanMapping.feature_id == Feature.id
    ).outerjoin(
        Plan, FeatureMinimumPlanMapping.minimum_plan_id == Plan.id
    ).all()
