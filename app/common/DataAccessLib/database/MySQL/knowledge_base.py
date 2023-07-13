from DataAccessLib.database.models import KnowledgeBase


def get_knowledge_base_details(conn, knowledge_base_id):
    """
    SQLAlchemy query to get Knowledge base data
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param knowledge_base_id: INTEGER: knowledge_base_id id
       :return: knowledge base details
    """
    return conn.query(KnowledgeBase).with_entities(
        KnowledgeBase.account_id.label("account_id"),
        KnowledgeBase.status.label("status"),
        KnowledgeBase.configurations.label("configurations"),
        KnowledgeBase.trained_model.label("trained_model"),
        KnowledgeBase.type.label("type"),
    ).filter(KnowledgeBase.id == knowledge_base_id).first()
