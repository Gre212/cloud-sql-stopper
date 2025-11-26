import logging
import google.auth
from googleapiclient import discovery

def stop_cloud_sql_instances(request):
    """Stops Cloud SQL instances that do not have the 'auto_stop' label set to 'false'."""
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Get credentials and project ID
        credentials, project_id = google.auth.default()
        
        # Build the Cloud SQL Admin API service
        service = discovery.build('sqladmin', 'v1beta4', credentials=credentials)

        # List all instances in the project
        request = service.instances().list(project=project_id)
        response = request.execute()
        instances = response.get('items', [])

        if not instances:
            logger.info("No Cloud SQL instances found.")
            return "No instances found", 200

        stopped_count = 0
        
        for instance in instances:
            name = instance.get('name')
            state = instance.get('state')
            user_labels = instance.get('settings', {}).get('userLabels', {})
            
            # Check if instance should be skipped
            if user_labels.get('auto_stop') == 'false':
                logger.info(f"Skipping instance {name} (auto_stop=false)")
                continue

            # Stop the instance if it is running
            if state == 'RUNNABLE': # 'RUNNABLE' is the state for running instances in v1beta4
                logger.info(f"Stopping instance {name}...")
                
                stop_request_body = {
                    "settings": {
                        "activationPolicy": "NEVER"
                    }
                }
                
                stop_op = service.instances().patch(
                    project=project_id,
                    instance=name,
                    body=stop_request_body
                ).execute()
                
                logger.info(f"Stop operation initiated for {name}: {stop_op.get('name')}")
                stopped_count += 1
            else:
                logger.info(f"Instance {name} is not running (State: {state}). Skipping.")

        return f"Processed {len(instances)} instances. Initiated stop for {stopped_count} instances.", 200

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return f"Error: {e}", 500
