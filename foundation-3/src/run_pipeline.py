from acquire_data import acquire_data
from transform_data import transform_data


def run_pipeline():
    print("Starting pipeline...")

    raw = acquire_data()
    print("Acquired rows:", len(raw))

    cleaned = transform_data()
    print("Transformed rows:", len(cleaned))

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()