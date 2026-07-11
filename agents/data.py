import kagglehub
from kagglehub import KaggleDatasetAdapter


def get_data():
    """Get data from Kaggle dataset."""
    file_path = "online_advertising_performance_data.csv"

    df = kagglehub.dataset_load(
    KaggleDatasetAdapter.PANDAS,
    "naniruddhan/online-advertising-digital-marketing-data",
    file_path
    )
    return df

if __name__ == "__main__":
    df = get_data()
    print(df.head())