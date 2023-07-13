from DataAccessLib.database.models import (BotBuilderBlock, BotBuilderBlockFeatureMapping,
                                           Feature)


def get_dialog_feature_mapping_data(conn):
    """
    SQLAlchemy query to fetch the Dialog <-> Feature mapping data from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object

    :return: Dialog <-> Feature mapping data
   """
    return conn.query(BotBuilderBlockFeatureMapping).with_entities(
        BotBuilderBlockFeatureMapping.bot_builder_block_id.label("bot_builder_block_id"),
        BotBuilderBlockFeatureMapping.feature_id.label("feature_id"),
        BotBuilderBlock.key.label('bot_builder_block_key'),
        Feature.key.label('feature_key')
    ).join(
        BotBuilderBlock, BotBuilderBlockFeatureMapping.bot_builder_block_id == BotBuilderBlock.id
    ).join(
        Feature, BotBuilderBlockFeatureMapping.feature_id == Feature.id
    ).all()
