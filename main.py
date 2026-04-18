from app.auth.gmail_auth import authenticate_gmail
from app.db.database import initialize_database
from app.services.extraction_service import extract_and_store_threads
from app.services.advanced_classification import classify_all_threads
from app.services.thread_state_engine import apply_thread_state_engine
from app.services.priority_engine import apply_priority_engine
from app.services.metrics_service import print_core_metrics

def main():
    initialize_database()
    service = authenticate_gmail()

    extract_and_store_threads(service)
    classify_all_threads()
    apply_thread_state_engine()
    apply_priority_engine()
    print_core_metrics()

if __name__ == "__main__":
    main()
