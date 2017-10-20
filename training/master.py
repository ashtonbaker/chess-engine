
from google.cloud import pubsub_v1

def create_topic(project, topic_name):
    """Create a new Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    topic = publisher.create_topic(topic_path)

    print('Topic created: {}'.format(topic))

def create_player_database(num_players):
    return None

def select_two_players():
    return None
