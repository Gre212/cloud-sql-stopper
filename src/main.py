import logging
import google.auth
from googleapiclient import discovery

# Set up logging once at module level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def stop_cloud_sql_instances(request):
    """Stops Cloud SQL instances that do not have the 'auto_stop' label set to 'false'."""

    try:
        # Get credentials and project ID
        credentials, project_id = google.auth.default()
        
        # Build the Cloud SQL Admin API service
        service = discovery.build('sqladmin', 'v1beta4', credentials=credentials)

        # List all instances in the project
        list_request = service.instances().list(project=project_id)
        response = list_request.execute()
        instances = response.get('items', [])

        if not instances:
            logger.info("No Cloud SQL instances found.")
            return "No instances found", 200

        stopped_count = 0
        skipped_count = 0
        error_count = 0

        for instance in instances:
            name = instance.get('name')
            state = instance.get('state')
            user_labels = instance.get('settings', {}).get('userLabels', {})
            
            # Check if instance should be skipped
            if user_labels.get('auto_stop') == 'false':
                logger.info(f"Skipping instance {name} (auto_stop=false)")
                skipped_count += 1
                continue

            # Get current activation policy
            activation_policy = instance.get('settings', {}).get('activationPolicy', 'ALWAYS')

            # Skip if instance is not runnable or already set to stop
            if state != 'RUNNABLE' or activation_policy == 'NEVER':
                logger.info(f"Instance {name} is not stoppable (State: {state}, ActivationPolicy: {activation_policy})")
                skipped_count += 1
                continue

            # Stop the running instance
            logger.info(f"Stopping instance {name} (State: {state}, ActivationPolicy: {activation_policy})...")

            try:
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

            except Exception as patch_error:
                logger.error(f"Unexpected error stopping instance {name}: {patch_error}")
                error_count += 1
                # Continue processing other instances even if one fails

        return (f"Processed {len(instances)} instances: "
                f"Stopped: {stopped_count}, "
                f"Skipped: {skipped_count}, "
                f"Errors: {error_count}"), 200

    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return f"Unexpected error: {e}", 500
