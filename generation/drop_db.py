import os


def drop_db():

    os.system(f"rm -rf ./neo_db_data")
    os.system(f"cp -r ./neo_db_data_backup ./neo_db_data")


if __name__ == "__main__":
    drop_db()
