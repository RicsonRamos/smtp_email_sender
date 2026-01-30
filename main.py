from runner import run_campaign
from utils.logger import log_event

def main() -> None:
    """
    Main entry point of the email campaign process.

    This function logs the start of the process, calls the run_campaign
    function to send the emails and logs the completion of the process.

    :return: None
    """
    log_event("🚀 Starting Email Campaign Process")
    run_campaign()
    log_event("🏁 Process Completed")

if __name__ == "__main__":
    main()