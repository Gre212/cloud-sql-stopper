import logging
import google.auth
from googleapiclient import discovery
from googleapiclient.errors import HttpError

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
        try:
            request = service.instances().list(project=project_id)
            response = request.execute()
            instances = response.get('items', [])
        except HttpError as http_error:
            logger.error(f"Failed to list Cloud SQL instances: {http_error}")
            return f"Failed to list instances: {http_error}", 500
        except Exception as e:
            logger.error(f"Unexpected error listing instances: {e}")
            return f"Unexpected error: {e}", 500

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

            # Get current activation policy
            activation_policy = instance.get('settings', {}).get('activationPolicy', 'ALWAYS')

            # Stop the instance if it is running
            # Check both state and activation policy to ensure instance is truly running
            if state == 'RUNNABLE' and activation_policy != 'NEVER':
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

                except HttpError as http_error:
                    error_message = str(http_error)

                    # Check if the error is about updating properties when instance is stopped
                    if "properties other than activation policy are not allowed" in error_message:
                        logger.warning(f"Instance {name} appears to be in an intermediate state. It may have been stopped recently.")
                    else:
                        logger.error(f"HTTP error stopping instance {name}: {http_error}")
                    # Continue processing other instances even if one fails

                except Exception as patch_error:
                    logger.error(f"Unexpected error stopping instance {name}: {patch_error}")
                    # Continue processing other instances even if one fails

            elif state in ['STOPPED', 'SUSPENDED'] or activation_policy == 'NEVER':
                logger.info(f"Instance {name} is already stopped (State: {state}, ActivationPolicy: {activation_policy}). Skipping.")
            else:
                logger.info(f"Instance {name} is in state {state} with ActivationPolicy {activation_policy}. Skipping.")

        return f"Processed {len(instances)} instances. Initiated stop for {stopped_count} instances.", 200

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return f"Error: {e}", 500
